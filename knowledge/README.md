# HOMEKU Design Intelligence v2.0 — Knowledge Entry Point

**Purpose:** a source-grounded design knowledge library for originating coherent, distinctive house concepts from a curated collection of visual home-tour references. This directory is **not** a production workflow, prompt library, image-generation specification, or model-specific tutorial.

## Knowledge navigation

1. [methodology.md](methodology.md) — source hierarchy, confidence, categories of claims, limitations and maintenance.
2. [dna-summary.md](dna-summary.md) — cross-reference synthesis and seven visual layers.
3. [reference-catalog.md](reference-catalog.md) — searchable index of reference identifiers, styles, scene sequences and camera metadata.
4. [reference-profiles/README.md](reference-profiles/README.md) — selective source-grounded architectural, color, lighting, scene and camera signatures for **all 58** references.
5. [architecture-dna.md](architecture-dna.md) — massing, scale, roof, envelope, openings, visible material families.
6. [landscape-dna.md](landscape-dna.md) — landscape composition, entrance and window-world continuity.
7. [interior-dna.md](interior-dna.md) — interior character, spatial anchors and furniture relationships.
7. [spatial-design-principles.md](spatial-design-principles.md) — observed vs inferred adjacency, views and geometric coherence.
8. [cinematography-dna.md](cinematography-dna.md) — framing, visual reveal, camera vocabulary and scene grammar.
9. [design-compatibility.md](design-compatibility.md) — compatibility reasoning and risks in cross-reference synthesis.
10. [originality-framework.md](originality-framework.md) — transformations that preserve visual vocabulary without copying a specific house.
11. [evidence-index.yaml](evidence-index.yaml) — machine-readable examples of traceable evidence, inferences and their limits.

## Source hierarchy

`references/<ID>/analysis.yaml` (primary recorded observation) → `analysis.md` (human-readable narrative from those fields) → `storyboard.jpg` and `shot-NN.jpg` (visual orientation and sanity check). The original video under `video/` is the strongest source when inspecting motion; a keyframe alone cannot prove a camera path.

**No file here specifies** a required number of images, duration, generation platform, approval gate, video prompt, editing schedule, or audio policy. Any external master prompt or creative brief is a separate layer and does not retroactively become source evidence.

The knowledge set represents a **dated snapshot**. An additional reference does not silently update aggregated claims. See [methodology](methodology.md) and `scripts/refresh_design_catalog.py` for an explicit refresh path.

**Claim classes:** `OBSERVATION` (one reference), `AGGREGATE` (counted source pattern), `INFERENCE` (interpretation), `DESIGN_PRINCIPLE` (general guidance, not a sourced historical fact). Never describe the last two as directly verified by video evidence.
