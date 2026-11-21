"""Validate and package the home-productions skills-only source for private release.

Development plans, tests and runs live outside the plugin directory. No network
or account writes happen here. Upload the inspected archive with Plugin Creator.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

import yaml

WORKSPACE = Path(__file__).resolve().parents[1]
PLUGIN = WORKSPACE / "home-productions"
SEMVER = r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?"


def inspect_source(source):
    source = Path(source).resolve()
    files = {}
    for path in sorted(source.rglob("*")):
        relative = path.relative_to(source)
        if path.is_symlink():
            raise ValueError("Symlinks are not packaged: " + str(relative))
        if any(part.startswith(".") or part in {"__pycache__", "node_modules", "dist", "runs", "tests"}
               for part in relative.parts):
            raise ValueError("Unexpected development/private path: " + str(relative))
        if path.is_dir():
            continue
        if not path.is_file():
            raise ValueError("Only regular files may be packaged: " + str(relative))
        if relative.as_posix() != "plugin.json" and relative.parts[0] not in {"skills", "assets"}:
            raise ValueError("Unexpected plugin-root component: " + str(relative))
        raw = path.read_bytes()
        files[relative.as_posix()] = raw
        if path.suffix in {".json", ".yaml", ".yml", ".md", ".py", ".txt"}:
            text = raw.decode("utf-8")
            if path.suffix == ".json":
                json.loads(text)
            elif path.suffix in {".yaml", ".yml"}:
                yaml.safe_load(text)
            elif path.suffix == ".py":
                ast.parse(text, filename=str(relative))
    if "plugin.json" not in files:
        raise ValueError("Root plugin.json is missing.")
    manifest = json.loads(files["plugin.json"])
    if manifest.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
        raise ValueError("Agent Plugins 1.0 schema declaration is required.")
    if manifest.get("name") != source.name:
        raise ValueError("Package folder and manifest name must match.")
    if not re.fullmatch(SEMVER, manifest.get("version", "")):
        raise ValueError("Manifest version must use semantic versioning.")
    if {"skills", "mcpServers", "apps", "interface"} & manifest.keys():
        raise ValueError("Portable manifest must not contain legacy component fields.")
    ui = manifest["extensions"]["com.openai"]["interface"]
    if not isinstance(ui.get("shortDescription"), str) or not 0 < len(ui["shortDescription"].strip()) <= 30:
        raise ValueError("Listing shortDescription must contain 1–30 characters.")
    if ui.get("category") != "Creativity":
        raise ValueError("This plugin's agreed listing category is Creativity.")
    skills = []
    for name, raw in files.items():
        path = Path(name)
        if path.name == "SKILL.md":
            if len(path.parts) != 3 or path.parts[0] != "skills":
                raise ValueError("Portable skill must be directly under skills/<name>/SKILL.md.")
            text = raw.decode("utf-8")
            if not text.startswith("---\n") or len(text.split("---", 2)) != 3:
                raise ValueError("Skill frontmatter is missing: " + name)
            metadata = yaml.safe_load(text.split("---", 2)[1])
            if not isinstance(metadata, dict) or metadata.get("name") != path.parent.name:
                raise ValueError("Skill name must match its folder: " + name)
            if not isinstance(metadata.get("description"), str) or not metadata["description"].strip():
                raise ValueError("Skill description is missing: " + name)
            if len(raw) > 1024 * 1024:
                raise ValueError("Skill exceeds the 1 MiB component limit.")
            skills.append(metadata["name"])
        if path.suffix == ".md":
            for href in re.findall(r"\[[^\]]*\]\(([^)]+)\)", raw.decode("utf-8")):
                url = urlsplit(href)
                if url.scheme or not url.path:
                    continue
                target = (source / path.parent / unquote(url.path)).resolve()
                if not target.is_relative_to(source) or target.relative_to(source).as_posix() not in files:
                    raise ValueError("Missing or escaping packaged reference: " + name + " -> " + href)
    if not skills or len(skills) != len(set(skills)):
        raise ValueError("Package needs at least one uniquely named skill.")
    for asset_field in ("logo", "composerIcon", "logoDark", "composerIconDark"):
        if asset_field in ui:
            target = (source / ui[asset_field]).resolve()
            if not target.is_relative_to(source) or target.relative_to(source).as_posix() not in files:
                raise ValueError("Referenced listing asset is missing: " + asset_field)
    return manifest, sorted(skills), files


def build_archive(source, output):
    source, output = Path(source).resolve(), Path(output).resolve()
    if output.is_relative_to(source):
        raise ValueError("Write the release archive outside the plugin directory.")
    manifest, skills, files = inspect_source(source)
    if output.exists():
        raise FileExistsError("Release archive already exists; it will not be overwritten.")
    output.parent.mkdir(parents=True, exist_ok=True)
    created = False
    try:
        with ZipFile(output, "x", compression=ZIP_DEFLATED) as archive:
            created = True
            for name, raw in files.items():
                info = ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                info.compress_type = ZIP_DEFLATED
                archive.writestr(info, raw)
        with ZipFile(output) as archive:
            if archive.testzip() is not None or archive.namelist() != list(files):
                raise ValueError("Release archive inventory or CRC is invalid.")
            if any(archive.read(name) != raw for name, raw in files.items()):
                raise ValueError("Archive differs from the inspected source.")
    except Exception:
        if created:
            output.unlink(missing_ok=True)
        raise
    return {
        "archive": str(output), "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "version": manifest["version"], "file_count": len(files), "skills": skills,
        "files": list(files),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = build_archive(PLUGIN, args.output)
    except (OSError, ValueError) as error:
        parser.exit(1, str(error) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
