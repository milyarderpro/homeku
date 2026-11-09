# HOMEKU Production Lite v1.1 — Staged Implementation Plan

> Status: **Proposed / planning only**  
> Tracking: [Issue #7](https://github.com/milyarderpro/homeku/issues/7)  
> Scope: new ideation/production workflow layered **beside** the existing reference-analysis workflow, with no direct change to legacy save behavior.

## 1. Goal and non-goals

Use the 58 currently available `references/<id>/` packages (analysis YAML, Markdown, shot JPEGs, storyboard) to guide **original** house-video ideas and ready-to-use prompts for **Google Flow Omni Flash**, aiming for fast production without building complex infrastructure.

**In scope:** DNA summary, lightweight ideation rules, one production template, two 10-second storyboard/prompt packages, a human-reviewed pilot.

**Out of scope:** training/fine-tuning, embeddings or RAG service, vector database, a new workflow runner/Actions, automatic publication, changing reference YAML schemas, performance prediction without metrics, and automatic Google Flow invocation.

The source-analysis process is immutable for this feature: do not modify `references/`, `video/`, `requests/`, `rules/workflow-analysis.md`, or `.github/workflows/save-analysis.yml`. In particular, **`save now` remains reserved exclusively for approved reference analyses**. Production persistence must be separately authorized.

## 2. Non-negotiable production contract

| Parameter | Required behavior |
| --- | --- |
| Video format | Vertical **9:16**, target final duration **20s** |
| Generation | **2 Omni Flash generations × 10s** (baseline target, not a first-try guarantee) |
| Visual opening | First shot is **exterior** and holds for **at least 6 full seconds** in final video |
| Default clip A | Local 0–6s **Exterior**; 6–10s **Living Room** |
| Default clip B | Local 0–4s **Kitchen**; 4–7s **Bedroom**; 7–10s **Bathroom** |
| Global final timeline | Exterior 0–6; Living 6–10; Kitchen 10–14; Bedroom 14–17; Bathroom 17–20 |
| Storyboard | Two levels: **per-shot** details and **per-10s-generation** sequence |
| Image foundation | One shared **Design Lock**, five approved master images (default scenes: exterior, living, kitchen, bedroom, bathroom) |
| Transition | Intended **hard cuts** between rooms, never architectural morphing as a deliberate transition |
| Main prompts | Exactly **one main video prompt per 10s clip**, containing all its planned shots and reference image mapping |
| DNA provenance | Usually **1 main + 1–2 support reference IDs** from the existing library |
| Creative constraints | Preserve an original architectural identity, consistent materials/geometry, and reference-inspired shot language; no one-to-one copying |

**Exterior is the hook:** it must be visually legible and attractive from the opening frame, not an empty 6-second camera drift. Camera direction should derive from selected references (e.g., dolly/tracking/pan) and the specific house, not force identical movement for every video.

**Timing realism:** text-defined timestamps, hard cuts, and multi-room changes are model instructions, not frame-accurate guarantees. QA must inspect actual output. If the exterior ends before six seconds, the result fails and the affected generation needs revision or reconstruction. The user may trim/edit to achieve exact final duration; do not relabel an imperfect output as passing.

A concept may propose another shot count or clip allocation if well motivated by source DNA, provided the **two 10s clips** and **exterior >=6s** remain satisfied. Document each exception.

## 3. User-facing workflow (one chat per video concept)

### Step 1 — DNA Selection
- User: `Buat 3 ide video baru.`
- AI reads `knowledge/dna-summary.md`, then selects and opens 2–3 relevant original packages (`analysis.yaml`, Markdown, storyboard/keyframes as needed).
- Record exact reference IDs, their role (primary architecture vs complementary landscape, interiors or camera), and observed evidence.
- Do not assert any visual detail or performance metric that has not been observed.

### Step 2 — Idea Generation
- AI proposes **three concise, differentiated Idea Cards** with style/visual hook, reference IDs, DNA used, original elements, proposed 20s scene sequence, and practical generation risks.
- User selects one idea. Do not develop two additional production packages unnecessarily.

### Step 3 — Design Lock & Storyboard
- AI defines one consistent house identity: form/floors/roofline, facade/windows/doors, material/colour palette, landscaping, interior harmony, lighting, and essential spatial relationships.
- AI produces both the **shot-level** and **Clip A / Clip B** storyboard with local timestamps, camera starting/ending view, focal subject, motion/speed, and transition instructions.
- Default schedule uses **6+4s / 4+3+3s**. Exterior duration is a hard validation rule.
- User may request changes before image preparation.

### Step 4 — Master Image Production (two routes)
- **Option A (DEFAULT):** AI generates five original master images, one for each scheduled scene, following Design Lock; display for review. Never force a prompt-only workflow by default when image generation is available.
- **Option B (explicit user request):** AI supplies five detailed English image-generation prompts. User generates images with their chosen image service and uploads them for review.
- Both routes converge only after **five suitable images are reviewed/approved**. Review silhouette, windows, materials, palette, room geometry, landscape, lighting, and mapping to storyboard.
- User can switch between A and B without restarting ideation/storyboard. If an image generation capability is unavailable, explain it truthfully and provide a practical prompt alternative.
- Do not assume separately generated rooms are spatially coherent; check alignment with Design Lock.

### Step 5 — Omni Flash Prompt Packaging
- AI creates **Prompt A (10s)** for Exterior+Living and **Prompt B (10s)** for Kitchen+Bedroom+Bathroom, unless an exception has been documented.
- Each prompt includes:
  1. video identity and master/reference image mapping;
  2. global Design Lock;
  3. local clip timeline and per-shot scene instructions;
  4. start/end framing, camera movement/speed and focal subject;
  5. lighting/material consistency;
  6. explicit hard-cut cues and prohibitions on geometry morphing;
  7. duration 10s, vertical 9:16, no unintended text/logos/people.
- Prompts are in English and ready to copy; explain any model-dependent limitations instead of promising precision.

### Step 6 — User Generate & QA
- User runs **two 10s generations** in Google Flow and may upload the results.
- AI performs visual review of the provided clips; user determines final acceptance.
- Check minimum six-second exterior, all required rooms, hard cuts, no major shape/furniture deformation, house identity, total 20s, 9:16.
- If a clip fails, revise **only the affected prompt/clip** first. Additional generations may be needed; two generations represent baseline attempts, not guaranteed total attempts.
- Assemble approved clips; save a production record to GitHub **only on explicit approval**, using a distinct production request (never `save now`).

## 4. Repository additions — minimal by design

```text
knowledge/dna-summary.md          # phase 1: compact corpus-wide reference patterns + provenance
rules/workflow-production.md      # phase 2: operational workflow/guardrails
templates/production.md           # phase 2: one reusable per-idea template
productions/IDEA-001/production.md # phase 3: first reviewed and authorized pilot only
```

No new database, server, queue, Github Actions, or automation. Keep image/video binaries outside the repo initially and place accessible references/links in the Markdown record where appropriate.

### DNA summary content contract
A compact, source-backed index of:
- architecture/style/scale (remember `common_regions` is stylistic association, **not real property location**);
- exterior design, colours/material appearance, landscape/environment;
- interior continuity and mood;
- camera movement, framing, pace, scene sequences, hard cuts;
- exterior timing/hook observations with reference IDs and explicit uncertainty;
- a short set of reusable **patterns**, **exceptions**, and **not yet proven** performance hypotheses.

Use only claims observable from library files; a dataset curated for popularity does not isolate causation behind views.

### Production template content contract
`templates/production.md` should provide sections for:
1. metadata, status, concept ID and approved route A/B;
2. 3 candidate Idea Cards and selected choice;
3. 1 primary + 1–2 supporting references and DNA traces;
4. immutable-for-prompting Design Lock;
5. shot-level storyboard with per-clip local timestamps and global final timestamps;
6. five image descriptors / images or prompts, revision and approval notes;
7. Prompt A / Prompt B (input references, timing, constraints);
8. QA checklist, retake notes, final review outcome and explicit save approval.

## 5. Staged PR delivery plan and acceptance gates

| Phase / suggested PR | Deliverable | Acceptance gate |
| --- | --- | --- |
| **P0 — this PR** | Issue + documentation of plan, scope, sequencing and invariants | Plan approved; **no reference/save workflow changes** |
| **P1 — DNA summary** | `knowledge/dna-summary.md` extracted from all 58 currently present packages | All available references accounted for; high-level pattern claims trace to reference IDs; uncertainties explicit |
| **P2 — workflow + template** | `rules/workflow-production.md` and `templates/production.md` | End-to-end mock walkthrough; Option A default, B explicit; exterior ≥6s; clip A 6+4, B 4+3+3; persistence isolated |
| **P3 — pilot** | 3 ideas → one selected → approved Design Lock, 5 images, 2 prompts, `productions/IDEA-001/production.md` only with permission | Pilot prompts ready; user-generated clip QA conducted; regressions documented; no unsupported success claims |
| **P4 — readiness review** | Pilot learnings and targeted corrections to rules/template | Visual checklist passes and production can repeat without re-analyzing 58 files each time |

**Incremental review principle:** implement each phase in a small focused PR; Phase 1 and Phase 2 should not be silently marked complete by merging the P0 documentation PR.

## 6. Acceptance checklist and practical failure cases

- [ ] New idea cites the selected reference IDs and explains DNA elements actually used.
- [ ] Exterior has **>=6s of real screen time** in the final composition and opens with a legible visual hook.
- [ ] Both 10-second clip storyboards add up correctly and use **local** clip timestamps.
- [ ] Design Lock maintains one believable house identity across exterior/interior.
- [ ] Either **direct images (A, default)** or **five prompts + uploaded images (B)** reaches the same approved-images gate.
- [ ] Prompts have unambiguous image→shot mapping and hard-cut instructions.
- [ ] If Omni ignores a cut/shot, the result is flagged failed and a localized retake is proposed; no fabricated "success".
- [ ] `save now` and historical analysis/Action paths are unaffected.
- [ ] No unsanctioned production writes, unverified claims about viral causation, or new infrastructure.

### Example daily dialogue

```text
User: Buat 3 ide video rumah baru berdasarkan DNA HOMEKU.
AI: 3 ideas + references + DNA reasons.
User: Pilih IDEA-001.
AI: Design Lock + 2 clip storyboards, exterior at least 6s.
User: Setuju. Buat master image.
AI: Option A (default) = 5 images and review.
      OR User: Buat image prompts.
AI: Option B = 5 prompts; review uploaded images.
User: Gambar sudah sesuai; buat prompt Flow.
AI: Prompt A / Prompt B, 10s each.
User: [Uploads Flow results for QA.]
AI: QA with findings; targeted revision where needed.
```

## 7. Change control

- `references/` is a read-only evidence library for this feature.
- Do not repurpose reference analysis fields, GitHub request files, or Action saves for production.
- Any requested persistent production update requires explicit approval identifying the target production record.
- Keep this plan and linked issue current during staged rollout, but distinguish **planned**, **implemented**, **tested**, and **approved** status.
