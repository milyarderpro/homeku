#!/usr/bin/env python3
"""Generate current synthetic packages and their separate MP4s in an isolated folder."""
import argparse
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from homeku.audit_session import workspace
from homeku.common import LibraryError, require
from tests.fixtures.factory import isolated_root, make_package


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = workspace(args.output)
    require(root.resolve() != ROOT and (not root.exists() or not any(root.iterdir())),
            "Use an empty fixture output outside the library")
    isolated_root(root)
    with tempfile.TemporaryDirectory(prefix="homeku-test-packages-") as name:
        work = Path(name)
        for fixture in ("normal", "multi"):
            print(make_package(work / fixture, root, f"fixture-{fixture}", multi=fixture == "multi"))


if __name__ == "__main__":
    try:
        main()
    except (LibraryError, OSError) as error:
        raise SystemExit(str(error))
