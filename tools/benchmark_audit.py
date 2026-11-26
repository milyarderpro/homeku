#!/usr/bin/env python3
"""Measure equivalent fixture data and local tool stages in an isolated workspace."""
from __future__ import annotations
import argparse
import json
import platform
import subprocess
import sys
import time
from importlib.metadata import version
from pathlib import Path

from homeku import FORMAT_VERSION
from homeku.audit_session import add_frames, load_session, mark_viewed, workspace
from homeku.authoring import check_camera, complete, prepare, update_shot
from homeku.common import LibraryError, dumps, read_json, require
from homeku.derivations import fact_claims, referenced_frames
from homeku.exporter import draft, export, review
from homeku.motion_analysis import motion_hints
from homeku.preflight import check_inputs

import build_audit_kit


def benchmark(source, audit_path, audit_info, output, *, cuts=None, motion_shot=None):
    output = workspace(output)
    require(not output.exists() or not any(output.iterdir()), "Use an empty benchmark workspace")
    output.mkdir(parents=True, exist_ok=True)
    audit = read_json(audit_path)
    require(audit.get("schema_version") == FORMAT_VERSION and audit.get("revision") == 1,
            f"Use a complete format {FORMAT_VERSION} r0001 fixture")
    cuts = [] if cuts is None else cuts
    timings = {}

    def measure(name, function, *args, **kwargs):
        started = time.perf_counter()
        result = function(*args, **kwargs)
        timings[name] = round(time.perf_counter() - started, 6)
        return result

    writing = output / "writing"
    prepared = measure("prepare_cold", prepare, source, cuts, writing)
    resumed = measure("prepare_resume", prepare, source, cuts, writing, resume=True)
    selected = {i for item in resumed["passes"] for i in item["record"]["selected_frame_indices"]}
    extra = sorted(set(referenced_frames(audit)) - selected)
    session = Path(prepared["session"])
    if extra:
        add_frames(session, extra, reason="Referenced native fixture frames.")
    _, state, _ = load_session(session)
    available = {i for item in state["passes"] for i in item["record"]["selected_frame_indices"]}
    declared = {i for record in audit_info["frame_reviews"] for i in record["viewed_frame_indices"]}
    require(available <= declared,
            "Benchmark fixture must already declare the prepared and evidence frames as viewed")
    mark_viewed(session, all_frames=True, all_passes=True)
    work_audit, work_info = Path(prepared["audit"]), Path(prepared["audit_info"])
    work_audit.write_text(dumps(audit), encoding="utf-8")
    work_info.write_text(dumps(audit_info), encoding="utf-8")
    measure("check_camera", check_camera, session)
    measure("complete", complete, work_audit, session_path=session)
    authored, logs = read_json(work_audit), read_json(work_info)
    valid = measure("preflight", check_inputs, source, authored, logs, session_path=session, purpose="fixture")
    require(valid["ok"], "Fixture failed preflight: " + json.dumps(valid["errors"], ensure_ascii=False))
    render_paths = {"output_root": output / "candidate", "purpose": "fixture",
                    "cache_dir": output / "render-cache" / "frames", "session_path": session}
    cold = measure("draft_cold", draft, source, work_audit, logs, **render_paths)
    warm = measure("draft_warm", draft, source, work_audit, logs, **render_paths)
    require(cold["snapshot_sha256"] == warm["snapshot_sha256"], "Cold and warm draft bytes differ")
    folder = Path(warm["candidate"])
    original = read_json(folder / "manifest.json")
    cards = measure("review", review, folder, output / "review.md")
    packaged = measure("export", export, folder, output / "exports", cards["receipt"])
    size = {"audit_pretty_bytes": (folder / "audit.json").stat().st_size,
            "audit_compact_bytes": len(json.dumps(authored, ensure_ascii=False, separators=(",", ":")).encode()),
            "manifest_bytes": (folder / "manifest.json").stat().st_size,
            "report_bytes": (folder / "analysis.md").stat().st_size,
            "media_bytes": warm["media_bytes"], "zip_bytes": packaged["package_bytes"],
            "kit_bytes": len(build_audit_kit.build_bytes()), "kit_resources": len(build_audit_kit.BUNDLED)}
    size["audit_plus_manifest_bytes"] = size["audit_pretty_bytes"] + size["manifest_bytes"]
    size["package_payload_bytes"] = size["audit_plus_manifest_bytes"] + size["report_bytes"] + size["media_bytes"]

    shot = authored["shots"][0]
    phase = shot["camera"]["phases"][0]
    # Correct a camera target in a fixture, preserving phases, all design and all evidence.
    phases = [dict(p) for p in shot["camera"]["phases"]]
    phases[0]["notation"] = "Strong " + phase["notation"]
    patch = output / "correction.json"
    patch.write_text(dumps({"camera": {"phases": phases}}), encoding="utf-8")
    update_shot(session, shot["shot"], patch)
    measure("recheck_camera", check_camera, session, shot_id=shot["shot"])
    changed = measure("draft_correction", draft, source, work_audit, logs, **render_paths)
    corrected = read_json(folder / "manifest.json")
    previous_media = {row["path"]: row["sha256"] for row in original["media"]}
    changed_media = [row["path"] for row in corrected["media"] if previous_media[row["path"]] != row["sha256"]]

    native_shot = motion_shot or shot["shot"]
    hints = measure("helper_on_cold", motion_hints, session, native_shot)
    reused_hints = measure("helper_on_warm", motion_hints, session, native_shot)
    bad_input = read_json(work_audit)
    del bad_input["design"]["size"]["floor_area_m2"]
    negative = measure("invalid_preflight", check_inputs, source, bad_input, logs, purpose="fixture")
    require(not negative["ok"], "Invalid floor area must fail preflight")
    result = {"kind": "homeku.technical-benchmark", "format_version": FORMAT_VERSION,
              "scope": "Local runtime on synthetic fixture. No provider or pilot turnaround measurement.",
              "environment": {"python": platform.python_version(), "pillow": version("Pillow"),
                              "jsonschema": version("jsonschema"),
                              "ffmpeg": subprocess.run(["ffmpeg", "-version"], capture_output=True,
                                                       check=True, text=True).stdout.splitlines()[0],
                              "optional_backend": hints.get("backend")},
              "reference": authored["id"], "facts": sum(len(list(fact_claims(s, i)))
                                                       for i, s in enumerate(authored["shots"])),
              "shots": len(authored["shots"]), "sizes": size,
              "timings_seconds": timings, "cold_warm_byte_parity": True,
              "cache": {"prepare_cold": prepared["cache"], "prepare_resume": resumed["cache"],
                        "draft_cold": cold["cache"], "draft_warm": warm["cache"],
                        "draft_correction": changed["cache"]},
              "correction_media_changed": changed_media,
              "helper_off": {"invoked": False, "seconds": 0},
              "helper_on": {"cold": hints["status"], "warm": reused_hints["status"],
                            "warm_reused": reused_hints["reused"]},
              "invalid_preflight": negative["errors"]}
    (output / "benchmark.json").write_text(dumps(result), encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("audit", type=Path)
    parser.add_argument("--audit-info", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--cuts-file", type=Path)
    parser.add_argument("--motion-shot")
    args = parser.parse_args()
    try:
        result = benchmark(args.source, args.audit, read_json(args.audit_info), args.output,
                           cuts=read_json(args.cuts_file) if args.cuts_file else None,
                           motion_shot=args.motion_shot)
        print(dumps(result), end="")
        return 0
    except (LibraryError, OSError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
