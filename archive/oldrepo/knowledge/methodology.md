# Evidence and synthesis methodology

## Dataset and provenance

The initial published snapshot 2026-11-17-stage-1-2 contains 57 reference packages (10 legacy `VID-XXX`, 47 `edh...`) and 295 annotated shots after source-integrity cleanup on 2026-11-17. The earlier 2026-11-09 P1 audit at commit [80072ac](https://github.com/milyarderpro/homeku/tree/80072accc56f7824d9575f144ed4e88dcf51a8bc) described 58 packages and 300 shots before duplicate removal; its totals are historical, not current counters. See [source-integrity.md](source-integrity.md) and [source-manifest.json](source-manifest.json) for the current source bindings and SHA-256 fingerprints.

Individual `analysis.yaml` records are source-of-record *annotations*, not independent measurements. The analysis workflow includes AI review before saving. Existing analysis status labels are retained as recorded; this migration does not invent new review events or change them in bulk. Quality is expressed through confidence, uncertainties, timestamp precision and notes, without a manual-verification requirement. Video cuts, focal lengths, materials, building area, world geography and seasons may remain uncertain. `common_regions` classifies stylistic association, not the location of a home.

## Four claim types

- **OBSERVATION:** directly reported visual features in one source. Cite `reference_id`, `shot_id`, field path and observation. Words like *stone appearance* are preferable to asserting hidden material composition.
- **AGGREGATE:** a computation from an identified snapshot of reference YAML. State numerator, denominator, measurement and exceptions; never generalize a curated sample to all viral videos.
- **INFERENCE:** a reasoned description of why a composition or combination may be visually coherent. Label as interpretation; not observed audience response or verified architecture.
- **DESIGN_PRINCIPLE:** a proposal-independent constraint used for new coherent designs (adjacency, line of sight, massing compatibility). May be architectural reasoning beyond the dataset; explicitly not attributed as a source observation.

## Evidence record contract

`knowledge/evidence-index.yaml` stores `id`, `category`, `claim_type`, `statement`, `sources` (each with `reference_id`, `shot_id`, `field_path`), `confidence`, and `limitations`. A reference points to actual `references/<ID>/analysis.yaml`; `shot_id` must exist. `field_path` uses `shots[N].<path>` with a zero-based shot index, or a root field. A record with two source IDs is **not** a claim that those houses are physically connected.

## Coverage and published snapshot

The [reference profiles](reference-profiles/README.md) contain source-metadata signatures for the [current published snapshot](release.json): perceived scale, architectural features, color labels, lighting, scene sequence and opening camera annotation. The 23 initial curated records in `evidence-index.yaml` are **worked examples**, not 57 complete per-shot records, and should not be described as exhaustive. Profiles link directly to source YAML and retain its recorded field names. Deeper thematic inference still requires AI review of additional shots and original frames.

## Interpretation safeguards

1. A labeled camera motion is inferred from pixels; it does not establish physical equipment or prove the difference between mechanical dolly and generative zoom.
2. Frame-to-frame continuity is evidence only within an observed shot; two separate cuts may show staged or synthetic spaces. No reference yields a measured whole-house floorplan by default.
3. Area ranges under `architecture.building_scale.estimated_floor_area_m2` are *visual estimates* with uncertainty, not real-estate surveys.
4. Exterior vegetation and interior window views can support a shared visual world but do not prove cardinal directions or season.
5. The collection was selected for perceived or reported success; per-platform, date-stamped views, retention and counterfactual controls are absent. **No element is proven to cause virality.**
6. Source observations and creative principles should never be conflated. Review conflicts against the original YAML and frames rather than averaging incompatible features.

## Using references for new concepts

All saved references are available for creative exploration; recorded analysis status and low confidence do not exclude them from inspiration. Confidence describes how certain a claim about the source is, not whether a material or design element may be chosen for a new concept.

For example, a source may show a stone-like surface with uncertain composition. A new design may explicitly choose natural stone as a creative decision. Do not retroactively claim that the source proves natural stone. The same distinction applies to newly designed room adjacency, dimensions, orientation and camera paths.

Review is performed by AI as part of analysis and may be repeated for targeted corrections or enrichment. There is no manual-verification gate and no replacement blanket verification flag. Preserve claim-level uncertainty and distinguish creative decisions from source observations.

## Attribution when adapting a reference

A source attribute needs support at the level being claimed: reference ID, relevant shot or source field, and the wording or visible evidence that supports it. A link to a general theme establishes context; it does not establish every adjective about a particular reference. A recorded label is also not an independent physical measurement.

A requested brief describes the desired new house. Its attributes do not become facts about whichever references are selected. Keep the source attribute, any interpretation, and the proposed transformation distinct.

For example, [edh052's annotation](../references/edh052/analysis.yaml) records `lush_tropical_landscaping` at `/visual_style/setting/1`. This is a qualitative source label, not a measured planting-density value.

| Statement | Status |
| --- | --- |
| The edh052 annotation records lush tropical landscaping | Traceable source statement |
| A new house uses its tropical vocabulary with lighter, more spaced planting | Creative adaptation |
| edh052 proves that its garden is sparse because the brief requests a light tropical garden | Unsupported attribution |

The same distinction applies to material composition, proportions, lighting, room relationships and camera paths. A transformation may deliberately simplify, intensify or combine source qualities. It remains usable even when the original attribute has low confidence; it must not be presented as a newly verified property of the source.

## Principles, project choices and unresolved alternatives

A DESIGN_PRINCIPLE is general reasoning, such as keeping connecting openings compatible across reciprocal views. Choosing natural stone for one new house or placing its kitchen north of its living room is a project-specific creative decision, not an observation about a reference and not itself a general principle.

An alternative such as “stone or tile” describes several possible designs. A specified material describes one design. Likewise, “island or peninsula if space allows” leaves geometry unresolved. These levels of specificity should not be conflated with a single established arrangement.

This library explains those distinctions. Selecting project alternatives and checking their use in final descriptions belong to the external plugin or master prompt.

## Maintenance

New references enter through the existing analysis-and-save pipeline and append-only source inventory. Explicit knowledge publication selects their source/annotation revisions, builds profiles and vocabulary mappings, and leaves thematic interpretations subject to separate AI review. Source corrections invalidate published bindings until a new release is selected. See [maintenance](../docs/knowledge-maintenance.md). The build script intentionally **does not use AI to invent insights**. Creative statements require review; do not auto-promote a count into a design rule.
