#!/usr/bin/env python3
"""Portable helper used inside a chat's code workspace; never calls an AI API."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from homeku.common import LibraryError, read_json, sha256
from homeku.exporter import assemble, frame_times, sample
from homeku.validation import probe_video, validate_folder
from homeku.markdown import review_cards


def main():
    parser = argparse.ArgumentParser(description="Inspect source, sample evidence, and assemble a HOMEKU ZIP")
    commands = parser.add_subparsers(dest="command", required=True)
    inspecting = commands.add_parser("inspect")
    inspecting.add_argument("source", type=Path)
    sampling = commands.add_parser("sample")
    sampling.add_argument("source", type=Path)
    sampling.add_argument("--output", required=True, type=Path)
    sampling.add_argument("--fps", type=float, default=10)
    sampling.add_argument("--start", type=float, default=0)
    sampling.add_argument("--end", type=float)
    sampling.add_argument("--native", action="store_true", help="All original frames in the interval, no forced 30 FPS")
    sampling.add_argument("--shot-id")
    sampling.add_argument("--reason")
    review = commands.add_parser("review")
    review.add_argument("candidate", type=Path)
    review.add_argument("--output", required=True, type=Path)
    review.add_argument("--source", type=Path, help="Canonical MP4 if the candidate omits source.mp4")
    for name in ("draft", "export"):
        command = commands.add_parser(name)
        command.add_argument("source", type=Path)
        command.add_argument("analysis", type=Path)
        command.add_argument("--audit-info", required=True, type=Path)
        command.add_argument("--output", required=True, type=Path)
        command.add_argument("--extras", type=Path)
        command.add_argument("--supersedes", type=Path)
        command.add_argument("--include-source", action="store_true")
        if name == "export":
            command.add_argument("--reviewed-sha256", required=True)
    args = parser.parse_args()
    try:
        if args.command == "review":
            candidate = args.candidate.resolve()
            override = {candidate.name: args.source.resolve()} if args.source else None
            snapshot_hash = sha256(candidate / "analysis.md")
            _, model, _ = validate_folder(candidate, candidate.parent, source_overrides=override)
            if sha256(candidate / "analysis.md") != snapshot_hash:
                raise LibraryError("Analysis changed during review generation; regenerate cards")
            output_path = args.output.resolve()
            if output_path.is_relative_to(candidate):
                raise LibraryError("Keep review cards outside the candidate package")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(review_cards(model, snapshot_hash, media_prefix=candidate.as_posix()), encoding="utf-8")
            print(json.dumps({"review": str(output_path), "analysis_sha256": snapshot_hash}, indent=2))
            return 0
        source = args.source.resolve()
        if args.command == "inspect":
            times = frame_times(source)
            result = {"source_sha256": sha256(source), "source": probe_video(source), "frame_count": len(times), "frame_timestamps_s": times}
        elif args.command == "sample":
            result = sample(source, args.output.resolve(), args.fps, args.start, args.end, native=args.native, shot_id=args.shot_id, reason=args.reason)
        else:
            result = assemble(source, args.analysis.resolve(), read_json(args.audit_info), args.output.resolve(),
                              extras=read_json(args.extras) if args.extras else None,
                              supersedes=read_json(args.supersedes) if args.supersedes else None,
                              include_source=args.include_source, reviewed_sha256=getattr(args, "reviewed_sha256", None))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (LibraryError, OSError) as error:
        print(json.dumps({"status": "failed", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
