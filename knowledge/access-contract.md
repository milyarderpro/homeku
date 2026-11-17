# Knowledge access contract

This library supports two reading routes: GitHub web/file access and a GitHub connector available to the consumer. The repository URL identifies the source; the route does not define a different knowledge corpus.

| Item | Canonical repository path |
| --- | --- |
| Entry | README.md |
| Core reading | knowledge/ai-knowledge.md |
| Current published snapshot | knowledge/release.json |
| Concept directories | knowledge/directories/README.md |
| Reference profile | knowledge/reference-profiles/REFERENCE_ID.md |
| Original annotation | references/REFERENCE_ID/analysis.yaml |
| Original report | references/REFERENCE_ID/analysis.md |
| Source image | references/REFERENCE_ID/shot-NN.jpg |
| Separate normalization | knowledge/enrichment/REFERENCE_ID.json |
| Original source inventory | knowledge/source-manifest.json |

[Core knowledge](ai-knowledge.md) · [Published profiles](reference-profiles/README.md) · [Vocabulary](taxonomy/README.md)

## Reading routes

Web readers start at the root README, follow Markdown links and open relevant profiles and evidence. Connector readers use the same paths and IDs to read or search files when their available tools support those operations. No custom search API, database, vector index, local clone or script execution is required for creative use.

A release ID and annotation/source SHA-256 bind each published profile to its source. Read the same branch/commit or release when comparing the two routes. A successful text fetch is not evidence that an image or video was viewed. Private repositories need an appropriately authenticated route. Reading failure is not permission to invent missing source content.

## Scope and growth

Saved archives remain available as creative references. A published snapshot describes the sources selected for the current derived knowledge library; selection is not a manual-verification or creative-eligibility gate. New archives do not silently change published counts, normalized labels, profiles or thematic interpretations.

The original schema 2.1 annotation retains its labels. The normalization records point back to field paths and annotation hashes. A lexical match never establishes real material composition, house location or physical camera equipment.

## Prototype verification status

Local validation checks navigation, field/path identities, snapshot hashes, alias behavior and deterministic build output. External web and connector reading of new files must be smoke-tested after these local changes are published to GitHub. This document does not claim that new, unpushed files have already been accessed through either remote route.

Suggested remote smoke test: starting with only the repo URL, read the core document, find a small-house example in a concept directory, open its profile and source annotation, compare the reference ID and annotation hash with the release, and separately test whether a shot image can actually be viewed. Repeat through the connector on the same commit. This is a knowledge-access test, not a video-production workflow.
