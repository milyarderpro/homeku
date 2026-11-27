#!/usr/bin/env python3
"""Inspect, author, review and export an audit."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from homeku.audit_performance import PHASES, TRACKED_COMMANDS, mark_phase, summarize, timed
from homeku.common import LibraryError, read_json, require, sha256
from homeku.render_assets import DEFAULT_COLUMNS


def parser():
    cli = argparse.ArgumentParser(description="HOMEKU audit workflow")
    commands = cli.add_subparsers(dest="command", required=True)
    checking = commands.add_parser("readiness", help="Verify the MP4 and the required audit runtime")
    checking.add_argument("source", type=Path)
    checking.add_argument("--workspace", required=True, type=Path)
    inspecting = commands.add_parser("inspect", help="List native timestamps to confirm cuts")
    inspecting.add_argument("source", type=Path)
    inspecting.add_argument("--cut-preview", type=Path, metavar="WORKSPACE",
                            help="Write native frame pairs for suspected cuts")

    status = commands.add_parser("status", help="Show unviewed frames, incomplete pass declarations, camera and receipt checks")
    status.add_argument("session", type=Path)
    status.add_argument("--candidate", type=Path)
    status.add_argument("--receipt", type=Path)

    preparing = commands.add_parser("prepare", help="Prepare cuts, working files and baseline frames")
    preparing.add_argument("source", type=Path)
    preparing.add_argument("--cuts-file", required=True, type=Path, help="Native cut indices, [] for one take")
    preparing.add_argument("--output", required=True, type=Path)
    preparing.add_argument("--resume", action="store_true")

    sampling = commands.add_parser("sample", help="Inspect a specific interval or native frames")
    sampling.add_argument("--session", required=True, type=Path)
    targets = sampling.add_mutually_exclusive_group(required=True)
    targets.add_argument("--shot-id")
    targets.add_argument("--frames", nargs="+", type=int)
    sampling.add_argument("--reason", required=True)
    sampling.add_argument("--start", type=float)
    sampling.add_argument("--end", type=float)
    rate = sampling.add_mutually_exclusive_group()
    rate.add_argument("--fps", type=float)
    rate.add_argument("--native", action="store_true")

    viewing = commands.add_parser("mark-viewed", help="Declare which frames were inspected")
    viewing.add_argument("session", type=Path)
    passes = viewing.add_mutually_exclusive_group(required=True)
    passes.add_argument("--pass-id", nargs="+")
    passes.add_argument("--all-passes", action="store_true")
    selection = viewing.add_mutually_exclusive_group(required=True)
    selection.add_argument("--all", action="store_true")
    selection.add_argument("--frames", nargs="+", type=int)

    updating = commands.add_parser("update-shot", help="Apply a JSON patch to one working shot")
    updating.add_argument("session", type=Path)
    updating.add_argument("--shot-id", required=True)
    updating.add_argument("--patch", required=True, type=Path)
    editing = commands.add_parser("edit-record", help="Append or patch one phase or area fact in the working audit")
    editing.add_argument("session", type=Path)
    editing.add_argument("--shot-id", required=True)
    editing.add_argument("--kind", choices=("phase", "fact"), required=True)
    editing.add_argument("--patch", required=True, type=Path)
    editing.add_argument("--record-index", type=int, help="Zero-based entry index. Omit to append.")
    editing.add_argument("--expect-audit-sha256", help="SHA-256 of the working audit used to choose the index")
    editing.add_argument("--block-index", type=int, help="Zero-based shot design block for a fact")
    editing.add_argument("--category", choices=("architecture", "furnishings", "environment"))
    camera = commands.add_parser("check-camera", help="Verify camera findings before authoring design")
    camera.add_argument("session", type=Path)
    camera.add_argument("--shot-id", help="Recheck one deliberately corrected shot")

    completing = commands.add_parser("complete", help="Fill mechanical fields from the bound session")
    completing.add_argument("audit", type=Path)
    completing.add_argument("--session", required=True, type=Path)
    completing.add_argument("--audit-info", type=Path)

    check = commands.add_parser("check-input", help="Check independent input errors before rendering")
    drafting = commands.add_parser("draft", help="Render a candidate and keep its exact payload for review")
    for command in (check, drafting):
        command.add_argument("source", type=Path)
        command.add_argument("audit", type=Path)
        command.add_argument("--audit-info", required=True, type=Path)
        command.add_argument("--session", required=True, type=Path)
        command.add_argument("--supersedes", type=Path, help="Previous revision and content SHA-256 JSON")
    drafting.add_argument("--output", required=True, type=Path)
    drafting.add_argument("--cache-dir", type=Path)
    drafting.add_argument("--quality", type=int, default=91)
    drafting.add_argument("--scale", type=float, default=1)
    drafting.add_argument("--columns", type=int, default=DEFAULT_COLUMNS, help="Maximum columns for multi-area shots (default: %(default)s)")
    drafting.add_argument("--overview-scale", type=float, default=1)
    drafting.add_argument("--storyboard-scale", type=float, default=1)
    drafting.add_argument("--fixture", action="store_true", help="Mark synthetic test data")

    reviewing = commands.add_parser("review", help="Prepare the complete review and its snapshot receipt")
    reviewing.add_argument("candidate", type=Path)
    reviewing.add_argument("--output", required=True, type=Path)
    reviewing.add_argument("--source", type=Path, help="Optionally verify against the original MP4")
    exporting = commands.add_parser("export", help="Package the validated review snapshot unchanged")
    exporting.add_argument("candidate", type=Path)
    exporting.add_argument("--output", required=True, type=Path)
    exporting.add_argument("--receipt", required=True, type=Path, help="Snapshot receipt generated by the review command")
    for command in (reviewing, exporting):
        command.add_argument("--session", type=Path, help="Audit session for workspace performance logging")

    phase = commands.add_parser("phase", help="Record the start or finish of an audit phase")
    phase.add_argument("workspace", type=Path)
    phase.add_argument("phase", choices=PHASES)
    phase.add_argument("action", choices=("start", "finish"))
    performance = commands.add_parser("performance", help="Summarize phases and command attempts")
    performance.add_argument("workspace", type=Path)

    measuring = commands.add_parser("measure-anchor", help="Measure scale from two native pixel segments")
    measuring.add_argument("session", type=Path)
    measuring.add_argument("--shot-id", required=True)
    measuring.add_argument("--frames", required=True, nargs=2, type=int, metavar=("FIRST", "LAST"))
    measuring.add_argument("--start-points", required=True, nargs=4, type=float, metavar="PX")
    measuring.add_argument("--end-points", nargs=4, type=float, metavar="PX",
                           help="Confirm or correct the two native end points. Omit to request tracking.")
    measuring.add_argument("--output", required=True, type=Path, help="Workspace directory for the measurement")

    motion = commands.add_parser("motion-hints", help="Bounded tracking statistics")
    motion.add_argument("session", type=Path)
    motion.add_argument("--shot-id", required=True)
    motion.add_argument("--start", type=float)
    motion.add_argument("--end", type=float)
    motion.add_argument("--max-frames", type=int, default=32)
    motion.add_argument("--width", type=int, default=320)
    motion.add_argument("--details", action="store_true")
    return cli


def run(args, *, attempt=None):
    if args.command == "readiness":
        from homeku.audit_workflow import readiness
        return readiness(args.source, args.workspace)
    from homeku.audit_session import add_frames, add_pass, mark_viewed, workspace
    from homeku.authoring import check_camera, complete, edit_record, prepare, update_shot
    from homeku.exporter import draft, export, review
    from homeku.preflight import check_inputs
    from homeku.video import frame_times, probe_video
    command = args.command
    if command in {"phase", "performance"}:
        log = workspace(args.workspace / "performance.jsonl")
        if command == "phase":
            return mark_phase(log, args.phase, args.action)
        return summarize(log)
    if command == "inspect":
        info = probe_video(args.source)
        times = frame_times(args.source, info=info)
        digest = sha256(args.source)
        if args.cut_preview is not None:
            from homeku.audit_workflow import cut_preview
            return {"source_sha256": digest, "source": info, "frame_count": len(times),
                    "cut_candidates": cut_preview(args.source, info, times, digest, args.cut_preview)}
        return {"source_sha256": digest, "source": info,
                "frame_count": len(times), "frame_timestamps_s": times}
    if command == "status":
        from homeku.audit_workflow import session_status
        return session_status(args.session, candidate=args.candidate, receipt=args.receipt)
    if command == "prepare":
        return prepare(args.source, read_json(args.cuts_file), args.output, resume=args.resume)
    if command == "sample":
        if args.frames:
            require(args.start is None and args.end is None and args.fps is None and not args.native,
                    "Exact frame indices do not take interval or sampling flags")
            return add_frames(args.session, args.frames, reason=args.reason)
        return add_pass(args.session, args.shot_id, start=args.start, end=args.end,
                        fps=10 if args.fps is None else args.fps, native=args.native, reason=args.reason)
    if command == "mark-viewed":
        return mark_viewed(args.session, args.pass_id, args.frames,
                           all_frames=args.all, all_passes=args.all_passes)
    if command == "update-shot":
        return update_shot(args.session, args.shot_id, args.patch)
    if command == "edit-record":
        return edit_record(args.session, args.shot_id, args.kind, args.patch, record_index=args.record_index,
                           block_index=args.block_index, category=args.category,
                           expected_audit_sha256=args.expect_audit_sha256)
    if command == "check-camera":
        return check_camera(args.session, shot_id=args.shot_id)
    if command == "complete":
        return complete(args.audit, session_path=args.session, info_path=args.audit_info)
    if command in {"check-input", "draft"}:
        info = read_json(args.audit_info)
        supersedes = read_json(args.supersedes) if args.supersedes else None
        if command == "check-input":
            result = check_inputs(args.source, read_json(args.audit), info, session_path=args.session,
                                  supersedes=supersedes)
            result.pop("context")
            return result
        return draft(args.source, args.audit, info, args.output, session_path=args.session, supersedes=supersedes,
                     purpose="fixture" if args.fixture else "reference", cache_dir=args.cache_dir,
                     quality=args.quality, scale=args.scale, columns=args.columns,
                     overview_scale=args.overview_scale, storyboard_scale=args.storyboard_scale)
    if command == "review":
        return review(args.candidate, args.output, args.source, attempt=attempt, session_path=args.session)
    if command == "export":
        return export(args.candidate, args.output, args.receipt, attempt=attempt)
    if command == "measure-anchor":
        from homeku.camera_anchor import measure_anchor
        return measure_anchor(args.session, args.shot_id, args.frames, args.start_points,
                              args.end_points, args.output)
    from homeku.motion_analysis import motion_hints
    return motion_hints(args.session, args.shot_id, start=args.start, end=args.end,
                        max_frames=args.max_frames, width=args.width, details=args.details)


def run_with_performance(args):
    if args.command not in TRACKED_COMMANDS or args.session is None:
        return run(args)
    from homeku.audit_session import workspace

    session_path = workspace(args.session)
    if args.command == "export":
        from homeku.exporter import export_session_path
        session_path = export_session_path(args.candidate, args.receipt, session_path)
    log = session_path.parent / "performance.jsonl"
    shot = getattr(args, "shot_id", None)
    with timed(log, args.command, **({"shot": shot} if shot else {})) as attempt:
        result = run(args, attempt=attempt)
        if args.command == "check-input" and not result["ok"]:
            attempt.update(state="failed", error="; ".join(
                f"{row['path']}: {row['message']}" for row in result["errors"]))
        if "snapshot_sha256" in result:
            attempt["snapshot_sha256"] = result["snapshot_sha256"]
        return result


def main():
    args = parser().parse_args()
    try:
        result = run_with_performance(args)
        if args.command in {"prepare", "sample"}:
            result["passes"] = [{"id": item["id"], "shot": item["record"]["shot_id"],
                                 "mode": item["record"]["mode"], "sheets": item["sheets"],
                                 "selected": len(item["record"]["selected_frame_indices"]),
                                 "viewed": len(item["record"]["viewed_frame_indices"])}
                                for item in result["passes"]]
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if args.command in {"check-input", "readiness"} and not result["ok"] else 0
    except (LibraryError, OSError) as error:
        print(json.dumps({"status": "failed", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
