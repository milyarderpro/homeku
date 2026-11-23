#!/usr/bin/env python3
"""HOMEKU library CLI. Run from any directory, Python 3.11+ and ffprobe required."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from homeku.common import LibraryError
from homeku.engine import build, check, ingest, validate_package
from homeku.storage import locked
from homeku.reader import search, read_reference, extract_panel, extract_shot_image


def main():
    parser = argparse.ArgumentParser(description="Validate, ingest and build the HOMEKU reference library")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate", help="Check one ZIP without publishing it")
    validate.add_argument("package", type=Path)
    importing = commands.add_parser("ingest", help="Import specified ZIPs, or scan every ZIP in incoming/")
    importing.add_argument("packages", nargs="*", type=Path)
    building = commands.add_parser("build", help="Rebuild catalogs and knowledge from registered audits")
    building.add_argument("--full", action="store_true", help="Bypass disposable projection caches")
    commands.add_parser("check", help="Validate all active sources and compare a full rebuild")
    commands.add_parser("recover", help="Recover an interrupted local publication")
    finding=commands.add_parser("search",help="Bounded search of explicit source facets")
    finding.add_argument("--style")
    finding.add_argument("--style-role",choices=["primary-style","style-influence","interior-style"],default="primary-style")
    finding.add_argument("--style-relation",choices=["family","blend","influence"])
    finding.add_argument("--scale")
    finding.add_argument("--area",action="append")
    finding.add_argument("--configuration")
    finding.add_argument("--tempo",choices=["slow","moderate","fast","unknown"])
    finding.add_argument("--route",nargs="+")
    finding.add_argument("--limit",type=int,default=10)
    finding.add_argument("--offset",type=int,default=0)
    finding.add_argument("--observed-only",action="store_true")
    reading=commands.add_parser("read",help="Read identity or one shot/area with continuity context")
    reading.add_argument("id")
    reading.add_argument("--part",choices=["identity","shot","area","full"],default="identity")
    reading.add_argument("--shot")
    reading.add_argument("--area")
    panel=commands.add_parser("panel",help="Extract one photograph temporarily without captions")
    panel.add_argument("id")
    panel.add_argument("selection_id")
    panel.add_argument("--output",type=Path,required=True)
    panel.add_argument("--native",action="store_true")
    shot_image=commands.add_parser("shot-image",help="Extract a stored shot collage or full Storyboard block without MP4")
    shot_image.add_argument("id")
    shot_image.add_argument("shot")
    shot_image.add_argument("--output",type=Path,required=True)
    shot_image.add_argument("--from-storyboard",action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        if args.command == "search":
            with locked(root,recovery=False):
                result=search(root,style=args.style,style_role=args.style_role,style_relation=args.style_relation,scale=args.scale,
                    area=args.area,configuration=args.configuration,tempo=args.tempo,route=args.route,limit=args.limit,offset=args.offset,include_uncertain=not args.observed_only)
        elif args.command == "read":
            with locked(root,recovery=False):
                result=read_reference(root,args.id,part=args.part,shot=args.shot,area=args.area)
        elif args.command == "panel":
            with locked(root,recovery=False):
                result=extract_panel(root,args.id,args.selection_id,args.output.resolve(),native=args.native)
        elif args.command == "shot-image":
            with locked(root,recovery=False):
                result=extract_shot_image(root,args.id,args.shot,args.output.resolve(),from_storyboard=args.from_storyboard)
        elif args.command == "validate":
            result = validate_package(root, args.package.resolve())
        elif args.command == "ingest":
            result = ingest(root, [p.resolve() for p in args.packages] if args.packages else None)
        elif args.command == "build":
            result = build(root, args.full)
        elif args.command == "check":
            result = check(root)
        else:
            with locked(root):
                result = {"status": "recovered"}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if args.command == "ingest" and any(r["status"] == "failed" for r in result["results"]):
            return 1
        return 0
    except (LibraryError, OSError) as error:
        print(json.dumps({"status": "failed", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
