# Stage 3 evaluation baseline

The bank was fixed on release 2026-11-17-stage-1-2-r2 before the stage 3–5 enrichment was built. The baseline records its SHA-256; the evaluator rejects later bank edits. Development and heldout labels were assigned before enrichment and search was not tuned on either split.

[Question bank](cases.json) · [Baseline](baseline.json) · [Current local checks](current.json)

There are 40 AI-authored cases: 24 development and 16 heldout.

| Cases | Measurement |
| --- | --- |
| 12 retrieval | Recall of specified positive examples using the local bilingual prototype; result precision is not measured |
| 14 recorded source values | Exact equality to saved source fields; this is not verification of physical truth |
| 8 unknown source facts | Authored reference answers only; consumer-model responses not captured |
| 6 creative boundaries | Authored reference answers only; consumer-model responses not captured |

The pilot covers VID-001, VID-004, VID-005, edh013, edh020, edh022, edh033, edh042, edh054, edh058, edh059 and edh060. It spans perceived scales, curved/rectilinear forms, loft/shared functions, separate rooms, different light/environment appearances and an endpoint transition.

Baseline: 26/26 automated local checks passed. The remaining 14 cases are unscored. consumer_model_accuracy is null. A heldout label does not turn these local source checks into a blinded AI-consumption experiment.

Run the maintenance evaluator with python scripts/evaluate_knowledge.py --write current. These evaluation files are outside the consumer knowledge corpus. Stage 6–7 must test web and GitHub connector consumption separately on the same published commit, including actual responses, citation support, uncertainty handling and creative freedom. No remote/model accuracy gain is claimed here.
