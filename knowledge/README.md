# HOMEKU Design Intelligence v2.0 — Knowledge Entry Point

**Purpose:** a source-grounded design knowledge library for originating coherent, distinctive house concepts from a curated collection of visual home-tour references. This directory is **not** a production workflow, prompt library, image-generation specification, or model-specific tutorial.

## Knowledge navigation

1. [methodology.md](methodology.md) — evidence classes, confidence, provenance and uncertainty.
2. [dna-summary.md](dna-summary.md) — seven-layer cross-reference synthesis.
3. [reference-catalog.md](reference-catalog.md) — 58-reference searchable metadata overview.
4. [reference-profiles/README.md](reference-profiles/README.md) — individually traceable profiles of **all 58** sources.
5. [architecture-dna.md](architecture-dna.md) — massing, scale, roof, envelope and openings.
6. [landscape-dna.md](landscape-dna.md) — setting, foreground, entrance and window views.
7. [interior-dna.md](interior-dna.md) — rooms, furniture and visual relationships.
8. [lighting-and-palette-dna.md](lighting-and-palette-dna.md) — source palette values, natural/practical light and mood.
9. [spatial-design-principles.md](spatial-design-principles.md) — geometry, reciprocal views and plausible adjacency.
10. [cinematography-dna.md](cinematography-dna.md) — framing, reveal, movement and visual sequence.
11. [design-compatibility.md](design-compatibility.md) — style combinations and conflict reasoning.
12. [originality-framework.md](originality-framework.md) — original design transformations.
13. [evidence-index.yaml](evidence-index.yaml) — curated claim-level YAML provenance examples.

## Source hierarchy

`references/<ID>/analysis.yaml` (primary recorded observation) → `analysis.md` (human-readable narrative from those fields) → `storyboard.jpg` and `shot-NN.jpg` (visual orientation and sanity check). The original video under `video/` is the strongest source when inspecting motion; a keyframe alone cannot prove a camera path.

**No file here specifies** a required number of images, duration, generation platform, approval gate, video prompt, editing schedule, or audio policy. Any external master prompt or creative brief is a separate layer and does not retroactively become source evidence.

The knowledge set represents a **dated snapshot**. An additional reference does not silently update aggregated claims. See [methodology](methodology.md) and `scripts/refresh_design_catalog.py` for an explicit refresh path.

**Claim classes:** `OBSERVATION` (one reference), `AGGREGATE` (counted source pattern), `INFERENCE` (interpretation), `DESIGN_PRINCIPLE` (general guidance, not a sourced historical fact). Never describe the last two as directly verified by video evidence.
