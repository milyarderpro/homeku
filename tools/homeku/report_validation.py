"""Independent contract checks for the human report, not a second source of facts."""
import re
from .common import require
from .derivations import camera_summary, selections
from .render_assets import TEMPLATE

HEADINGS = ["## 1. Profil desain", "## 2. Ukuran & proporsi", "## 3. Shot Timeline",
            "## 4. Overview", "## 5. Storyboard", "## 6. Shot Details"]
CATEGORIES = ("architecture", "furnishings", "environment")


def plain(value, path, allow_empty=False):
    require(isinstance(value, str), f"{path}: expected plain text")
    require((allow_empty or bool(value.strip())) and "\n" not in value and "\r" not in value,
            f"{path}: write one plain paragraph")
    require(not re.search(r"^\s*(?:#{1,6}\s|>|\||[-+*]\s|\d+[.)]\s)|\x60{3}|~~~|<[/!A-Za-z]", value),
            f"{path}: Markdown blocks/HTML are not allowed in a paragraph")


def inline(value):
    return re.sub(r"([\\\x60*_[\]<>])", r"\\\1", value)


def display(value):
    plain(value, "Report text")
    return inline(value)


def lines(rows):
    return "\n".join(f"- **{title}:** {value}" for title, value in rows)


def table(columns, rows):
    def row(values):
        return "| " + " | ".join(str(value).replace("|", r"\|") for value in values) + " |"
    return "\n".join([row(columns), row(["---"] * len(columns)), *(row(values) for values in rows)])


def validate_report(text, audit, frames):
    require(re.findall(r"^## .+$", text, re.M) == HEADINGS,
            "analysis.md: exactly six ordered template sections required")
    require(len(re.findall(r"^# ", text, re.M)) == 1, "analysis.md: one title required")
    require(not re.search(r"^\s*(?:\x60{3}|~~~)|<(?!!--|a id=|/a>)[A-Za-z/!]", text, re.M),
            "analysis.md: unexpected code block/HTML")
    require(text.count('<a id="profil-dna"></a>') == 1, "analysis.md: missing profile anchor")
    require("| Shot | Time (s) | Duration | Area/Scene | Camera Movement |" in text,
            "analysis.md: timeline must use the five template columns")
    timeline = text.split(HEADINGS[2], 1)[1].split(HEADINGS[3], 1)[0]
    rows = [line for line in timeline.splitlines() if line.startswith("|")]
    require(len(rows) == len(audit["shots"]) + 2, "analysis.md: timeline row count mismatch")
    for line in rows:
        require(len(re.split(r"(?<!\\)\|", line)) == 7, "analysis.md: timeline column count mismatch")
    expected_images = ["media/overview.jpg", "media/storyboard.jpg"] + [
        f"media/{s['shot']}.jpg" for s in audit["shots"]]
    require(re.findall(r"!\[[^\n]*?\]\((media/[^)]+)\)", text) == expected_images,
            "analysis.md: media order/inventory mismatch")
    require(len(re.findall(r"^### Shot ", text, re.M)) == len(audit["shots"]),
            "analysis.md: one detail per continuous shot required")
    overview = text.split(HEADINGS[3], 1)[1].split(HEADINGS[4], 1)[0]
    labels = {v["id"]: inline(v["label"]) for v in audit["areas"]}
    expected_overviews = [
        f"**Shot {p['shot_id'][5:]} · {' / '.join(labels[k] for k in p['area_ids'])} · {p['timestamp_s']:.2f}s**"
        for p in selections(audit, frames) if p["role"] == "overview"]
    require(re.findall(r"^\*\*Shot .+$", overview, re.M) == expected_overviews,
            "analysis.md: Overview selection order/count mismatch")
    details = text.split(HEADINGS[5], 1)[1]
    chunks = re.split(r'^<a id="shot-[0-9]+"></a>\n\n', details, flags=re.M)[1:]
    require(len(chunks) == len(audit["shots"]), "analysis.md: shot anchors mismatch")
    template = TEMPLATE.read_text(encoding="utf-8")
    groups = re.findall(r"^#### .+$", template, re.M)
    require(len(groups) == 3, "Invalid report section contract")
    for s, chunk in zip(audit["shots"], chunks):
        require(re.findall(r"^#### .+$", chunk, re.M) == groups,
                f"{s['shot']}: A/B/C order mismatch")
        require(chunk.startswith(f"### Shot {s['shot'][5:]} · "), "analysis.md: shot order mismatch")
        expected_subgroups = len(s["design"]) if len(s["area_ids"]) > 1 else 0
        require(len(re.findall(r"^##### ", chunk, re.M)) == expected_subgroups,
                f"{s['shot']}: area grouping mismatch")
        for label in ("Arsitektur", "Furnitur & dekorasi", "Lingkungan"):
            require(chunk.count(f"**{label}**\n\n> ") == len(s["design"]),
                    f"{s['shot']}: missing design category {label}")
        require("**Camera:** " + inline(camera_summary(s)) + "\n" in chunk + "\n",
                f"{s['shot']}: camera literal mismatch")
        require(("**Movement Timeline**" in chunk) ==
                (len(s["area_ids"]) > 1 or len(s["camera"]["phases"]) > 1),
                f"{s['shot']}: conditional movement timeline mismatch")
    require(len(re.findall(r"^#{1,6} ", text, re.M)) ==
            7 + sum(4 + (len(s["design"]) if len(s["area_ids"]) > 1 else 0)
                    for s in audit["shots"]), "analysis.md: unexpected heading")
    return text
