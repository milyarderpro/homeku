#!/usr/bin/env python3
"""Run one interactive import from Google Drive into a local HOMEKU library."""
import argparse
import os
from pathlib import Path
import re
import sys
from tempfile import TemporaryDirectory

from homeku.common import LibraryError, require


ROOT = Path(__file__).resolve().parents[1]


def config_dir():
    return Path.home() / ".config" / "homeku"


def drive_root_id(value):
    path = config_dir() / "drive-root.id"
    if value is None:
        try:
            value = path.read_text(encoding="utf-8").strip()
        except FileNotFoundError:
            raise LibraryError(f"Berikan ID folder HOMEKU dengan --drive-root atau HOMEKU_DRIVE_ROOT_ID, "
                               f"atau simpan ID di {path}.") from None
        except UnicodeError:
            raise LibraryError(f"Isi {path} dengan ID folder HOMEKU dalam teks UTF-8.") from None
    require(re.fullmatch(r"[A-Za-z0-9_-]+", value), "ID folder HOMEKU tidak valid. Gunakan ID dari tautan Drive.")
    return value


def parser():
    config = config_dir()
    cli = argparse.ArgumentParser(description="Pindai ZIP audit di Google Drive dan ingest satu batch lokal.")
    cli.add_argument("--root", type=Path, default=ROOT, help="Root pustaka lokal HOMEKU")
    cli.add_argument("--drive-root", default=os.getenv("HOMEKU_DRIVE_ROOT_ID"),
                     help="ID folder HOMEKU di Drive, HOMEKU_DRIVE_ROOT_ID, atau ~/.config/homeku/drive-root.id")
    cli.add_argument("--credentials", type=Path, default=config / "google-oauth-client.json",
                     help="JSON klien OAuth Desktop app di luar repo")
    cli.add_argument("--token", type=Path, default=config / "drive-token.json",
                     help="File token lokal di luar repo")
    cli.add_argument("--list", action="store_true", help="Lihat daftar tanpa ingest")
    return cli


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        drive_root = drive_root_id(args.drive_root)
        from homeku.audit_performance import safe_path
        from homeku.drive_client import connect
        from homeku.drive_ingest import inspect_batch, process_batch, report_batch

        root = args.root.resolve()
        require((root / "data/taxonomy.json").is_file(), "Pilih root pustaka HOMEKU dengan --root.")
        staging = safe_path(root / ".homeku/drive-ingest")
        staging.mkdir(parents=True, exist_ok=True, mode=0o700)
        with connect(args.credentials.expanduser(), args.token.expanduser(), root) as drive:
            with TemporaryDirectory(prefix="batch-", dir=staging) as temporary:
                work = Path(temporary)
                inventory, selected = inspect_batch(drive, root, drive_root, work, list_only=args.list, read=input)
                if selected:
                    print(f"Memproses {len(selected)} ZIP yang disetujui.")
                    return report_batch(process_batch(drive, inventory, selected, root, work))
        return 0
    except (LibraryError, OSError) as error:
        print(f"Gagal: {error}", file=sys.stderr)
        return 1
    except (EOFError, KeyboardInterrupt):
        print("\nDibatalkan.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
