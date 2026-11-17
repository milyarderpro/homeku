"""Audit static reader navigation and validate recorded remote access, without inventing AI scores."""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

import yaml
from knowledge_library import ROOT, dump, load_release, resolve_pointer
from verify_source_integrity import sha256_file

LINK = re.compile(r"\]\(([^)]+)\)")
ENTRY_LIMITS = {"README.md": 350, "knowledge/README.md": 600, "knowledge/ai-knowledge.md": 1100}
THEMES = [
    "architecture-dna.md", "interior-dna.md", "landscape-dna.md",
    "lighting-and-palette-dna.md", "spatial-design-principles.md",
    "continuity-dna.md", "cinematography-dna.md", "design-compatibility.md",
    "originality-framework.md",
]
TECHNICAL = ("requests/", "tests/", "scripts/", "docs/", "evaluations/",
             "knowledge/enrichment/", "knowledge/reviews/", "knowledge/temporal/",
             "knowledge/releases/", "knowledge/similarity/")
TECHNICAL_FILES = {"knowledge/source-manifest.json", "knowledge/release.json",
                   "knowledge/aggregates.json", "knowledge/diversity.json"}


def visible_reading(text):
    """Details remain accessible, but are not the primary reading sequence."""
    return re.sub(r"<details>.*?</details>", "", text, flags=re.S | re.I)


def local_links(path, text, root):
    root, path = Path(root).resolve(), Path(path)
    result = []
    for target in LINK.findall(text):
        parsed = urlsplit(target)
        if parsed.scheme or target.startswith("#"):
            continue
        item = (path.parent / unquote(parsed.path)).resolve()
        if not item.is_relative_to(root):
            raise ValueError("Link escapes repository: " + target)
        if not item.is_file():
            raise ValueError(f"Missing local link: {path.relative_to(root)} → {target}")
        result.append(item.relative_to(root).as_posix())
    return result


def input_fingerprint(root):
    root = Path(root)
    paths = [root / "README.md", root / "knowledge/release.json",
             *sorted((root / "knowledge").rglob("*.md"))]
    inputs = {p.relative_to(root).as_posix(): sha256_file(p) for p in paths}
    digest = hashlib.sha256(dump(inputs).encode()).hexdigest()
    return digest, inputs


def dependency_impact(changed_paths, release):
    sources = release["references"]
    changed = set(changed_paths)
    taxonomy_changed = any(p.startswith("knowledge/taxonomy/") for p in changed)
    source_changed = {s["reference_id"] for s in sources if
                      s["source_path"] in changed or s["analysis_path"] in changed or
                      any(p.startswith("references/" + s["reference_id"] + "/") for p in changed)}
    affected = sorted(s["reference_id"] for s in sources
                      if s["reference_id"] in source_changed or taxonomy_changed)
    dependents = {}
    for ident in affected:
        paths = [f"knowledge/reference-profiles/{ident}.md", f"knowledge/enrichment/{ident}.json",
                 f"knowledge/design-evidence/{ident}.md", f"knowledge/design-evidence/{ident}.json"]
        if ident in source_changed:
            paths += [f"knowledge/reviews/{ident}.json", f"knowledge/temporal/{ident}/"]
        dependents[ident] = paths
    return {"affected_reference_ids": affected, "source_specific_dependents": dependents,
            "shared_dependents": ["knowledge/directories/", "knowledge/aggregates.json",
                                  "knowledge/diversity.json", "knowledge/corpus-patterns.md",
                                  "knowledge/design-evidence/coverage.json"] if affected else [],
            "requires_new_source_review": bool(source_changed),
            "unpublished_addition_changes_published_knowledge": False}


def audit(root=ROOT):
    root = Path(root).resolve()
    release = load_release(root)
    sizes = {}
    for relative, limit in ENTRY_LIMITS.items():
        path = root / relative
        text = path.read_text()
        if relative == "knowledge/ai-knowledge.md" and re.search(r"!\[|<img\b", text, flags=re.I):
            raise ValueError("Core must remain meaningful without loading embedded images")
        count = len(text.split())
        sizes[relative] = {"words": count, "characters": len(text), "word_limit": limit}
        if count > limit:
            raise ValueError("Reader entry exceeds agreed word budget: " + relative)
        links = local_links(path, visible_reading(text), root)
        if relative != "knowledge/ai-knowledge.md":
            for target in links:
                if target.startswith(TECHNICAL) or target in TECHNICAL_FILES:
                    raise ValueError("Maintenance promoted to primary reading: " + target)
    root_links = local_links(root / "README.md", visible_reading((root / "README.md").read_text()), root)
    if "knowledge/ai-knowledge.md" not in root_links:
        raise ValueError("Root entry does not lead to core")
    guide = (root / "knowledge/README.md").read_text()
    for theme in THEMES:
        if "knowledge/" + theme not in local_links(root / "knowledge/README.md", guide, root):
            raise ValueError("Unreachable design theme: " + theme)
    files = [root / "README.md", *sorted((root / "knowledge").rglob("*.md"))]
    local_link_count = sum(len(local_links(p, p.read_text(), root)) for p in files)
    profile_sizes = {}
    for source in release["references"]:
        ident = source["reference_id"]
        path = root / f"knowledge/reference-profiles/{ident}.md"
        words = len(path.read_text().split())
        profile_sizes[ident] = words
        if words > 1200:
            raise ValueError("Profile too long for selective reading: " + ident)
        source_path = source["analysis_path"]
        if source_path not in local_links(path, path.read_text(), root):
            raise ValueError("Profile lost canonical annotation link: " + ident)
    fingerprint, inputs = input_fingerprint(root)
    return {"schema_version": "1.0", "release_id": release["release_id"],
            "reader_fingerprint": fingerprint, "input_sha256": inputs,
            "entry_sizes": sizes, "primary_entry_count": 1, "theme_count": len(THEMES),
            "published_reference_count": len(release["references"]),
            "profile_word_min": min(profile_sizes.values()),
            "profile_word_max": max(profile_sizes.values()),
            "local_markdown_links_checked": local_link_count,
            "required_image_fetches_for_core_reading": 0,
            "limits": ["Word counts are whitespace-based, not model tokens.",
                       "Local reachability and file budgets do not measure AI answer quality.",
                       "Supporting files remain available; primary reading is selective."]}


def returned_document_text(event):
    content = event["content"]
    if event.get("content_format") != "web_numbered_lines":
        return content
    numbered = re.findall(r"^L(\d+): ?(.*)$", content, flags=re.M)
    numbers = [int(n) for n, _ in numbered]
    if not numbers or numbers != list(range(0, numbers[-1] + 1)):
        raise ValueError("Source extraction has missing/reordered web lines")
    return "\n".join(line for _, line in numbered) + "\n"


def validate_remote_run(run, bank):
    if run.get("route") not in ("web", "github_connector"):
        raise ValueError("Unknown access route")
    if not re.fullmatch(r"[0-9a-f]{40}", run.get("commit", "")):
        raise ValueError("Remote run must pin one commit")
    if run.get("independent_model_evaluation") is not False or run.get("consumer_model_accuracy") is not None:
        raise ValueError("Observed access traces cannot claim independent model accuracy")
    events = {}
    for event in run["access_events"]:
        if event["id"] in events:
            raise ValueError("Duplicate access event")
        if event["commit"] != run["commit"] or event["route"] != run["route"]:
            raise ValueError("Mixed commit/route in access trace")
        if event["status"] not in ("read", "failed", "unsupported"):
            raise ValueError("Unknown access status")
        content = event.get("content", "")
        if event["status"] == "read":
            if not content:
                raise ValueError("Successful text read without returned content")
            if hashlib.sha256(content.encode()).hexdigest() != event["content_sha256"]:
                raise ValueError("Changed remote transcript content")
            if event["characters"] != len(content):
                raise ValueError("Incorrect remote character count")
        elif not event.get("reason"):
            raise ValueError("Failed access requires a reason")
        if event.get("annotation_text") and event["annotation_text"] != returned_document_text(event):
            raise ValueError("Parsed annotation differs from fetched text")
        events[event["id"]] = event
    manifest = events.get(run.get("release_evidence_event_id"))
    if not manifest or manifest["status"] != "read" or manifest["path"] != "knowledge/release.json":
        raise ValueError("Remote run must read its release manifest")
    # A web tool may return a prefix of a long manifest. Verify only the actual
    # returned release_id field; do not imply that all source bindings were read.
    manifest_text = returned_document_text(manifest)
    release_fields = re.findall(r'"release_id"\s*:\s*"([^"]+)"', manifest_text)
    if not manifest_text.lstrip().startswith("{") or release_fields != [run["release_id"]]:
        raise ValueError("Remote release differs from declared snapshot")
    cases = {c["id"]: c for c in bank["cases"]}
    results = []
    seen = set()
    for response in run["responses"]:
        case_id = response["case_id"]
        if case_id not in cases or case_id in seen:
            raise ValueError("Invalid or duplicate response case")
        seen.add(case_id)
        case = cases[case_id]
        citations = response.get("citations", [])
        evidence = []
        for cite in citations:
            event = events.get(cite["event_id"])
            if not event or event["status"] != "read":
                raise ValueError("Citation points to unread/failed content")
            if not cite["excerpt"] or cite["excerpt"] not in event["content"]:
                raise ValueError("Citation excerpt absent from fetched content")
            evidence.append(event)
        if response["status"] == "access_blocked":
            if response.get("answer") or citations:
                raise ValueError("Blocked read cannot contain a fabricated answer")
            passed = None
        elif response["status"] == "answered":
            if not evidence or not response.get("answer"):
                raise ValueError("Answered case requires actual remote evidence")
            passed = None
            if case["kind"] == "retrieval":
                found = response["reference_ids"]
                passed = set(case["expected_reference_ids"]) <= set(found)
                for ident in found:
                    if not any(ident in e["content"] or ident in e["path"] for e in evidence):
                        raise ValueError("Retrieved ID has no fetched evidence")
            elif case["kind"] == "source_value":
                matches = [e for e in evidence if e["path"] == f"references/{case['reference_id']}/analysis.yaml"
                           and e.get("annotation_text")]
                if matches:
                    actual = resolve_pointer(yaml.safe_load(matches[0]["annotation_text"]), case["field_path"])
                    passed = actual == case["expected"] == response["answer_value"]
                # A cited profile may support a manual answer but is not counted as parsed-source measurement.
        else:
            raise ValueError("Unknown response status")
        results.append({"case_id": case_id, "kind": case["kind"], "split": case["split"],
                        "status": response["status"], "mechanical_check_passed": passed,
                        "semantic_quality_score": None,
                        "measurement": ("guided_positive_example_access" if case["kind"] == "retrieval"
                                        else "parsed_remote_annotation_value" if case["kind"] == "source_value"
                                        else "same_assistant_semantic_answer_unscored")})
    if seen != set(cases):
        raise ValueError("Remote run must account for every frozen case, including blocked ones")
    successful = [e for e in events.values() if e["status"] == "read"]
    measured = [r for r in results if r["mechanical_check_passed"] is not None]
    return {"route": run["route"], "commit": run["commit"], "release_id": run["release_id"],
            "text_fetch_attempts": len(events), "successful_text_fetches": len(successful),
            "partial_text_fetches": sum(e.get("complete_document_returned") is False for e in successful),
            "manifest_check": "returned_release_id_field_only",
            "unique_paths_read": len({e["path"] for e in successful}),
            "characters_returned": sum(e["characters"] for e in successful),
            "answered_cases": sum(r["status"] == "answered" for r in results),
            "blocked_cases": sum(r["status"] == "access_blocked" for r in results),
            "mechanically_checked_cases": len(measured),
            "mechanical_checks_passed": sum(r["mechanical_check_passed"] for r in measured),
            "consumer_model_accuracy": None, "independent_model_evaluation": False,
            "visual_access": run["visual_access"], "search_access": run["search_access"],
            "context_isolation": run["context_isolation"], "cases": results,
            "limitations": run["limitations"]}


def remote_summary(root=ROOT):
    root = Path(root)
    bank = json.loads((root / "evaluations/stage3/cases.json").read_text())
    baseline = json.loads((root / "evaluations/stage3/baseline.json").read_text())
    bank_hash = sha256_file(root / "evaluations/stage3/cases.json")
    if baseline["question_bank_sha256"] != bank_hash:
        raise ValueError("Frozen question bank changed")
    folder = root / "evaluations/stage7"
    result = []
    for route in ("web", "github_connector"):
        path = folder / (route + ".json")
        if path.exists():
            captured = json.loads(path.read_text())
            if captured["question_bank_sha256"] != bank_hash:
                raise ValueError("Remote run used a different question bank")
            result.append(validate_remote_run(captured, bank))
    if len(result) == 2 and result[0]["commit"] != result[1]["commit"]:
        raise ValueError("Web and connector must use the same commit")
    return {"schema_version": "1.0", "runs": result,
            "both_routes_recorded": len(result) == 2,
            "consumer_model_accuracy": None,
            "measurement": "observed_route_access_and_mechanical_source_checks_not_blinded_model_accuracy"}


def run(root=ROOT, write=False):
    root = Path(root)
    outputs = {"evaluations/stage7/local-report.json": dump(audit(root)),
               "evaluations/stage7/remote-summary.json": dump(remote_summary(root))}
    for relative, content in outputs.items():
        path = root / relative
        if write:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        elif not path.is_file() or path.read_text() != content:
            raise ValueError("Stale access evaluation: " + relative)
    return json.loads(outputs["evaluations/stage7/local-report.json"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = run(args.root, args.write)
    print(f"{data['local_markdown_links_checked']} local links; "
          f"{data['published_reference_count']} profiles; reader budgets verified")


if __name__ == "__main__":
    main()
