"""Reproducible local retrieval/source checks; does not evaluate a live creative AI."""
import argparse
import json
from pathlib import Path
from knowledge_library import ROOT, dump, load_release, read_archives, resolve_pointer, search_examples
from verify_source_integrity import sha256_file


def evaluate(root=ROOT):
    root = Path(root)
    bank = json.loads((root / "evaluations/stage3/cases.json").read_text())
    baseline = root / "evaluations/stage3/baseline.json"
    if baseline.exists() and json.loads(baseline.read_text())["question_bank_sha256"] != sha256_file(root / "evaluations/stage3/cases.json"):
        raise ValueError("Frozen evaluation bank changed; create a new bank/version")
    refs = read_archives(root)
    rows = []
    for case in bank["cases"]:
        row = {"id": case["id"], "kind": case["kind"], "split": case["split"]}
        if case["kind"] == "retrieval":
            found = search_examples(case["query"], root)
            row.update(returned_reference_ids=found,
                       passed=set(case["expected_reference_ids"]) <= set(found),
                       measurement="positive_example_recall_only")
        elif case["kind"] == "source_value":
            actual = resolve_pointer(refs[case["reference_id"]], case["field_path"])
            row.update(actual=actual, passed=actual == case["expected"],
                       measurement="exact_recorded_value_not_physical_truth")
        else:
            row.update(passed=None, measurement="authored_reference_answer_only",
                       reason="No consumer-model response captured; not scored.")
        rows.append(row)
    scored = [r for r in rows if r["passed"] is not None]
    return {"schema_version": "1.0", "release_id": load_release(root)["release_id"],
            "question_bank_sha256": sha256_file(root / "evaluations/stage3/cases.json"),
            "case_count": len(rows), "automated_cases": len(scored),
            "passed": sum(r["passed"] for r in scored),
            "unscored_reference_answers": len(rows) - len(scored),
            "consumer_model_accuracy": None,
            "limitations": ["Local prototype only; web and GitHub connector are not measured.",
                            "Positive retrieval cases do not measure result precision.",
                            "Development/heldout labels are fixed; heldout is not a live-model benchmark."],
            "cases": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--write", metavar="NAME")
    args = parser.parse_args()
    result = evaluate(args.root)
    if args.write:
        if args.write not in ("baseline", "current"):
            parser.error("Report name must be baseline or current")
        target = args.root / "evaluations/stage3" / (args.write + ".json")
        if args.write == "baseline" and target.exists():
            raise ValueError("Baseline is immutable")
        target.write_text(dump(result))
    print(f"{result['passed']}/{result['automated_cases']} local checks; "
          f"{result['unscored_reference_answers']} unscored reference answers")


if __name__ == "__main__":
    main()
