#!/usr/bin/env python3
"""Regenerate the two checked-in synthetic ZIPs; never import into the library."""
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tests.fixtures.factory import copy_fixture, make_folder, package_folder
from homeku.common import dumps, read_json


def main():
    with tempfile.TemporaryDirectory() as name:
        work = Path(name)
        valid = make_folder(work / "valid", rid="fixture-valid")
        package_folder(valid, ROOT / "tests/fixtures/fixture-valid-r0001.zip")
        invalid = copy_fixture(work / "invalid", "fixture-invalid", valid)
        manifest = read_json(invalid / "manifest.json")
        manifest["media"][1]["sha256"] = "0" * 64
        (invalid / "manifest.json").write_text(dumps(manifest))
        package_folder(invalid, ROOT / "tests/fixtures/fixture-invalid-r0001.zip")
    print("Generated synthetic valid/invalid test ZIPs, not active references.")


if __name__ == "__main__":
    main()
