# AI review scope

[Evidence coverage](../design-evidence/README.md) · [Corpus patterns](../corpus-patterns.md) · [Methodology](../methodology.md)

The numeric coverage below describes the initial 2026-11-17-stage-3-5 pass. The linked coverage report is authoritative for the current snapshot.

Review records explain which source claims were inspected and which remain uncertain. They are not a global verification flag, and they never exclude a source from creative inspiration.

- visual-notes.json records the selected characteristics actually inspected in the original storyboards during this implementation.
- temporal-notes.json records the sampled progression actually inspected in the twelve pilot contact sheets, covering 59 shots and 177 sampled instants.
- Each source has a generated review record with its annotation/video hashes, inspected media hashes, date, method, scope and findings.
- Codex AI performed this inspection. The runtime does not expose an exact model build; model_version is null rather than an invented identifier.

A supported finding concerns the described characteristics only. Other tags at the same source field have not all been rechecked. Approximate dimensions, geological material composition, structural feasibility and physical-building identity remain unknown. No factual source correction was established by this limited pass, so original analysis packages were preserved.

In that initial pass, all 57 source storyboards were inspected. Start/middle/end frames exist for all 295 shots; only the twelve pilot sources have a new sampled-temporal visual review. The other 45 are explicitly pending temporal review. Continuous playback, every intermediate frame and exact camera mechanics have not been independently revalidated in this pass.

A mechanical difference between overview scene aliases and shot labels is recorded separately as an annotation discrepancy, not a new visual review. In edh060, richer overview aliases differ from two shot scene labels; this does not establish an erroneous room description.

Confidence qualifies a source claim. A new concept may choose natural stone, a new layout or a coherent hybrid style even when the original composition or plan is unknown. No manual verification is required.

If a video, annotation or inspected image changes, hash validation rejects its old review binding. Rebuilding generated files cannot create a new AI inspection: new review notes must describe evidence actually viewed.
