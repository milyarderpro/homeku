"""The subset executor uses the same implementation as full rendering."""
from .media import render_one


def render_missing_media(folder, plan, missing, source_path, source, config):
    return [render_one(folder, meta, selected, design, source_path, source, config)
            for meta, selected, design in plan if meta["path"] in missing]
