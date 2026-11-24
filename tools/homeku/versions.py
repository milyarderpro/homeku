"""Explicit version dispatch; accepted source and renderer bytes stay unchanged."""
JSON_CONTRACTS = ("2.0", "2.1", "2.2", "2.3", "2.4", "2.5")
OVERVIEW_CONTRACTS = ("2.1", "2.2", "2.3", "2.4", "2.5")
QUALITY_CONTRACTS = ("2.2", "2.3", "2.4", "2.5")
DEFAULT_REPORT = {"2.0": "2.1.2", "2.1": "2.2.0", "2.2": "2.2.1", "2.3": "2.2.2", "2.4": "2.2.3", "2.5": "2.2.4"}
SCHEMA_SUFFIX = {"2.0": "v2", "2.1": "v2-1", "2.2": "v2-2", "2.3": "v2-3", "2.4": "v2-4", "2.5": "v2-5"}
BASELINE_FPS = {"2.2": 10, "2.3": 6, "2.4": 6, "2.5": 6}


def schema_name(kind, version):
    from .common import require
    require(version in SCHEMA_SUFFIX, f"Unsupported JSON contract: {version}")
    return f"{kind}-{SCHEMA_SUFFIX[version]}.schema.json"
