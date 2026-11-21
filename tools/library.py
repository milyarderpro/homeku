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
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        if args.command == "validate":
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
