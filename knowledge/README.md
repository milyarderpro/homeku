# HOMEKU Design Intelligence v2.0 — Knowledge Entry Point

**Purpose:** a source-grounded design knowledge library for originating coherent, distinctive house concepts from a curated collection of visual home-tour references. This directory is **not** a production workflow, prompt library, image-generation specification, or model-specific tutorial.

Start at [Core knowledge](ai-knowledge.md), then [concept directories](directories/README.md) or [individual profiles](reference-profiles/README.md). Both web and connector readers use these same files. See [access contract](access-contract.md) and [published release](release.json).

## Knowledge navigation

1. [methodology.md](methodology.md) — evidence classes, confidence, provenance and uncertainty.
2. [dna-summary.md](dna-summary.md) — seven-layer cross-reference synthesis.
3. [reference-catalog.md](reference-catalog.md) — published snapshot metadata overview.
4. [reference-profiles/README.md](reference-profiles/README.md) — individually traceable profiles of the published sources.
5. [architecture-dna.md](architecture-dna.md) — massing, scale, roof, envelope and openings.
6. [landscape-dna.md](landscape-dna.md) — setting, foreground, entrance and window views.
7. [interior-dna.md](interior-dna.md) — rooms, furniture and visual relationships.
8. [lighting-and-palette-dna.md](lighting-and-palette-dna.md) — source palette values, natural/practical light and mood.
9. [spatial-design-principles.md](spatial-design-principles.md) — geometry, reciprocal views and plausible adjacency.
10. [cinematography-dna.md](cinematography-dna.md) — framing, reveal, movement and visual sequence.
11. [design-compatibility.md](design-compatibility.md) — style combinations and conflict reasoning.
12. [originality-framework.md](originality-framework.md) — original design transformations.
13. [evidence-index.yaml](evidence-index.yaml) — curated claim-level YAML provenance examples.
14. [source-integrity.md](source-integrity.md) — canonical sources, retired IDs and byte-integrity checks.
15. [source-manifest.json](source-manifest.json) — SHA-256 source bindings and separate unannotated inventory.

16. [ai-knowledge.md](ai-knowledge.md) — compact core reading for creative AI.
17. [access-contract.md](access-contract.md) — shared web/connector reading paths.
18. [taxonomy/README.md](taxonomy/README.md) — versioned Indonesian/English vocabulary.
19. [directories/README.md](directories/README.md) — examples grouped by normalized concepts.

## Source hierarchy

`references/<ID>/analysis.yaml` (primary recorded observation) → `analysis.md` (human-readable narrative from those fields) → `storyboard.jpg` and `shot-NN.jpg` (visual orientation and sanity check). The original video under `video/` is the strongest source when inspecting motion; a keyframe alone cannot prove a camera path.

**No file here specifies** a required number of images, duration, generation platform, approval gate, video prompt, editing schedule, or audio policy. Any external master prompt or creative brief is a separate layer and does not retroactively become source evidence.

The knowledge set represents a **dated snapshot**. An additional reference does not silently update aggregated claims. See [methodology](methodology.md) and [maintenance](../docs/knowledge-maintenance.md) for explicit snapshot publication. Catalog regeneration alone does not publish new sources.

All saved references may inform new concepts. Confidence and analysis status qualify source claims; they do not prohibit creative choices. See the usage policy in [methodology](methodology.md).

**Claim classes:** `OBSERVATION` (one reference), `AGGREGATE` (counted source pattern), `INFERENCE` (interpretation), `DESIGN_PRINCIPLE` (general guidance, not a sourced historical fact). Never describe the last two as directly verified by video evidence.
