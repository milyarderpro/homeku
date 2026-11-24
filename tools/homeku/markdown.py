"""Strict, documented Markdown tables; no semantic extraction from free prose."""

from __future__ import annotations

import math
import re

from .common import LibraryError, require

IDENTITY = ("format_version", "id", "revision", "title")
COVERAGE = ("method", "limitations")
COMPOSITION = ("overview_timestamp_s", "overview_role", "overview_reason", "overview_exception",
               "camera_position", "camera_direction", "view_angle", "camera_height", "camera_tilt",
               "foreground", "depth", "reveal", "start_composition", "end_composition", "motion_compatibility")
TIMELINE = ("shot", "start_s", "end_s", "areas", "transition", "continuity")
FACTS = ("id", "domain", "subject", "attribute", "value", "state", "confidence", "evidence")
PHASES = ("phase", "start_s", "end_s", "components", "anchor", "tempo", "speed_change", "basis",
          "evidence", "confidence", "uncertainty")
RELATIONS = ("from", "to", "relation", "description", "state", "confidence", "evidence")
PROFILE = ("id", "aspect", "value", "state", "confidence", "evidence")
PROFILE_ASPECTS = ("primary-style", "style-influence", "apparent-scale", "levels-visible", "massing", "roof",
                   "entrance", "porch", "openings", "material-hierarchy", "palette", "lighting", "environment",
                   "spatial-configuration", "distinctive-features", "continuity")
STATES = {"observed", "uncertain", "not-visible", "not-present", "unknown"}
CONFIDENCE = {"high", "medium", "low", "unknown"}
TEMPOS = {"slow", "moderate", "fast", "variable", "unknown"}
LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)\)")


def number(value, label):
    try:
        result = float(value)
    except (TypeError, ValueError) as error:
        raise LibraryError(f"{label}: expected seconds as a number") from error
    require(math.isfinite(result), f"{label}: number must be finite")
    return result


def split_row(line):
    require(line.startswith("|") and line.endswith("|"), f"Invalid table row: {line[:100]}")
    values = re.split(r"(?<!\\)\|", line[1:-1])
    return [v.strip().replace("\\|", "|").replace("\\\\", "\\") for v in values]


def tables(text):
    result, current = [], []
    for line in text.splitlines() + [""]:
        if line.startswith("|"):
            current.append(line.rstrip())
        elif current:
            require(len(current) >= 2, "Table needs a header and separator")
            header = split_row(current[0])
            require(len(header) == len(set(header)), "Duplicate table columns")
            separator = split_row(current[1])
            require(len(separator) == len(header) and all(re.fullmatch(r":?-{3,}:?", c) for c in separator),
                    "Invalid Markdown table separator")
            rows = []
            for line in current[2:]:
                values = split_row(line)
                require(len(values) == len(header), f"Wrong table column count: {line[:100]}")
                require(all(values), "Use 'unknown' or '-' instead of an empty cell")
                rows.append(dict(zip(header, values)))
            result.append((tuple(header), rows))
            current = []
    return result


def table(text, columns, label):
    found = tables(text)
    require(len(found) == 1 and found[0][0] == columns, f"{label}: expected exactly one table with columns {columns}")
    return found[0][1]


def fields(text, keys, label):
    rows = table(text, ("field", "value"), label)
    require(len(rows) == len(keys) and {r["field"] for r in rows} == set(keys), f"{label}: fields must be {keys}")
    return {r["field"]: r["value"] for r in rows}


def prose(text):
    """Keep authored prose while omitting parser tables and presentation wrappers."""
    return "\n".join(line for line in text.splitlines()
                     if not line.startswith("|") and not re.fullmatch(r"</?details>|<summary>.*</summary>", line.strip())
                     and not re.fullmatch(r'<a id="[^"]+"></a>', line.strip())).strip()


def sections(text, level):
    # Headings inside fenced camera summaries are not document headings.
    result, key, lines, fenced = {}, None, [], False
    for line in text.splitlines():
        if line.startswith("```"):
            fenced = not fenced
        match = None if fenced else re.fullmatch(r"#{" + str(level) + r"} (.+)", line)
        if match:
            if key is not None:
                result[key] = "\n".join(lines).strip()
            key, lines = match[1], []
            require(key not in result, f"Duplicate heading: {key}")
        elif key is not None:
            lines.append(line)
    require(not fenced, "Unclosed code fence")
    if key is not None:
        require(key not in result, f"Duplicate heading: {key}")
        result[key] = "\n".join(lines).strip()
    return result


def evidence(value):
    if value == "-":
        return []
    links = LINK.findall(value)
    residue = LINK.sub("", value).replace(";", "").strip()
    require(links and not residue, "Evidence must be semicolon-separated local Markdown links")
    return links


def normalized(value):
    return re.sub(r"\s+", " ", value).strip().rstrip(".")


def component(value, version=None):
    if version == "2.5":
        from .camera_notation import component as current
        return current(value)
    """Preserve the literal clause, while projecting explicit camera tokens only."""
    names = ("Dolly-In", "Dolly-Out", "Orbit Left", "Orbit Right", "Pan Left", "Pan Right",
             "Tilt Up", "Tilt Down", "Truck Left", "Truck Right", "Pedestal Up", "Pedestal Down",
             "Zoom-In", "Zoom-Out", "Tracking", "Static", "Uncertain")
    found = [name for name in names if re.search(r"\b" + re.escape(name).replace(r"\ ", "[ -]") + r"\b", value, re.I)]
    require(len(found) <= 1, "Use '+' between simultaneous camera components")
    name = found[0] if found else "other"
    direction = next((d for d in ("Left", "Right", "Up", "Down", "In", "Out")
                      if re.search(r"\b" + d + r"\b", name)), None)
    return {"raw": value.strip(), "movement": name, "direction": direction,
            "qualifiers": re.findall(r"\b(?:Accelerating|Decelerating|strong|gentle)\b", value, re.I),
            "estimates": re.findall(r"~[^()\n+→]+[°×]", value),
            "toward": value.split("toward", 1)[1].strip() if "toward" in value else None}


def parse(text):
    require("\x00" not in text, "NUL in Markdown")
    require(text.count("<details>") == text.count("</details>"), "Unbalanced details blocks")
    top = sections(text, 2)
    names = ["Identitas", "Ringkasan", "Cakupan", "Timeline", "Hubungan antarshot", "Keterbatasan"]
    require(all(name in top and top[name] for name in names), f"Missing required H2 section: {names}")
    identity = fields(top["Identitas"], IDENTITY, "Identitas")
    require(identity["revision"].isdigit(), "revision must be an integer")
    identity["revision"] = int(identity["revision"])
    require(identity["format_version"] in {"1.0", "1.1"}, "Unsupported Markdown format_version")
    modern = identity["format_version"] == "1.1"
    profile = []
    if modern:
        names += ["Profil DNA", "Palet dan suasana"]
        require(all(name in top and top[name] for name in names), "Missing readable DNA/palette sections")
        profile = table(top["Profil DNA"], PROFILE, "Profil DNA")
        require(set(PROFILE_ASPECTS) <= {r["aspect"] for r in profile}, "DNA profile must cover all required aspects; use unknown explicitly")
        ids_seen = set()
        for claim in profile:
            require(re.fullmatch(r"dna-[0-9]{2,}", claim["id"]) and claim["id"] not in ids_seen, "Invalid/duplicate DNA claim ID")
            ids_seen.add(claim["id"])
            require(claim["state"] in STATES and claim["confidence"] in CONFIDENCE, "Invalid DNA state/confidence")
            claim["evidence"] = evidence(claim["evidence"])
            require(claim["evidence"] or claim["state"] == "unknown", "DNA claim needs evidence")
        require(prose(top["Profil DNA"]), "Write a readable DNA narrative")
    coverage = fields(top["Cakupan"], COVERAGE, "Cakupan")
    timeline = table(top["Timeline"], TIMELINE, "Timeline")
    require(timeline, "Timeline must have at least one shot")
    ids = [row["shot"] for row in timeline]
    require(ids == [f"shot-{i:02d}" for i in range(1, len(ids) + 1)], "Shot IDs must be sequential: shot-01, shot-02, ...")
    require(set(top) == set(names + [f"Shot {sid}" for sid in ids]), "Unknown or missing H2 section")
    shots = []
    for row in timeline:
        sid = row["shot"]
        require(f'<a id="{sid}"></a>' in text, f"Missing explicit shot anchor: {sid}")
        subs = sections(top[f"Shot {sid}"], 3)
        required = {"Desain dan konfigurasi", "Fakta", "Komposisi", "Kamera", "Ketidakpastian"}
        if modern:
            required.add("Ikhtisar")
        require(set(subs) == required and all(subs.values()), f"{sid}: required H3 sections: {sorted(required)}")
        start, end = number(row["start_s"], sid), number(row["end_s"], sid)
        require(0 <= start < end, f"{sid}: invalid interval")
        areas = [v.strip() for v in row["areas"].split(";")]
        require(all(areas) and len(set(areas)) == len(areas), f"{sid}: invalid area list")
        comp = fields(subs["Komposisi"], COMPOSITION, f"{sid}/Komposisi")
        comp["overview_timestamp_s"] = number(comp["overview_timestamp_s"], sid)
        require(comp["overview_role"] in {"start", "middle", "end"}, f"{sid}: invalid overview_role")
        facts = table(subs["Fakta"], FACTS, f"{sid}/Fakta")
        fact_ids = [fact["id"] for fact in facts]
        require(len(fact_ids) == len(set(fact_ids)), f"{sid}: duplicate fact IDs")
        for fact in facts:
            require(re.fullmatch(r"f-[0-9]{2,}", fact["id"]), f"{sid}: invalid fact id")
            require(fact["state"] in STATES and fact["confidence"] in CONFIDENCE, f"{sid}: invalid fact state/confidence")
            fact["evidence"] = evidence(fact["evidence"])
            require(fact["evidence"] or fact["state"] == "unknown", f"{sid}: a claim needs media evidence")
        summaries = re.findall(r"```text\n(.*?)\n```", subs["Kamera"], re.S)
        require(len(summaries) == 1, f"{sid}: one camera summary in a text code fence is required")
        summary = summaries[0].strip()
        phases = table(subs["Kamera"], PHASES, f"{sid}/Kamera")
        clauses = [normalized(c) for c in summary.split("→")]
        require(len(phases) == len(clauses) and phases, f"{sid}: camera summary and phase count differ")
        for index, (phase, clause) in enumerate(zip(phases, clauses), 1):
            require(phase["phase"] == f"phase-{index:02d}", f"{sid}: phase IDs must be sequential")
            require(normalized(phase["components"]) == clause, f"{sid}: camera summary and phase components differ")
            phase["start_s"] = number(phase["start_s"], sid)
            phase["end_s"] = number(phase["end_s"], sid)
            require(start <= phase["start_s"] < phase["end_s"] <= end, f"{sid}: phase outside shot")
            expected_start = start if index == 1 else phases[index - 2]["end_s"]
            require(abs(phase["start_s"] - expected_start) <= 0.001, f"{sid}: phases must cover the shot without gaps/overlaps")
            require(phase["tempo"] in TEMPOS, f"{sid}: invalid tempo")
            require(phase["speed_change"] in {"accelerating", "decelerating", "constant", "variable", "unknown"}, f"{sid}: invalid speed_change")
            require(phase["confidence"] in CONFIDENCE, f"{sid}: invalid confidence")
            require(phase["tempo"] != "unknown" or phase["uncertainty"] != "-", f"{sid}: explain unknown tempo")
            phase["evidence"] = evidence(phase["evidence"])
            require(phase["evidence"], f"{sid}: camera phase needs evidence")
            phase["components_parsed"] = [component(v) for v in clause.split("+")]
            require(all(v.strip() for v in clause.split("+")), f"{sid}: empty camera component")
            if any("accelerating" in [q.lower() for q in c["qualifiers"]] for c in phase["components_parsed"]):
                require(phase["speed_change"] in {"accelerating", "variable"}, f"{sid}: accelerating summary conflicts with speed_change")
        require(abs(phases[-1]["end_s"] - end) <= 0.001, f"{sid}: phases must reach shot end")
        movements = {c["movement"] for phase in phases for c in phase["components_parsed"]}
        expected_role = "start" if movements == {"Dolly-In"} else "end" if movements == {"Dolly-Out"} else None
        if expected_role and comp["overview_role"] != expected_role:
            require(comp["overview_exception"] != "-", f"{sid}: explain IN/OUT overview exception")
        shots.append({**row, "start_s": start, "end_s": end, "areas": areas, "composition": comp,
                      "facts": facts, "camera_summary": summary, "phases": phases,
                      "design": subs["Desain dan konfigurasi"], "uncertainty": subs["Ketidakpastian"],
                      "review_summary": subs.get("Ikhtisar", subs["Desain dan konfigurasi"]),
                      "composition_notes": prose(subs["Komposisi"]),
                      "camera_notes": prose(re.sub(r"```text\n.*?\n```", "", subs["Kamera"], flags=re.S))})
    relations = table(top["Hubungan antarshot"], RELATIONS, "Hubungan antarshot")
    for relation in relations:
        require(relation["from"] in ids and relation["to"] in ids, "Relation has unknown shot")
        require(relation["state"] in STATES and relation["confidence"] in CONFIDENCE, "Invalid relation state/confidence")
        relation["evidence"] = evidence(relation["evidence"])
        require(relation["evidence"] or relation["state"] == "unknown", "Relation needs evidence")
    return {**identity, "summary": top["Ringkasan"], "coverage": coverage, "shots": shots,
            "profile": profile, "profile_notes": prose(top.get("Profil DNA", "")),
            "palette_notes": top.get("Palet dan suasana", ""), "timeline_notes": prose(top["Timeline"]),
            "relations": relations, "limitations": top["Keterbatasan"], "links": LINK.findall(text)}


def review_cards(model, analysis_sha256, *, media_prefix=""):
    """A deterministic review view of the same MD snapshot, with no new claims."""
    def media(path):
        return media_prefix.rstrip("/") + "/" + path if media_prefix else path
    lines = [f"# Tinjauan {model['id']} — revisi {model['revision']}", "",
             f"Snapshot analysis.md SHA-256: `{analysis_sha256}`", "", model["summary"], "",
             model.get("profile_notes", ""), "", model.get("palette_notes", ""), "",
             f"![Storyboard]({media('media/storyboard.jpg')})", ""]
    for shot in model["shots"]:
        comp = shot["composition"]
        lines += [f"## {shot['shot']} · {' / '.join(shot['areas'])} · {shot['start_s']:g}–{shot['end_s']:g} s", "",
                  f"![Gambaran area]({media('media/' + shot['shot'] + '/area-overview.jpg')})", "",
                  shot["review_summary"], "", "**Posisi dan pandangan:** " + comp["camera_position"] + " " + comp["camera_direction"] +
                  " Sudut: " + comp["view_angle"], "", "**Awal sumber:** " + comp["start_composition"], "",
                  "**Akhir sumber:** " + comp["end_composition"], "",
                  "**Peran gambar area:** " + comp["overview_role"] + " — " + comp["overview_reason"], "",
                  "**Kecocokan gerak:** " + comp["motion_compatibility"], "", "```text", shot["camera_summary"], "```", ""]
        for phase in shot["phases"]:
            lines += [f"- {phase['start_s']:g}–{phase['end_s']:g} s sumber "
                      f"({phase['start_s']-shot['start_s']:g}–{phase['end_s']-shot['start_s']:g} s dalam shot): "
                      f"{phase['components']}; tempo {phase['tempo']}; perubahan {phase['speed_change']}. "
                      f"Dasar: {phase['basis']} Batas: {phase['uncertainty']}"]
        lines += ["", "**Belum pasti:** " + shot["uncertainty"], ""]
    lines += ["## Batas keseluruhan", "", model["limitations"], "",
              "Laporan lengkap tetap tersedia pada analysis.md. Tinjauan ini tidak menyatakan persetujuan pengguna.", ""]
    return "\n".join(lines)
