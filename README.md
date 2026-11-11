# HOMEKU — Design Intelligence v2.0

**A source-grounded visual design knowledge repository** for reasoning about original, architecturally coherent house concepts using a curated collection of 58 annotated home-tour references. HOMEKU stores *design evidence and intelligence*, not a video-generation workflow.

## Read the knowledge

Start at **[knowledge/README.md](knowledge/README.md)**. The knowledge library covers architectural form/scale, landscape and window-world, room and furniture relationships, spatial coherence, camera/visual narrative, design compatibility and creative originality.

- [Cross-reference DNA synthesis](knowledge/dna-summary.md)
- [Catalog of 58 reference sources](knowledge/reference-catalog.md)
- [58 detailed source design signatures](knowledge/reference-profiles/README.md)
- [Traceable evidence index](knowledge/evidence-index.yaml)
- [Evidence and uncertainty methodology](knowledge/methodology.md)

The original evidence is at `references/<ID>/analysis.yaml`, with `analysis.md`, `storyboard.jpg`, and one `shot-NN.jpg` per annotated shot. `video/` holds source recordings. **Recorded annotations, material identities, dimensions and inferred camera movement are not fully human-verified.**

## Separation of responsibility

| This repository provides | This repository does **not** provide |
| --- | --- |
| Source observations and traceable design patterns | Production video workflow or approval gates |
| Design reasoning about geometry, style and landscape | Generator-specific parameters or frame schedules |
| Distinctions between observation, inference and creative principle | Image/video prompt templates and audio instructions |
| Originality and compatibility knowledge | Proof that a visual feature causes virality |

An external **Master Prompt** or creative brief can use this library; that prompt remains the independent control layer and may change without modifying the underlying design knowledge.

The 58 references were selected for perceived/reported strong performance, but the repository does not contain verified platform-level views, watch time, completion or causal tests. Do **not** describe any roof style, color, framing or duration as a proven formula for viral reach.

## Add new source analyses (ingestion, not production)

The existing visual-source analysis pipeline remains functional:

1. Upload an original MP4 to `video/<filename>.mp4`, and analyze it with [rules/workflow-analysis.md](rules/workflow-analysis.md), [rules/analysis.md](rules/analysis.md), [templates/video-analysis.yaml](templates/video-analysis.yaml), [templates/analysis.md](templates/analysis.md), and [templates/shot-narratives.json](templates/shot-narratives.json).
2. Review the draft YAML and Indonesian per-shot narratives. In this workflow only, a separate exact **`save now`** message authorizes one immutable pending request in `requests/pending/`. The existing GitHub Actions publish the verified reference package.
3. A saved reference does **not** automatically alter Design Intelligence. Run `python scripts/refresh_design_catalog.py --check` to inspect the current catalog, then `--write` for an explicit catalog refresh; review new patterns and update appropriate knowledge/evidence entries before accepting a revised knowledge snapshot.

Existing `references/`, `video/`, `requests/`, schemas, scripts, analysis rules and save workflow are retained. See [analysis workflow v1.4](rules/workflow-analysis.md) for permission, consistency and recovery behavior.

## Quality checks

```sh
python scripts/refresh_design_catalog.py --check
python -m unittest discover -s tests -v
```

A catalog refresh is deterministic and uses source YAML; AI-authored interpretations require separate review. The [evidence methodology](knowledge/methodology.md) explains source quality and the limits of any claim.
