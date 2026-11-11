# Evidence and synthesis methodology

## Dataset and provenance

The baseline is 58 archived reference packages (10 legacy `VID-XXX`, 48 `edh...`), 300 annotated shots, at source snapshot commit [80072ac](https://github.com/milyarderpro/homeku/tree/80072accc56f7824d9575f144ed4e88dcf51a8bc), audited 2026-11-09 in the original P1 summary. The current knowledge migration was compared with `main` at commit `6bfe47ae3235ca5276097996de291e9318c3e7d5`. The catalog can be regenerated; **numbers must not be treated as live counters**.

Individual `analysis.yaml` records are source-of-record *annotations*, not independent measurements. Recorded `analysis_quality.human_verified` is false for the original 58; 57 have status `draft` and one is `reviewed`. Video cuts, focal lengths, materials, building area, world geography and seasons may remain uncertain. `common_regions` classifies stylistic association, not the location of a home.

## Four claim types

- **OBSERVATION:** directly reported visual features in one source. Cite `reference_id`, `shot_id`, field path and observation. Words like *stone appearance* are preferable to asserting hidden material composition.
- **AGGREGATE:** a computation from an identified snapshot of reference YAML. State numerator, denominator, measurement and exceptions; never generalize a curated sample to all viral videos.
- **INFERENCE:** a reasoned description of why a composition or combination may be visually coherent. Label as interpretation; not observed audience response or verified architecture.
- **DESIGN_PRINCIPLE:** a proposal-independent constraint used for new coherent designs (adjacency, line of sight, massing compatibility). May be architectural reasoning beyond the dataset; explicitly not attributed as a source observation.

## Evidence record contract

`knowledge/evidence-index.yaml` stores `id`, `category`, `claim_type`, `statement`, `sources` (each with `reference_id`, `shot_id`, `field_path`), `confidence`, and `limitations`. A reference points to actual `references/<ID>/analysis.yaml`; `shot_id` must exist. `field_path` uses `shots[N].<path>` with a zero-based shot index, or a root field. A record with two source IDs is **not** a claim that those houses are physically connected.

## Coverage of all 58 sources

The [reference profiles](reference-profiles/README.md) contain concise source-metadata signatures for all 58 references: perceived scale, architectural features, color labels, lighting, scene sequence and opening camera annotation. The 23 initial curated records in `evidence-index.yaml` are **worked examples**, not 58 complete per-shot records, and should not be described as exhaustive. Profiles link directly to source YAML and retain its recorded field names. Deeper thematic inference still requires human/AI review of additional shots and original frames.

## Interpretation safeguards

1. A labeled camera motion is inferred from pixels; it does not establish physical equipment or prove the difference between mechanical dolly and generative zoom.
2. Frame-to-frame continuity is evidence only within an observed shot; two separate cuts may show staged or synthetic spaces. No reference yields a measured whole-house floorplan by default.
3. Area ranges under `architecture.building_scale.estimated_floor_area_m2` are *visual estimates* with uncertainty, not real-estate surveys.
4. Exterior vegetation and interior window views can support a shared visual world but do not prove cardinal directions or season.
5. The collection was selected for perceived or reported success; per-platform, date-stamped views, retention and counterfactual controls are absent. **No element is proven to cause virality.**
6. Source observations and creative principles should never be conflated. Review conflicts against the original YAML and frames rather than averaging incompatible features.

## Maintenance

New references enter through the existing analysis-and-save pipeline. A deliberate knowledge refresh subsequently reruns the catalog builder, checks changes against the previous source snapshot, reviews new evidence against source YAML and keyframes, and updates affected thematic documents. The build script intentionally **does not use AI to invent insights**. Creative statements require review; do not auto-promote a count into a design rule.
