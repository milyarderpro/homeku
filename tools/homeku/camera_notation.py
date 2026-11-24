"""Camera notation parser. Preserves literals; never infers physical motion."""
import math
import re
from .common import require

NUMBER = r"[0-9]+(?:[.,][0-9]+)?"
ESTIMATE = re.compile(r"~" + NUMBER + r"(?:°?[–−-]" + NUMBER + r")?[°×x]")
QUALIFIER = re.compile(r"\b(?:Straight|Diagonal|Pure|Mild|Subtle|Moderate|Strong|gentle|Accelerating|Decelerating|Constant|Ease-In|Ease-Out)\b", re.I)
MOVEMENTS = (
    "Dolly-In", "Dolly-Out", "Orbit Left", "Orbit Right", "Pan Left", "Pan Right",
    "Tilt Up", "Tilt Down", "Truck Left", "Truck Right", "Pedestal Up", "Pedestal Down",
    "Zoom-In", "Zoom-Out", "Tracking", "Static Distance", "Static", "Uncertain",
)


def normalize(text):
    require(isinstance(text, str), "Camera notation must be a string")
    text = re.sub(r"(?<=\d),(?=\d)", ".", text)
    return re.sub(r"(?<=\d)x\b", "×", text)


def component(value):
    require(isinstance(value, str) and value.strip(), "Empty camera component")
    raw = value.strip()
    require("+" not in raw and "→" not in raw and "\n" not in raw,
            "Use one clause per component and one paragraph per phase")
    found = [name for name in MOVEMENTS if re.search(
        r"\b" + re.escape(name).replace(r"\ ", "[ -]") + r"\b", raw, re.I)]
    if "Static Distance" in found:
        found.remove("Static")
    require(len(found) <= 1, "Use '+' between simultaneous camera components")
    movement = found[0] if found else "other"
    direction = next((d for d in ("Left", "Right", "Up", "Down", "In", "Out")
                      if re.search(r"\b" + d + r"\b", movement)), None)
    estimates = ESTIMATE.findall(raw)
    require("~" not in ESTIMATE.sub("", raw), "Invalid numeric camera estimate")
    target = re.search(r"\btoward\s+(.+)$", raw, re.I)
    result = {"raw": raw, "movement": movement, "direction": direction,
              "qualifiers": QUALIFIER.findall(raw),
              "estimates": [normalize(v) for v in estimates],
              "toward": target[1].strip() if target else None}
    validate_component(result)
    return result


def bounds(value, unit):
    match = re.fullmatch(r"~(" + NUMBER + r")(?:°?[–−-](" + NUMBER + r"))?" +
                         re.escape(unit), value)
    require(match is not None, "Invalid visual estimate/range")
    lo, hi = float(match[1].replace(",", ".")), float((match[2] or match[1]).replace(",", "."))
    require(math.isfinite(lo) and math.isfinite(hi) and 0 < lo <= hi,
            "Use a finite positive ordered estimate/range")
    if unit == "×":
        require(lo >= 1, "IN/OUT scale magnitude must be at least one")
    return lo, hi


def validate_component(value, phase=None):
    raw = normalize(value["raw"])
    require(raw.count("(") == raw.count(")"), "Unbalanced camera parentheses")
    for estimate in value["estimates"]:
        bounds(estimate, estimate[-1])
        require(re.search(r"\([^)]*" + re.escape(estimate) + r"[^)]*\)", raw) is not None,
                "Write camera estimates inside parentheses")
    # Component easing is retained, not converted to a shot-wide tempo/curve.


def parse(notation):
    require(isinstance(notation, str) and notation.strip() and "{{" not in notation,
            "Fill phase notation before parsing")
    require("→" not in notation and "\n" not in notation,
            "One phase cannot contain sequential arrows or line breaks")
    return [component(clause.strip()) for clause in notation.strip().rstrip(".").split("+")]
