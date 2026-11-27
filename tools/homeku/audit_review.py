"""Workspace-only review checklist derived from validated candidate files."""
from urllib.parse import quote

from .derivations import claims, tempo_segments
from .report_validation import display, inline


def _link(label, path):
    return f"[{label}](<{quote(path.as_posix(), safe='/:')}>)"


def _inline_caption(value):
    return inline(" ".join(value.splitlines())).replace("&", r"\&").replace("~", r"\~")


def checklist(candidate, report, audit, manifest, digest, *, source_verified=False, changes=()):
    links = [
        _link("Laporan lengkap", report),
        _link("Overview", candidate / "media/overview.jpg"),
        _link("Storyboard", candidate / "media/storyboard.jpg"),
    ]
    rows = ["# Lembar pemeriksaan kandidat", f"**{audit['id']} · r{audit['revision']:04d}**",
            f"Snapshot SHA-256 `{digest}`", " · ".join(links), "## Pemeriksaan teknis",
            "- Paket, laporan hasil renderer, hash media, dan referensi bukti pada manifest lulus validasi."]
    if source_verified:
        rows.append("- Metadata MP4 asli, PTS native, dan deklarasi viewed telah diverifikasi.")
    rows.extend(("## Pemeriksaan visual", "- [ ] Cocokkan profil desain, laporan lengkap, Overview, dan urutan Storyboard."))
    for shot in audit["shots"]:
        sid = shot["shot"]
        rows.extend((f"### {sid}", _link("Kolase shot", candidate / f"media/{sid}.jpg")))
        camera = shot["camera"]
        for phase in camera["phases"]:
            rows.append(f"- Fase {phase['start_s']:.3f}–{phase['end_s']:.3f}s · {display(phase['notation'])}")
        for segment in tempo_segments(shot):
            rows.append(f"- Tempo {segment['start_s']:.3f}–{segment['end_s']:.3f}s · "
                        f"{display(segment['label'])} · {display(segment['description'])}")
        if choice := shot["composition"].get("production_start"):
            index = choice["frame_index"]
            rows.append(f"- Production Start · F{index} · {manifest['frames'][str(index)]:.3f}s")
        panels = (row for row in manifest["selections"] if row["shot_id"] == sid and row["role"] != "overview")
        for panel in panels:
            label = panel.get("label") or panel["role"]
            rows.append(f"- Panel {_inline_caption(label)} · F{panel['frame_index']} · {panel['timestamp_s']:.3f}s")
        rows.extend(("- [ ] Cocokkan fase, arah, tempo, dan bukti frame.",
                     "- [ ] Periksa framing, kejernihan, caption, dan waktu panel."))
    rows.extend(changes)
    return "\n\n".join(rows) + "\n"


def reviewed_summary(audit, manifest, digest):
    shots = {}
    for i, shot in enumerate(audit["shots"]):
        sid = shot["shot"]
        phases = shot["camera"]["phases"]
        evidence = {}
        if start := shot["composition"].get("production_start"):
            evidence[f"/shots/{i}/composition/production_start"] = [start["frame_index"]]
        panels = [row for row in manifest["selections"] if row["shot_id"] == sid and row["role"] != "overview"]
        shots[sid] = {
            "notation": [f"{p['start_s']:.3f}–{p['end_s']:.3f}s · {p['notation']}" for p in phases],
            "evidence": evidence,
            "evidence_areas": {},
            "override_components": {},
            "panels": [f"{p.get('label') or p['role']} · F{p['frame_index']} · {p['timestamp_s']:.3f}s"
                       for p in panels],
            "panel_areas": {p["source_pointer"]: p["area_ids"] for p in panels},
        }
    audit_evidence = {}
    for pointer, claim, areas, sid, _ in claims(audit):
        evidence = audit_evidence if sid is None else shots[sid]["evidence"]
        evidence[pointer] = claim["evidence"]
        if sid is not None:
            shots[sid]["evidence_areas"][pointer] = areas
        for number, override in enumerate(claim.get("overrides", ())):
            override_pointer = f"{pointer}/overrides/{number}"
            shots[sid]["override_components"][override_pointer] = [override["component_index"]]
            if "evidence" in override:
                evidence[override_pointer] = override["evidence"]
    return {"snapshot_sha256": digest, "shots": shots, "evidence": audit_evidence,
            "media": {row["path"]: row["sha256"] for row in manifest["media"]}}


def _pointer_changes(before, after, label, render_value):
    rows = []
    for pointer in sorted(before.keys() | after.keys()):
        if before.get(pointer) != after.get(pointer):
            old_values = ", ".join(render_value(value) for value in before.get(pointer, [])) or "—"
            new_values = ", ".join(render_value(value) for value in after.get(pointer, [])) or "—"
            rows.append(f"- **{label}** `{pointer}` · {old_values} → {new_values}")
    return rows


def review_changes(previous, current):
    if previous is None:
        return []
    rows = ["## Perubahan sejak review sebelumnya",
            f"`{previous['snapshot_sha256']}` → `{current['snapshot_sha256']}`"]
    def frame_label(index):
        return f"F{index}"

    def component_label(index):
        return f"Komponen {index + 1}"

    if "evidence" in previous:
        audit_changes = _pointer_changes(previous["evidence"], current["evidence"], "Bukti", frame_label)
        if audit_changes:
            rows.extend(("### Bukti tingkat audit", *audit_changes))
    else:
        rows.append("Riwayat sebelumnya hanya mencatat sebagian bukti. "
                    "Perbandingan ini mencakup bukti yang sudah tercatat saat itu.")
    if any("panel_areas" not in shot for shot in previous["shots"].values()):
        rows.append("Riwayat sebelumnya belum mencatat cakupan area untuk semua panel.")
    if any("override_components" not in shot for shot in previous["shots"].values()):
        rows.append("Riwayat sebelumnya belum mencatat komponen yang dirujuk setiap override.")
    if any("evidence_areas" not in shot for shot in previous["shots"].values()):
        rows.append("Riwayat sebelumnya belum mencatat cakupan area bukti.")
    for sid in sorted(previous["shots"].keys() | current["shots"].keys()):
        old = previous["shots"].get(sid, {})
        new = current["shots"].get(sid, {})
        shot_changes = []
        for field, label, format_text in (("notation", "Notasi", display), ("panels", "Panel", _inline_caption)):
            if old.get(field) != new.get(field):
                before = " / ".join(format_text(item) for item in old.get(field, [])) or "—"
                after = " / ".join(format_text(item) for item in new.get(field, [])) or "—"
                shot_changes.append(f"- **{label}** · {before} → {after}")
        before, after = old.get("evidence", {}), new.get("evidence", {})
        if "evidence" not in previous:
            # Earlier summaries did not include claims about relations between areas.
            after = {pointer: frames for pointer, frames in after.items() if "/area_relations/" not in pointer}
        shot_changes.extend(_pointer_changes(before, after, "Bukti", frame_label))
        for field, label, render in (("panel_areas", "Cakupan area panel", _inline_caption),
                                      ("evidence_areas", "Cakupan area bukti", _inline_caption),
                                      ("override_components", "Komponen override", component_label)):
            if field in old or sid not in previous["shots"]:
                shot_changes.extend(_pointer_changes(old.get(field, {}), new.get(field, {}), label, render))
        if shot_changes:
            rows.extend((f"### {sid}", *shot_changes))
    old_media, new_media = previous["media"], current["media"]
    for path in sorted(old_media.keys() | new_media.keys()):
        if old_media.get(path) != new_media.get(path):
            rows.append(f"- **Media berubah** `{path}`")
    if len(rows) == 2:
        rows.append("Notasi, bukti, panel, dan media cocok pada kedua snapshot.")
    return rows
