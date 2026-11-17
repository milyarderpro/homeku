# Stage 7 — reader access and maintenance evaluation

The [stage 3 bank](../stage3/cases.json) and its baseline SHA remain frozen. No heldout answer tuning is performed.

Local checks measure entry length, primary navigation, canonical source links and dependency impact. They do not score creative answers.

Remote traces use the same published commit for web and GitHub connector. Each event records actual returned text or an explicit failure. Responses cite excerpts from successful events. Parsed-source comparisons and positive-example retrieval are mechanical checks; uncertainty/creative responses have no automated semantic score.

The evaluating assistant has prior repository context. These are guided route readthroughs and self-assessed answer records, not independent or blind model experiments. consumer_model_accuracy remains null. A failed web fetch is never filled from connector or local files.

Generated results: [local audit](local-report.json) · [remote summary](remote-summary.json).

Web and connector traces are recorded only after the relevant commit is published. Image and search access are tested separately; text access never proves an image was seen.
