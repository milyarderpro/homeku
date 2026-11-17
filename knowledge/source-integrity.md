# Source integrity — active knowledge snapshot

Audited on 2026-11-17. This document records source provenance and integrity, not a production workflow or a semantic verification of design annotations.

## Current inventory

- 57 active reference packages, 295 shots/keyframes, and 6,111 recorded visual-detail items.
- Every active reference has its source MP4 available at the exact recorded filename.
- 62 source MP4 files: 57 bound to active references and 5 not yet annotated.
- No exact duplicate MP4 bytes remain in the current video directory (SHA-256 comparison). Re-encoded or visually similar videos are outside this check.
- Unannotated files remain source inventory only; they do not count as design evidence.

[source-manifest.json](source-manifest.json) pins each reference ID to its source path, SHA-256 and byte size. It separately lists unannotated files and retired IDs. These fingerprints establish a reviewed byte baseline; they do not prove a video's external origin, rights, or physical authenticity.

## Duplicate retirement

`edh026` was removed on 2026-11-17 at the user's direction because its MP4 was byte-identical to `edh027.mp4`. The canonical active reference is [edh027](../references/edh027/analysis.yaml). Its video, annotations and images are retained unchanged.

The duplicate's MP4, reference package, design profile, pending request and saved-result record were removed from the current tree. Previous Git revisions remain historical. The manifest's retirement record retains the shared hash and canonical ID. Restoring a retired reference, its source filename or either request artifact makes the integrity check fail. The save workflow excludes the retired request path from push triggers; it cannot be dispatched while the request file is absent.

Active aggregates and profile coverage were recalculated after removal. The former 58-reference/300-shot snapshot is historical and must not be used as the current dataset total.

## Restored legacy source

`video/dreamshome01.mp4` is available for [VID-001](../references/VID-001/analysis.yaml) and is fingerprinted in the manifest. FFprobe reports 720×1280 at 30 FPS, with a video-stream duration of 20.033333 seconds, consistent with the recorded 20.03-second annotation. The container duration is 20.176735 seconds; stream and container duration are different measurements.

Source availability and metadata consistency do not establish that every annotation is accurate. AI review, confidence and recorded uncertainties describe annotation quality; manual verification is not required.

## Read-only verification

```sh
python scripts/verify_source_integrity.py --check
python scripts/refresh_design_catalog.py --check
python -m unittest discover -s tests -v
```

The integrity check rejects missing/empty sources, source-content duplicates under different filenames, multiple references bound to one source, unsafe filenames, case collisions, retired artifacts and changes to pinned source bytes or bindings. CI runs it through the regression suite when source, knowledge or maintenance files change.

After an intentional source inventory change, review the new/changed sources and then explicitly refresh the manifest with `python scripts/verify_source_integrity.py --write`. Invalid duplicates and retired artifacts cannot be accepted by this refresh. A new source does not automatically become a new design principle, profile or evidence claim.

Catalog refreshes remain explicit. This source audit adds no references and does not change the repository's knowledge-only scope.
