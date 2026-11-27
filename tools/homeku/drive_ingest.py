"""Discover and ingest approved Drive audit packages in one local invocation."""
from collections import Counter
from dataclasses import dataclass, replace
import os
from pathlib import Path, PurePosixPath
import re
from tempfile import mkdtemp, TemporaryDirectory

from .audit_performance import safe_path
from .common import LibraryError, read_json, require, schema_check, sha256, snapshot_hash
from .drive_client import DriveItem, FOLDER
from .engine import fixture_allowed, ingest, registry_at
from .storage import locked
from .validation import MAX_TOTAL, extract_package


PACKAGE_NAME = re.compile(r"([A-Za-z0-9][A-Za-z0-9_-]{0,79})-r([0-9]{4})\.zip")
ZIP_TYPES = {"application/zip", "application/x-zip-compressed", "application/octet-stream"}


@dataclass(frozen=True)
class Package:
    file: DriveItem
    folder: DriveItem
    id: str
    revision: int


@dataclass(frozen=True)
class Inventory:
    audit: DriveItem
    video_folders: tuple[DriveItem, ...]
    packages: tuple[Package, ...]
    folder_counts: Counter


def _folders(children, name):
    return tuple(item for item in children if item.name == name and item.mime == FOLDER)


def scan(drive, root_id):
    root = drive.metadata(root_id)
    require(root.id == root_id and root.mime == FOLDER and not root.trashed,
            "Root HOMEKU harus berupa folder Drive yang aktif.")
    children = drive.children(root_id)
    audit_folders = _folders(children, "Audit")
    require(len(audit_folders) == 1, "Root HOMEKU harus memiliki satu folder Audit yang dapat dipastikan.")
    audit = audit_folders[0]
    folders = [item for item in drive.children(audit.id) if item.mime == FOLDER]
    packages = []
    for folder in folders:
        for item in drive.children(folder.id):
            match = PACKAGE_NAME.fullmatch(item.name)
            if match and item.mime in ZIP_TYPES and int(match[2]) > 0:
                packages.append(Package(item, folder, match[1], int(match[2])))
    packages.sort(key=lambda pkg: (pkg.id.casefold(), pkg.revision, pkg.folder.name, pkg.file.id))
    return Inventory(audit, _folders(children, "Video"), tuple(packages),
                     Counter(folder.name.casefold() for folder in folders))


@dataclass(frozen=True)
class Entry:
    package: Package
    status: str
    digest: str | None = None
    reason: str = ""
    predecessors: tuple[int, ...] = ()


def library_history(root):
    with locked(root, recovery=False):
        references = registry_at(root)["references"]
        ledger_path = safe_path(root / "data/ingest.json")
        ledger = read_json(ledger_path) if ledger_path.exists() else {"version": 1, "packages": {}}
        require(isinstance(ledger, dict) and ledger.get("version") == 1 and
                isinstance(ledger.get("packages"), dict), "Riwayat ingest lokal tidak valid.")
    return references, ledger["packages"]


def _inspect_zip(drive, package, work):
    with TemporaryDirectory(prefix="inspect-", dir=work) as scratch:
        path = Path(scratch) / package.file.name
        digest = drive.download(package.file, path, limit=MAX_TOTAL)
        require(package.file.sha256 in (None, digest), "SHA-256 ZIP berubah saat daftar dipindai.")
        unpacked = extract_package(path, path.parent / "unpacked")
        return digest, snapshot_hash(unpacked)


def classify(drive, inventory, references, ledger, work):
    ids = set(references) | {package.id for package in inventory.packages}
    casing = Counter(ref_id.casefold() for ref_id in ids)
    versions = Counter((pkg.id, pkg.revision) for pkg in inventory.packages)
    entries = []
    for package in inventory.packages:
        try:
            entry = _classify_package(drive, inventory, package, references.get(package.id), ledger,
                                      casing, versions, work)
        except (LibraryError, OSError) as error:
            entry = Entry(package, "blocked", reason=str(error))
        entries.append(entry)

    candidates = {(row.package.id, row.package.revision) for row in entries if row.status == "ready"}
    for index, entry in enumerate(entries):
        if entry.status != "ready":
            continue
        package = entry.package
        active = references.get(package.id, {}).get("revision", 0)
        predecessors = tuple(range(active + 1, package.revision))
        missing = next((revision for revision in predecessors if (package.id, revision) not in candidates), None)
        if missing is not None:
            entries[index] = replace(entry, status="blocked", reason=f"Perlu r{missing:04d} yang dapat dipilih.")
        elif predecessors:
            entries[index] = replace(entry, predecessors=predecessors)
    return entries


def _classify_package(drive, inventory, package, active, ledger, casing, versions, work):
    digest = package.file.sha256
    content = None
    if digest is None:
        digest, content = _inspect_zip(drive, package, work)
    prior = ledger.get(digest)
    if (isinstance(prior, dict) and prior.get("status") == "imported" and
            prior.get("package") == package.file.name and prior.get("id") == package.id and
            prior.get("revision") == package.revision):
        return Entry(package, "imported", digest)
    if active and package.revision == active["revision"]:
        if digest == active["package_sha256"]:
            return Entry(package, "imported", digest)
        if content is None:
            _, content = _inspect_zip(drive, package, work)
        if content == active["content_sha256"]:
            return Entry(package, "imported", digest)
        return Entry(package, "conflict", digest, "Isi ZIP berbeda pada nomor revisi aktif.")
    if active and package.revision < active["revision"]:
        return Entry(package, "blocked", digest, "Revisi lebih lama daripada referensi aktif.")
    if (versions[package.id, package.revision] > 1 or casing[package.id.casefold()] > 1 or
            inventory.folder_counts[package.folder.name.casefold()] > 1):
        return Entry(package, "conflict", digest, "Nama folder, ID audit, atau nomor revisi bertabrakan di inventaris.")
    if package.file.size is not None and package.file.size > MAX_TOTAL:
        return Entry(package, "blocked", digest, "ZIP melebihi batas ukuran paket.")
    return Entry(package, "ready", digest)


STATUS_LABELS = {
    "imported": "sudah masuk",
    "ready": "dapat dipilih",
    "conflict": "konflik",
    "blocked": "tertunda",
}


def inspect_batch(drive, root, drive_root, staging, *, list_only=False, read=input, emit=print):
    inventory = scan(drive, drive_root)
    references, ledger = library_history(root)
    entries = classify(drive, inventory, references, ledger, staging)
    candidates = [row for row in entries if row.status == "ready"]
    numbers = {row.package.file.id: number for number, row in enumerate(candidates, 1)}
    counts = Counter(entry.status for entry in entries)
    emit(f"{len(entries)} ZIP ditemukan. {counts['imported']} sudah masuk, {counts['ready']} dapat dipilih, "
         f"{counts['conflict']} konflik, {counts['blocked']} tertunda.")
    for entry in entries:
        package = entry.package
        heading = f"HOMEKU/Audit/{package.folder.name!r}/{package.file.name}"
        if entry.status == "ready":
            number = numbers[package.file.id]
            emit(f"  {number}. {heading} ({STATUS_LABELS[entry.status]})")
            emit(f"     Drive {package.file.id} | SHA-256 {entry.digest}")
            if entry.predecessors:
                names = ", ".join(f"r{revision:04d}" for revision in entry.predecessors)
                emit(f"     Pilih juga revisi pendahulu {names}.")
        else:
            reason = f" — {entry.reason}" if entry.reason else ""
            emit(f"  {heading} ({STATUS_LABELS[entry.status]}){reason}")

    if list_only or not candidates:
        return inventory, ()
    choice = read("Pilih nomor dipisah koma, ketik 'semua', atau Enter untuk batal: ").strip().casefold()
    if not choice:
        return inventory, ()
    if choice == "semua":
        selected = tuple(candidates)
    else:
        try:
            indices = {int(value.strip()) for value in choice.split(",")}
        except ValueError:
            raise LibraryError("Pilihan tidak valid. Masukkan nomor dipisah koma atau 'semua'.") from None
        require(all(1 <= number <= len(candidates) for number in indices), "Nomor pilihan di luar daftar.")
        selected = tuple(candidates[number - 1] for number in sorted(indices))

    chosen = {(entry.package.id, entry.package.revision) for entry in selected}
    for entry in selected:
        for revision in entry.predecessors:
            require((entry.package.id, revision) in chosen,
                    f"Pilih {entry.package.id}-r{revision:04d} sebelum menyetujui {entry.package.file.name}.")
    names = ", ".join(entry.package.file.name for entry in selected)
    approved = read(f"Ingest {len(selected)} ZIP ({names})? Ketik 'ya' untuk menyetujui: ").strip().casefold()
    return inventory, selected if approved == "ya" else ()


def _same_location(current, original):
    return (not current.trashed and current.id == original.id and current.name == original.name and
            current.mime == original.mime and current.parents == original.parents)


def _approved_file(drive, inventory, entry):
    package = entry.package
    current = drive.metadata(package.file.id)
    require(_same_location(drive.metadata(inventory.audit.id), inventory.audit) and
            _same_location(drive.metadata(package.folder.id), package.folder) and
            _same_location(current, package.file) and current.sha256 in (None, entry.digest),
            "ZIP atau lokasi Drive berubah. Pindai ulang dan setujui snapshot terbaru.")
    return current


def stage_zip(drive, inventory, entry, staging):
    require(entry.status == "ready" and entry.digest is not None, "ZIP ini belum siap untuk diproses.")
    current = _approved_file(drive, inventory, entry)
    directory = Path(mkdtemp(prefix="approved-", dir=staging))
    path = directory / entry.package.file.name
    try:
        digest = drive.download(current, path, limit=MAX_TOTAL)
        require(digest == entry.digest, "SHA-256 ZIP berbeda dari yang disetujui. Pindai ulang.")
        _approved_file(drive, inventory, entry)
    except (LibraryError, OSError, KeyboardInterrupt):
        path.unlink(missing_ok=True)
        directory.rmdir()
        raise
    return path


def package_source(root, package, archive):
    with TemporaryDirectory(prefix="manifest-", dir=archive.parent) as scratch:
        extracted = extract_package(archive, Path(scratch) / "unpacked")
        manifest = schema_check(read_json(extracted / "manifest.json"), "manifest.schema.json")
        require(manifest["id"] == package.id and manifest["revision"] == package.revision and
                manifest["source"]["path"] == f"video/{package.id}.mp4",
                "Identitas atau jalur sumber di manifest berbeda dari nama paket.")
        fixture_allowed(root, manifest)
        return manifest["source"]["sha256"]


def _local_source(root, package, digest):
    active = registry_at(root)["references"].get(package.id)
    require(active is None or active["source_sha256"] == digest,
            "SHA-256 MP4 paket berbeda dari sumber referensi aktif.")
    path = safe_path(root / "video" / f"{package.id}.mp4")
    if path.parent.exists():
        require(path.parent.is_dir(), "Jalur video lokal bukan direktori.")
        require(not any(other.name.casefold() == path.name.casefold() and other.name != path.name
                        for other in path.parent.iterdir()), "Nama MP4 kanonis bertabrakan di folder video lokal.")
    if path.exists():
        require(path.is_file() and sha256(path) == digest,
                "MP4 kanonis lokal berbeda dari SHA-256 di manifest.")
    return path


def _source_candidates(drive, inventory, package):
    require(len(inventory.video_folders) == 1, "Folder Video di root HOMEKU hilang atau ambigu.")
    folder = inventory.video_folders[0]
    require(_same_location(drive.metadata(folder.id), folder), "Lokasi folder Video di Drive berubah.")
    return [item for item in drive.children(folder.id)
            if item.mime in {"video/mp4", "application/octet-stream"} and
            (name := PurePosixPath(item.name)).name == item.name and
            name.stem == package.folder.name and name.suffix.lower() == ".mp4"]


def ensure_source(drive, inventory, package, root, digest, staging):
    with locked(root, recovery=False):
        path = _local_source(root, package, digest)
        if path.is_file():
            return path
    candidates = _source_candidates(drive, inventory, package)
    require(candidates, f"MP4 untuk {package.folder.name!r} tidak ditemukan di HOMEKU/Video.")
    with TemporaryDirectory(prefix="source-", dir=staging) as scratch:
        verified = None
        for index, item in enumerate(candidates):
            if item.sha256 not in (None, digest):
                continue
            current = drive.metadata(item.id)
            require(_same_location(current, item), "Lokasi MP4 di Drive berubah saat akan diunduh.")
            if current.sha256 not in (None, digest):
                continue
            destination = Path(scratch) / f"{index}.mp4"
            if drive.download(current, destination) == digest:
                require(verified is None, "Lebih dari satu MP4 di Drive cocok dengan SHA-256 sumber.")
                verified = destination
            else:
                destination.unlink()
        require(verified is not None, "SHA-256 semua MP4 yang ditemukan berbeda dari manifest.")
        with locked(root):
            path = _local_source(root, package, digest)
            if not path.is_file():
                path.parent.mkdir(parents=True, exist_ok=True)
                os.link(verified, path)
        return path


def process_batch(drive, inventory, selected, root, staging):
    paths = {}
    results = {}
    for entry in sorted(selected, key=lambda row: (row.package.id, row.package.revision)):
        package = entry.package
        name = package.file.name
        try:
            for revision in entry.predecessors:
                require(f"{package.id}-r{revision:04d}.zip" in paths,
                        f"Menunggu {package.id}-r{revision:04d}.zip yang terverifikasi.")
            path = stage_zip(drive, inventory, entry, staging)
            digest = package_source(root, package, path)
            ensure_source(drive, inventory, package, root, digest, staging)
            paths[name] = path
        except (LibraryError, OSError) as error:
            results[name] = {"package": name, "status": "pending", "error": str(error)}

    if paths:
        results.update((row["package"], row) for row in ingest(root, list(paths.values()))["results"])
    for entry in selected:
        package = entry.package
        row = results[package.file.name]
        if row["status"] == "failed":
            waiting = next((f"{package.id}-r{revision:04d}.zip" for revision in entry.predecessors
                            if results[f"{package.id}-r{revision:04d}.zip"]["status"] in ("failed", "pending")), None)
            if waiting:
                row.update(status="pending", error=f"Menunggu {waiting}. {row['error']}")
    return [results[entry.package.file.name] for entry in selected]


RESULT_LABELS = {
    "imported": "berhasil",
    "unchanged": "sudah masuk",
    "pending": "tertunda",
    "failed": "gagal",
}


def report_batch(rows, emit=print):
    counts = Counter(row["status"] for row in rows)
    emit(f"Batch selesai. {counts['imported']} berhasil, {counts['unchanged']} sudah masuk, "
         f"{counts['pending']} tertunda, {counts['failed']} gagal.")
    for row in rows:
        reason = f" — {row['error']}" if "error" in row else ""
        emit(f"  {row['package']} ({RESULT_LABELS[row['status']]}){reason}")
    return int(bool(counts["pending"] or counts["failed"]))
