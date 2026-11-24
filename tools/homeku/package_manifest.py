"""Technical provenance and media inventory for a compact audit package."""
from . import FORMAT_VERSION
from .common import require
from .derivations import frame_map, selections
from .models import schema_check


def build_manifest(audit, source, logs, audit_sha256, config, times, media, *,
                   supersedes=None, purpose="reference"):
    frames = frame_map(audit, times)
    manifest = {
        "contract_version": FORMAT_VERSION,
        "id": audit["id"], "revision": audit["revision"],
        "supersedes": supersedes, "purpose": purpose,
        "source": source, "audit": logs, "audit_sha256": audit_sha256, "render": config,
        "frames": frames, "selections": list(selections(audit, frames)), "media": media,
    }
    return schema_check(manifest, "manifest.schema.json")


def validate_frame_map(manifest, audit, times=None):
    frames = manifest["frames"]
    if times is not None:
        require(frames == frame_map(audit, times), "Manifest PTS map differs from native referenced frames")
    else:
        from .derivations import referenced_frames
        require(set(frames) == {str(i) for i in referenced_frames(audit)},
                "Manifest PTS map must contain only referenced frames")
    indices = sorted(map(int, frames))
    require(all(frames[str(a)] < frames[str(b)] for a, b in zip(indices, indices[1:])),
            "Manifest native PTS must increase")
    require(manifest["selections"] == list(selections(audit, frames)),
            "Manifest selections differ from source choices and native PTS")
