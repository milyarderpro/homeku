# Stage 7 — reader access and maintenance evaluation

[Local audit](local-report.json) · [Remote summary](remote-summary.json) · [Web trace](web.json) · [GitHub connector trace](github_connector.json) · [Implementation report](../../docs/stage-6-7-report.md)

The [stage 3 bank](../stage3/cases.json) and baseline SHA remain frozen: 24 development and 16 heldout cases. Reference answers are visible to this evaluator. The current execution is a guided batch readthrough, not a blinded consumer-model experiment.

Both routes read candidate commit 217c63a473f5b6d9d967b1cb3372dae355ffed8b. The web route made 34 text requests with 33 successful responses; connector text reads succeeded 32/32. Each read 32 distinct paths. Each recorded 40 responses and passed 26 mechanical checks. Fourteen uncertainty/creative answers per route remain unscored. consumer_model_accuracy is null.

Twelve mechanical checks are known-positive example access, not independent retrieval precision/recall. Fourteen parse exact recorded source values from returned remote text, not physical truth or model reasoning. Same-assistant semantic answers carry actual fetched excerpts but no independent semantic score.

The web manifest was partially returned; only the returned release_id field is verified remotely. Image access, search probes and video playback are distinct from successful text access. No failed read was filled from local source files or the other route.

Characters are tool-returned text for the whole batch, not tokens or isolated per-question cost. Shared reads, prior repository context and visible reference answers prevent independent performance conclusions.

## Repeatable checks

Run python scripts/knowledge_access.py --write after authorized reader/report changes and --check for validation. The validator checks actual excerpts, returned-text hashes, source extraction, release identity and equal commit across routes. It does not judge whether every semantic answer is correct.

Use the same commit in both routes. Record actual tool responses or failures and never synthesize an unavailable page. Source extraction must preserve returned text and line order. Keep partial coverage explicit.

The user selected access checks only for this implementation. Independent benchmarking is explicitly deferred.

## Independent evaluation for a later validation stage

A fresh consumer receives only the repository URL, a question, and either web tools or a GitHub connector. It must not see local files, this bank's expected answers, or an earlier repository conversation. Record its model/build, answer, exact citations, pages/characters and visual access before judging.

Judge source support, observation/inference distinction, unknown handling and creative freedom separately. For creative concepts, evaluate coherent geometry, fixed anchors, light/window world and originality without forcing one reference arrangement. Any later prompt/generator test belongs to evaluation of the external consumer, not to a production workflow stored in this knowledge corpus.

The current trace format intentionally rejects claims of independent model accuracy. A genuinely independent run needs its own declared evaluation method and results; changing a flag on these guided traces is not evidence of independence.
