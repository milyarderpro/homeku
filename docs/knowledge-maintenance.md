# Knowledge maintenance — stages 1–7

These commands are for maintainers. Creative consumers read static GitHub files through web or connector access and do not run these commands.

## Inventory and publication

The source manifest records all archived references and unannotated MP4 files, pinning source bytes and annotation revisions. The knowledge release selects sources for the published catalog, profiles, mappings and directories. Sources outside the snapshot remain usable for inspiration; new thematic claims are not inferred from their addition.

The parallel save runner recomputes the manifest append-only after rebasing and publishes it with the archive. It does not change the knowledge release. CI permits additions before saving while still protecting all pinned entries.

## Verify

Install scripts/requirements.txt in the maintenance environment, then run:

~~~sh
python scripts/verify_source_integrity.py --check
python scripts/knowledge_library.py --check
python scripts/refresh_design_catalog.py --check
python scripts/design_evidence.py --check
python scripts/knowledge_access.py --check
python scripts/video_similarity.py --check
python -m unittest discover -s tests -v
~~~

Source inventory --check is strict; ingestion regression checks allow append-only additions. Newly uploaded sources can be pinned before analysis with an explicit source-manifest refresh.

## Add archives

Keep the existing analysis/save procedure. The parallel runner updates the manifest after rendering and after each rebase, accepting additions only. Workers do not rebase competing generated manifest diffs. No profile, normalized sidecar, taxonomy release or thematic interpretation is published by ingestion.

## Rebuild the existing knowledge snapshot

~~~sh
python scripts/knowledge_library.py --write
~~~

This rebuilds generated files for the existing release without selecting new archives. Changed published source/annotation or taxonomy bytes invalidate the release binding and require explicit publication.

## Correct sources or publish a new snapshot

Review source corrections with AI and inspect the diff. Explicitly accept an intentional inventory correction using:

~~~sh
python scripts/verify_source_integrity.py --write
~~~

Publish a NEW release ID and date:

~~~sh
python scripts/knowledge_library.py --publish RELEASE_ID --date YYYY-MM-DD
~~~

Default selection is all archives; use --references ID1 ID2 for a subset. An immutable release ID can be repeated identically but cannot acquire different contents. Publication snapshots existing annotations; it is not a blanket claim of visual verification.

Manifests retain source/annotation hashes, taxonomy hash and computed counts under knowledge/releases/. Older artifacts and sources remain traceable through Git history; current working files are not a preserved copy of every historical release.

## Vocabulary changes

Keep published taxonomy files unchanged. Add a versioned JSON file with matching version and Indonesian/English aliases, then publish with --taxonomy-version VERSION and a new release ID. Ambiguous and unmapped labels stay visible; partial lexical mapping does not normalize every attribute or verify visual truth.

## Evidence enrichment and scoped AI review

For a newly published source, generate temporal evidence:

~~~sh
python scripts/sample_temporal_evidence.py --references ID1 ID2
~~~

Without --references the sampler visits the published snapshot and reuses valid cached media. It needs FFmpeg and ffprobe for extraction; ordinary consumers never need them. A changed source, annotation, frame or contact sheet rejects the old cache. Preserve the old material in Git history before explicitly removing/replacing that reference's derived temporal folder.

Inspect actual storyboard/sample/video evidence with AI. Write only findings that were actually reviewed into knowledge/reviews/visual-notes.json and temporal-notes.json, binding source and media hashes. Keep the scope narrow: sampled instants do not certify all intermediate motion. Model build is null if unavailable. No manual review is required.

After an intentional annotation correction, old notes must be re-reviewed or explicitly retained outside the active notes for that source revision. Do not merely replace their hash with the new one: that would invent a review. Missing new notes generate pending coverage; they never disqualify creative use.

Build in dependency order:

~~~sh
python scripts/design_evidence.py --write
python scripts/video_similarity.py --write
python scripts/knowledge_library.py --write
python scripts/evaluate_knowledge.py --write current
~~~

The first command creates observations, literal relations, source mention inventories, review records, aggregate counts, diversity and readable evidence. The similarity command scans all archived MP4 files, including unpublished/unannotated sources, and reports candidates only. Its report can need a refresh after archive growth even when published knowledge is unchanged.

Counts use each published video reference once. Content independence or physical-house identity is not established by file SHA uniqueness. Preserve counterexamples and annotation wording limitations.

The evaluation bank and baseline are frozen. Do not overwrite baseline or tune search on heldout answers. New evaluation versions require a new bank. The evaluator measures local positive retrieval examples and saved fields only; unmeasured creative/unknown answers retain null scores.

## Remaining publication and evaluation

Newly generated files must be published before external web AND connector smoke tests in stages 6–7; local navigation tests do not substitute for remote testing. No source-processing command pushes commits or tests a consumer model automatically.

[Stage 3–5 report](stage-3-5-report.md) records actual coverage and outstanding temporal-review limits.

## Reader publication and recorded access evaluation

The primary reading sequence is README → core → relevant theme/example → evidence when needed. Supporting media, review metadata and JSON remain available without becoming mandatory reading.

The access audit checks word budgets (root 350, guide 600, core 1100, profile 1200), local links and canonical annotation access. Counts are whitespace words, not model tokens. It fingerprints reader files and the release; changes require a fresh local report.

~~~sh
python scripts/knowledge_library.py --write
python scripts/knowledge_access.py --write
python scripts/knowledge_access.py --check
~~~

Remote testing requires publishing the exact candidate commit first. Record web and connector on that same commit in evaluations/stage7/web.json and github_connector.json, using only actual returned content or explicit access failures. The frozen stage3 bank is reused unchanged.

Each event records route, commit, path, tool, status, returned text, SHA-256 and character count. Source extraction must match actual fetched text. Responses cite exact fetched excerpts. No failed read may acquire an answer from local files or the other route. Record image and search capability separately.

The current assistant has prior repository context, so guided readthroughs are not blind consumer-model experiments. Mechanical retrieval/source checks and unscored semantic responses are separate. A future independent evaluation must start with only the repo URL, question and allowed route; it records model/build, answers and evidence use before judging. Do not report model accuracy from a navigation test.

For source corrections, dependency_impact in scripts/knowledge_access.py identifies source-specific profiles, mappings, evidence and review/media dependencies plus shared aggregates/directories. Published taxonomy changes refresh mappings; mixed taxonomy/source edits still require new source review. Unpublished archive additions do not change published interpretation.

CI verifies generated knowledge, scoped evidence and recorded access reports without making remote network calls or rewriting results. The snapshot and fingerprints describe which inputs were checked; Git history retains prior versions.
