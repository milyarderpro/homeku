# Knowledge data contracts

Source analyses remain schema 2.1. [knowledge.schema.json](knowledge.schema.json) defines Draft 2020-12 contracts for derived data; it does not require editing archived annotations.

| Contract | Meaning |
| --- | --- |
| source | Canonical reference ID, source/annotation paths and SHA-256 fingerprints |
| release | Explicit snapshot selection, counts, taxonomy version and source revisions |
| normalization | Source-bound lexical mappings retaining every selected raw value |
| mapping | Field pointer, raw value, dimensions, state, coverage, candidates and modifiers |
| observation | Claim-level record with basis, evidence, source revision, confidence and limits |
| review | Scoped AI review event with method, scope, source revision and findings |
| aggregate | Counted statement with numerator, denominator and release identity |

Stage 3–5 activates observation, review and aggregate contracts. Additional relation, entity_mention, temporal_frame, temporal_shot, design_shot and design_evidence contracts constrain source-bound enrichment. World orientation and cross-cut adjacency remain unknown. Review events are generated only from actual source/media-bound AI notes; sampled-frame availability alone cannot create an event.

OBSERVATION explicitly distinguishes recorded_annotation, ai_storyboard_review and ai_sampled_temporal_review. A literal recorded relation is evidence of the saved description, not a fresh endorsement of physical geometry. Metadata alias discrepancies are mechanical findings outside visual review events. Exact runtime model build is unavailable and recorded as null.

Observation IDs are stable within their source revision. Normalization IDs are deterministic from reference ID, field pointer and raw value; reordering source arrays requires a new annotation revision, not silent reuse of old evidence. Actual source terms are never overwritten by normalized values.

A missing field differs from null/unknown, an empty list, explicitly not visible and explicitly not applicable. Alternatives/negations remain ambiguous candidates. Exact/partial coverage describes lexical mapping coverage, not visual certainty. Alias collisions within one dimension fail validation.

Source and annotation changes invalidate the published binding. Explicit release publication selects updated revisions. A published taxonomy version and release ID cannot be overwritten with different content. Automated archive synchronization accepts additions only; pinned source changes require an explicit reviewed maintenance update.

No manual verification flag is required. Existing confidence and uncertainty remain in the source of truth. All saved references can inspire creative decisions; status and lexical coverage do not act as creativity filters.

JSON validation uses jsonschema Draft202012Validator with only local definitions; no network reference resolution is necessary. [Maintenance](../docs/knowledge-maintenance.md) explains deterministic build/check commands.
