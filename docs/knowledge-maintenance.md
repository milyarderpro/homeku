# Knowledge maintenance — stages 1 and 2

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

## Remaining stages

Observation, review and aggregate schemas prepare later work. No new review event is invented. Visual review and relationship enrichment are later stages. Newly generated files must be published before external web AND connector smoke tests; local navigation tests do not substitute for remote testing.
