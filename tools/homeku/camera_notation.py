"""Version 2.5 notation. Descriptors are retained; no movement is inferred."""
import math
import re
from .common import require

NUMBER = r"[0-9]+(?:[.,][0-9]+)?"
ESTIMATE = re.compile(r"~" + NUMBER + r"(?:°?[–−-]" + NUMBER + r")?[°×x]")
QUALIFIER = re.compile(r"\b(?:Straight|Diagonal|Pure|Mild|Subtle|Moderate|Strong|gentle|Accelerating|Decelerating|Constant|Ease-In|Ease-Out)\b", re.I)

def normalize(text):
    text = re.sub(r"(?<=\d),(?=\d)", ".", text)
    return re.sub(r"(?<=\d)x\b", "×", text)

def component(value):
    from .markdown import component as legacy
    raw = value.strip()
    result = legacy(raw)
    result["qualifiers"] = QUALIFIER.findall(raw)
    estimates = ESTIMATE.findall(raw)
    require("~" not in ESTIMATE.sub("", raw), "Invalid numeric camera estimate")
    result["estimates"] = [normalize(v) for v in estimates]
    if re.search(r"\bStatic Distance\b", raw, re.I):
        result["movement"] = "Static Distance"
    return result

def bounds(value, unit):
    m = re.fullmatch(r"~(" + NUMBER + r")(?:°?[–−-](" + NUMBER + r"))?" + re.escape(unit), value)
    require(m is not None, "Invalid visual estimate/range")
    lo, hi = float(m[1].replace(",", ".")), float((m[2] or m[1]).replace(",", "."))
    require(math.isfinite(lo) and math.isfinite(hi) and 0 < lo <= hi, "Use a finite positive ordered estimate/range")
    if unit == "×":
        require(lo >= 1, "IN/OUT scale magnitude must be at least one")
    return lo, hi

def validate_component(c, phase):
    qualifiers = {q.casefold() for q in c["qualifiers"]}
    if qualifiers & {"ease-in", "accelerating"}:
        require(phase["speed_change"] in {"accelerating", "variable"}, "Ease-In/Accelerating conflicts with speed_change")
    if qualifiers & {"ease-out", "decelerating"}:
        require(phase["speed_change"] in {"decelerating", "variable"}, "Ease-Out/Decelerating conflicts with speed_change")
    for estimate in c["estimates"]:
        bounds(estimate, estimate[-1])
        require(re.search(r"\([^)]*" + re.escape(estimate) + r"[^)]*\)", c["raw"]) is not None,
                "Write normalized estimates inside parentheses")
