# HOMEKU — Reference DNA Summary v1.0 (P1)

> **Status:** production-facing observational knowledge, NOT a generative prompt and NOT an assertion of virality causation.  
> **Tracking:** [Issue #7](https://github.com/milyarderpro/homeku/issues/7) · [P0 roadmap PR #8](https://github.com/milyarderpro/homeku/pull/8).  
> **Snapshot:** `milyarderpro/homeku` at [commit `80072accc56f7824d9575f144ed4e88dcf51a8bc`](https://github.com/milyarderpro/homeku/tree/80072accc56f7824d9575f144ed4e88dcf51a8bc), audited 2026-11-09.  
> **Source priority:** per-video `analysis.yaml` (Schema 2.1, visual observations) → `analysis.md` (human-readable render) → `storyboard.jpg` and `shot-NN.jpg` (visual cross-check). For fine detail, **open the selected source again**; this summary is a retrieval index, not a replacement for it.

## 1. What the corpus can and cannot teach

HOMEKU's DNA is not just house style. It is the **combination of architecture, exterior reveal, environment, interior composition, material/lighting continuity, camera choreography, shot order, edit rhythm, and on-screen visual progression**.

These 58 packages were selected from videos reported by the owner as viral. Their metadata is observational, not an outcome-comparison dataset. **Do not claim that a roof, colour, 5-shot sequence, 6-second opening, or camera movement *caused* millions of views.** No verified per-video retention, audience demographics, audio, music, caption, thumbnail, platform delivery, or experiment/control results are in this corpus. All source `analysis_quality.human_verified` flags are `false` (57 `draft`; 1 `reviewed`); use visual confidence and uncertainty cautiously. Visual appearance does not prove real-world materials, exact floor area, season, or property location.

## 2. Audit coverage and measured baselines

| Audit measure | Observed at snapshot | Interpretation |
| --- | --- | --- |
| Reference packages | **58** (10 historical `VID-XXX`; 48 filename-based) | All 58 contain `analysis.yaml`, `analysis.md`, and `storyboard.jpg` |
| Shot evidence | **300** shot records and **300** per-shot JPEG files | Shot counts agree with package-level image counts; every package has a storyboard |
| Detailed visual descriptors | **6,226** recorded items: 2,850 architectural; 2,504 furniture/props; 872 environment | Items can recur across shots; NOT 6,226 unique objects |
| Video duration | **15.30–27.233s**; median **20.19s**; mean **20.57s** | Approx. 20 seconds is a useful **production target**, not an exact source invariant |
| Shot-count distribution | **3 shots: 1**; **4: 6**; **5: 35**; **6: 14**; **7: 2** | 5 is the mode, not a compulsory number |
| Overall pace labels | **slow: 29**, **moderate: 28**, **slow_to_moderate: 1** | Movement is typically deliberate within scenes, even where the sequence is moderate |
| Opening scene | **58/58** first shots reference an exterior; **5** explicitly combine exterior with living-room entry | Do not count all of a mixed opening as exterior-only time |
| First-shot length bins | **12** below 5s; **33** from 5s to under 6s; **13** at least 6s | These are first-shot spans, NOT measured outdoor-only visibility |
| Pure exterior-coded first shot ≥6s | **8** clear examples: `VID-001`, `VID-002`, `VID-003`, `edh022`, `edh032`, `edh038`, `edh056`, `edh060` | The other five first-shot spans ≥6s include entry-to-interior (`edh016`, `edh026`, `edh031`, `edh035`, `edh036`) |
| Editing pattern | Hard/straight cuts are very common; exceptions include continuous doorway travel and occasional soft/flash transition | **Default production:** clean hard cuts; never imply morphing between rooms |

**Critical correction:** not every source opening is ≥5 seconds. Examples: [`edh019`](../references/edh019/analysis.yaml) 3.97s, [`edh015`](../references/edh015/analysis.yaml) 4.133s, [`VID-004`](../references/VID-004/analysis.yaml) 4.73s. The HOMEKU rule **exterior ≥6 full seconds in final production** is a **new deliberate creative constraint**, not a statistical finding or claim of proven retention benefit. Check true outdoor screen time from generated footage, not merely planned timestamps. Source shot timestamps may be estimated and some shot endpoints differ from the listed container duration by about 0.1–0.15s; use approximate tolerances during analysis, exact viewing during final QA.

## 3. Complete reusable DNA — seven layers

Use all layers to build an original video; **do not stop after selecting an architecture style**. A selected source supports a technique, not a license to copy its house or exact frame.

### DNA-01 · Opening / visual hook

**Observed grammar:** reveal an identifiable, attractive dwelling **from frame one**, usually an establishing wide or three-quarter exterior shot; move deliberately toward the facade, doorway, porch or distinctive feature; let foreground landscaping and facade details create progressive discovery.

- **Wide/full house → tighter entry/facade:** [`edh058`](../references/edh058/analysis.yaml) approaches the terracotta-roof cottage and curved stone walkway; [`VID-001`](../references/VID-001/analysis.yaml) approaches a sage-sided storybook facade; [`edh059`](../references/edh059/analysis.yaml) closes toward the stone cottage's entry/balcony.
- **Foreground parallax → reveal facade:** [`edh060`](../references/edh060/analysis.yaml) starts with tree trunks partly obscuring a trailer-based tiny house and shifts right; [`edh047`](../references/edh047/analysis.yaml) uses foreground trunks and an entry stair; [`edh042`](../references/edh042/analysis.yaml) has leafy canopy, lawn and pathway framing a white tropical facade.
- **Hero feature as destination:** [`edh038`](../references/edh038/analysis.yaml) exterior stairs and rooftop terrace; [`edh020`](../references/edh020/analysis.yaml) pointed arch, stone facade and curved eave; [`edh052`](../references/edh052/analysis.yaml) recessed porch, terracotta-like roof, palms and flowering beds.

**Carry into production:** starting composition, hero feature, foreground/house/background layers, camera path, ending composition, visible architectural attributes, day/lighting, and exterior-only duration. Do not spend opening frames on blank sky, indistinct vegetation, or a long approach without revealing the house. **Target 6.0s+ exterior** for the new workflow.

### DNA-02 · Architecture / character / scale

Record **one primary style**, distinctive massing/roofline, levels/vertical scale, texture/material **appearance**, facade, door/window geometry, porch/stairs/chimney, and visible colour contrast. Use `architecture.building_scale` as a rough visual proportion, not a measured plan. `architecture.common_regions` is a **stylistic association only**, never a verified building location.

Reference families worth retrieving (examples, not exhaustive labels):

| Family | Source IDs | Reusable DNA |
| --- | --- | --- |
| Storybook / rustic stone / alpine | [`edh020`](../references/edh020/analysis.yaml), [`edh025`](../references/edh025/analysis.yaml), [`edh059`](../references/edh059/analysis.yaml), [`edh057`](../references/edh057/analysis.yaml) | prominent gable/arch, stone appearance, wood detail, black gridded glazing, warm lamps against cool landscape |
| Mediterranean / courtyard-capable | [`edh038`](../references/edh038/analysis.yaml), [`edh058`](../references/edh058/analysis.yaml), [`edh053`](../references/edh053/analysis.yaml), [`edh050`](../references/edh050/analysis.yaml) | cream stucco appearance, terracotta-like roof or stone, arches, wood entries, planted paths/terraces |
| Tropical / contemporary | [`VID-005`](../references/VID-005/analysis.yaml), [`edh042`](../references/edh042/analysis.yaml), [`edh052`](../references/edh052/analysis.yaml), [`edh055`](../references/edh055/analysis.yaml) | light masses, broad openings, palms/trees, lawn/plant borders, wood contrast, bright/diffused daylight |
| Modern farmhouse / cottage | [`edh017`](../references/edh017/analysis.yaml), [`edh041`](../references/edh041/analysis.yaml), [`edh060`](../references/edh060/analysis.yaml), [`VID-001`](../references/VID-001/analysis.yaml) | gables or compact masses, calm light palette, dark window hardware, warm wood, porches and practical lighting |
| Compact / loft / open plan | [`edh033`](../references/edh033/analysis.yaml), [`edh060`](../references/edh060/analysis.yaml), [`edh022`](../references/edh022/analysis.yaml), [`edh057`](../references/edh057/analysis.yaml) | efficient combined living/kitchen, loft or terrace where supported, compact bathroom, clear vertical hierarchy |

**Conflict rule:** a support reference can contribute a camera pattern, mood or landscape without importing its whole roof/facade/room geometry. The **primary architecture source + approved Design Lock override incidental support details**. New videos must retain a recognisable HOMEKU visual language while changing the actual layout/massing, combinations, details or landscape to make an original concept.

### DNA-03 · Environment / spatial context

Environment is a co-star, **not generic background filler**. Specify foreground, both house sides, behind the roofline, entry path, beds, trees, fence, distant view, and views **through windows** where observed.

- **Snow + stone + winter woodland:** [`edh020`](../references/edh020/analysis.yaml), [`edh025`](../references/edh025/analysis.yaml), [`edh059`](../references/edh059/analysis.yaml). Snow/trees can recur through the interior windows to connect scenes.
- **Flowering paths and courtyard/garden warmth:** [`edh058`](../references/edh058/analysis.yaml), [`edh052`](../references/edh052/analysis.yaml), [`edh038`](../references/edh038/analysis.yaml). Paths direct attention to the entry; planted borders create visual layers.
- **Tropical foliage and mature-tree framing:** [`edh042`](../references/edh042/analysis.yaml), [`edh047`](../references/edh047/analysis.yaml), [`edh055`](../references/edh055/analysis.yaml).
- **Woodland/forest framing:** [`edh056`](../references/edh056/analysis.yaml), [`edh060`](../references/edh060/analysis.yaml).

**Production consistency:** do not show snow in one exterior and lush tropical palm views from the same house's windows unless the concept explicitly accounts for it. Treat house position, path entry, foreground tree placement, climate/season appearance and exterior light direction as a single scene-world lock.

### DNA-04 · Interior / object relationships / micro-reveals

Room DNA consists of **architecture + objects + positions + camera discovery + views beyond windows**; naming a room is insufficient.

| Scene | Recurring visual role / planned reveal | Source evidence |
| --- | --- | --- |
| Living | Establish lifestyle: sofa/rug/table facing TV/fireplace, windows and/or stairs; either wide→detail or detail→wide | [`edh058`](../references/edh058/analysis.yaml) TV arch → window/seating reveal; [`edh020`](../references/edh020/analysis.yaml) stone fireplace and plaid accents; [`edh047`](../references/edh047/analysis.yaml) double-height mezzanine and stair |
| Kitchen | Show material palette, cabinetry, hood/sink, island/peninsula, window, utensils; move along functional composition | [`edh058`](../references/edh058/analysis.yaml) peninsula→range; [`edh052`](../references/edh052/analysis.yaml) compact cream shaker kitchen; [`edh042`](../references/edh042/analysis.yaml) U-shaped kitchen and sink-window |
| Bedroom | Bed/headboard as focal anchor; reveal window/ceiling/wardrobe/lamps; textiles echo palette | [`edh058`](../references/edh058/analysis.yaml) bed close→beams/side tables; [`edh025`](../references/edh025/analysis.yaml) stone/arch/winter view; [`edh047`](../references/edh047/analysis.yaml) vaulted ceiling and dark framed glazing |
| Bathroom | Vanity/tub/shower/toilet relation and fixtures, mirror/tiles/window; close→wide or wide→hero detail | [`edh060`](../references/edh060/analysis.yaml) vanity→tub pan; [`edh058`](../references/edh058/analysis.yaml) tub→vanity pan; [`edh025`](../references/edh025/analysis.yaml) round window and tub |
| Optional specialty | Laundry/closet/loft/return-to-exterior only when the original concept makes sense | [`edh044`](../references/edh044/analysis.yaml) laundry; [`edh055`](../references/edh055/analysis.yaml) closet; [`edh033`](../references/edh033/analysis.yaml) loft and bath/laundry; [`edh051`](../references/edh051/analysis.yaml) exterior return |

**Master-image implication:** each room needs a specific **hero composition**, not a generic wide interior prompt. Anchor fixed window shape, wall/floor materials, hardware, external view, furniture layout, and object positions. Distinguish verified appearance from material/scale guesses. Do not infer a physically valid floor plan from independent shots; production must invent/check a plausible layout.

### DNA-05 · Cinematic grammar (camera, framing, speed, subject)

- **Main motion:** subtle forward dolly/push and side tracking recur in exterior and some hero close-ups; gentle pan/slide or dolly-out often reveals more of a room. Recorded vocabulary includes `dolly_in/out`, `tracking_left/right`, `pan_left/right`, occasional `tilt_up/down`, with modifiers `slow`, `slight`, `subtle`, `gentle`. Retrieve **actual `shots[].camera.movements` and `speed`** of the chosen sources; do not flatten every shot into the same dolly-in.
- **Framing trajectory A — wide→medium/close:** [`edh058`](../references/edh058/analysis.yaml) exterior and kitchen, [`edh047`](../references/edh047/analysis.yaml) facade and living; works for approaching the architectural focal subject.
- **Framing trajectory B — detail→wide:** [`edh058`](../references/edh058/analysis.yaml) bedroom and bathroom; [`edh044`](../references/edh044/analysis.yaml) living starts on fireplace then shows seating; works for controlled spatial reveal.
- **Framing trajectory C — lateral scan:** [`edh052`](../references/edh052/analysis.yaml) living/kitchen pans; [`edh038`](../references/edh038/analysis.yaml) narrow-room reveals. Avoid too-fast motion, spatial teleports, extreme lens warping and contradictory camera directions.
- **Camera is a narrative tool:** specify **where it starts, what is initially visible, which feature it travels toward/reveals, where it ends, and which objects become newly visible**. A list of motion names alone is not a complete video prompt.
- **Camera confidence matters:** source movement may reflect digital zoom or synthetic movement. Treat it as intended screen motion, not proof of physical rig.

### DNA-06 · Lighting, palette and emotional continuity

Recurring palette families include warm ivory/cream/off-white, light/natural/honey wood, stone-like beige/gray, dark/charcoal/black frames or fixtures, greenery, and selective terracotta/sage/rust accents. These are **combinations and material contrasts**, not a compulsory single beige house. Distinctive exceptions (sage green storybook siding, pink/blush cottage, winter snow, bold tiled roof) may anchor an idea.

- **Outside:** soft overcast/diffuse or bright daylight, readable facade, often glowing wall lanterns under porches; e.g. [`edh058`](../references/edh058/analysis.yaml) clear sun, [`edh020`](../references/edh020/analysis.yaml) cool winter light with warm entry lamps, [`edh056`](../references/edh056/analysis.yaml) forest ambient with glowing windows.
- **Inside:** daylight through visible windows plus warm practical/recessed/pendant/sconce lighting; e.g. [`edh058`](../references/edh058/analysis.yaml), [`edh052`](../references/edh052/analysis.yaml), [`edh047`](../references/edh047/analysis.yaml).
- **Mood:** visual signals of cozy, calm, inviting, warm, orderly and/or bright; the emotional effect is an interpretation, not a measured audience reaction.

**Lock continuity:** choose daylight/weather/season, camera exposure, white balance, wood tone, accent colours, window-frame finish, visible fixture family, and exterior garden view. All generated images and clips must be checked against those anchors.

### DNA-07 · Structure, edit rhythm and scene payoff

The **modal** path is Exterior → Living → Kitchen → Bedroom → Bathroom, but the corpus has meaningful alternatives:

- **Compact standard tour:** [`VID-001`](../references/VID-001/analysis.yaml), [`edh011`](../references/edh011/analysis.yaml), [`edh052`](../references/edh052/analysis.yaml), [`edh059`](../references/edh059/analysis.yaml).
- **Expanded tour:** laundry/closet between core rooms; [`edh044`](../references/edh044/analysis.yaml), [`edh055`](../references/edh055/analysis.yaml), [`edh058`](../references/edh058/analysis.yaml).
- **Open-plan / loft condensation:** [`edh033`](../references/edh033/analysis.yaml), [`edh057`](../references/edh057/analysis.yaml), [`edh060`](../references/edh060/analysis.yaml).
- **Exterior bookend:** [`edh047`](../references/edh047/analysis.yaml), [`edh051`](../references/edh051/analysis.yaml), [`edh056`](../references/edh056/analysis.yaml).
- **Continuous doorway entry exception:** [`edh016`](../references/edh016/analysis.yaml), [`edh026`](../references/edh026/analysis.yaml), [`edh031`](../references/edh031/analysis.yaml), [`edh035`](../references/edh035/analysis.yaml), [`edh036`](../references/edh036/analysis.yaml). Those first-shot durations **include interior**, and cannot validate 6s of exterior alone.
- **Other transition exception:** early [`VID-001`](../references/VID-001/analysis.yaml) soft blur and [`VID-003`](../references/VID-003/analysis.yaml) warm flash/dissolve; these are not the new hard-cut default.

**Micro-narrative:** establish house → confirm livability in living area → reveal kitchen functionality → bedroom comfort → bathroom quality/detail. In a 20s production each shot must deliver a distinct visual payload; redundant views waste the remaining 14s after the 6s exterior hook.

## 4. DNA retrieval rules for idea generation (P2 handoff)

This P1 summary is small enough to read every ideation session. **Then open 2–3 full references** selected for the concept rather than relying on this summary alone.

1. **Primary (1 ID):** supplies the dominant house identity: style, massing, facade, consistent interior materials/window language. Example: `edh058` Mediterranean cottage.
2. **Supporting A (1 ID):** one compatible contribution such as tropical context (`edh052`), winter wooded context (`edh025`), or a compact planning strategy (`edh060`). Explicitly state what was *not* imported.
3. **Supporting B (optional, 1 ID):** provides camera/timing/room-reveal technique or editorial structure, not a contradictory second building.
4. **Check compatibility:** roof vs style, floor count, window shape, facade finish, climate/window views, daylight direction, scale and room layout. If incompatible, keep the primary Design Lock and reject the imported feature.
5. **Force originality:** change distinctive massing/layout, orientation/composition, garden path or feature combinations; never imitate a complete reference frame, sequence or specific house one-to-one.
6. **Record provenance per decision:** `DNA feature → source ID / shot ID / observed fields → intended new use → originality change → uncertainty`.

**Example combination, marked creative hypothesis:** primary `edh058` (warm Mediterranean identity + facade approach); support `edh052` (tropical planted context); optional `edh044` (fireplace detail→wide reveal). The resulting home can be new, but references do not prove this exact mix will outperform alternatives.

### Required per-idea DNA Trace (minimum fields)

| Field | Must include |
| --- | --- |
| `references` | 1 primary + 1–2 supporting IDs and their assigned roles |
| `architectural_dna` | building form/scale/roof, facade, openings, material appearance, colour |
| `environmental_dna` | garden/path/trees/view/weather appearance, foreground/background relations |
| `interior_dna` | room palette + spatial/furniture anchors + view through windows |
| `cinematic_dna` | per-shot start/end framing, camera path/speed, focal subject, reveal direction |
| `editorial_dna` | scene order, time allocations, local cuts, end-frame payoff |
| `lighting_mood_dna` | indoor/outdoor light sources, colour temperature, emotional tone |
| `source_trace` | source video ID, shot ID or top-level field for each chosen feature |
| `new_design_decisions` | what intentionally differs from the cited references |
| `unknowns_and_conflicts` | unproven materials/locations/spatial relationships or incompatible traits |

Avoid generic statements such as "use luxury lighting" or "cinematic camera" without shot-level source evidence and a concrete visual effect.

## 5. Production-facing mapping (contract agreed for P2/P3)

**These are prescriptive HOMEKU production rules, NOT measured properties of all reference videos.**

| Final timeline | Omni clip (local) | Default planned scene | Required DNA |
| --- | --- | --- | --- |
| 00:00–00:06 | A, 0–6s | **Exterior: ≥6s outdoor-only, hook** | whole-house visibility, hero facade, landscape parallax, camera reveal, identity/lighting |
| 00:06–00:10 | A, 6–10s | Living | furniture/layout focal subject; framing and lighting consistent with facade/world |
| 00:10–00:14 | B, 0–4s | Kitchen | coherent cabinetry, window placement, camera path, functional reveal |
| 00:14–00:17 | B, 4–7s | Bedroom | hero bed, window/ceiling reveal, calming light and palette |
| 00:17–00:20 | B, 7–10s | Bathroom | vanity/tub/shower reveal, matching fixture finish, strong end-frame composition |

- **Format:** target 20s at 9:16 from **two 10s Omni Flash generations**. 5 shots and timings are defaults; exceptions require explicit storyboard justification and must keep two 10s clips and first exterior ≥6s.
- **One Design Lock:** roof/massing, level count, window/door system, facade and room materials, palette, climate/window views, light source/direction, approximate layout. The image and video stages must both honour it.
- **Shot-level storyboard:** `clip_id`, `local_start/end_s`, `global_start/end_s`, `scene`, `source_dna`, `first_frame`, `last_frame`, `focal_subject`, `camera_movement/speed`, `architectural+props+environment anchors`, `lighting`, `transition_out`.
- **Clip storyboard:** an ordered summary of its constituent shots. Prompt A instructs 6+4; Prompt B instructs 4+3+3. State **clean hard cut** at boundaries. Avoid an animated morph through walls as a room change.
- **Master image route:** Option A **default** AI creates five coherent images. Option B **only if requested** AI creates five image prompts and reviews user-provided generated images. Same five-approved-image gate.
- **Prompt packaging:** 1 English video prompt per clip; include reference image→shot mapping, global Design Lock, local timing, shot-by-shot camera and reveal, lighting, hard cuts, negative constraints and 9:16/10s output.
- **Generation limits:** model timing, multiple hard cuts, and room identity may fail; never promise that two first tries suffice. QA actual generated exterior screen-time, cuts, absence of morphing, geometry, room count, visual continuity, and final assembled duration. Repair the affected clip first.
- **Production persistence:** no GitHub write without separate, explicit approval; **`save now` belongs only to analysis v1.4**.

### P2 implementation acceptance (derived from this summary)

A production rules/template PR should fail review if it omits **any** of: 2–3 traceable source references; primary-vs-supporting precedence; exterior+environment anchors; framing start **and** end; camera motion **and** speed; room focal subjects and spatial object relationships; daylight/material consistency; order/timing/transitions; Design Lock; both image routes; two separate 10s prompts; QA and uncertainty/originality. The workflow must distinguish **observed DNA** from **creative constraints** and **model-dependent behavior**.

## 6. Source registry — all 58 packages

**Legend:** `E` exterior, `L` living, `K` kitchen, `B` bedroom, `Ba` bathroom, `U` laundry, `C` walk-in closet/wardrobe, `X` return to exterior. `LK` combined living+kitchen shot; `EL` combined exterior→living shot; `Ba/U` bath+laundry shot; `(loft)` combined loft. **Opening** is the duration of the **first annotated shot** (seconds), *not guaranteed exclusive exterior time*. Rows marked `*` are the five exterior→living combined first shots.

| Reference YAML | Primary style (source label) | Video duration (s) | Shots | Opening shot (s) | Annotated sequence |
| --- | --- | ---: | ---: | ---: | --- |
| [VID-001](../references/VID-001/analysis.yaml) | american_storybook_cottage | 20.030 | 5 | 6.200 | E-L-K-B-Ba |
| [VID-002](../references/VID-002/analysis.yaml) | modern_rustic_cottage | 20.900 | 4 | 6.310 | E-L-B-Ba |
| [VID-003](../references/VID-003/analysis.yaml) | american_cottage | 26.500 | 7 | 6.700 | E-L-K-U-B-Ba-C |
| [VID-004](../references/VID-004/analysis.yaml) | organic_modern_cottage | 18.400 | 5 | 4.730 | E-L-K-B-Ba/U |
| [VID-005](../references/VID-005/analysis.yaml) | modern_tropical_villa | 18.850 | 6 | 4.630 | E-L-K-B-Ba-X |
| [VID-006](../references/VID-006/analysis.yaml) | modern_cottage | 21.780 | 5 | 4.550 | E-L-K-B-Ba |
| [VID-007](../references/VID-007/analysis.yaml) | modern_traditional_cottage | 21.500 | 7 | 5.070 | E-L-K-B-C-Ba-X |
| [VID-008](../references/VID-008/analysis.yaml) | modern_cottage | 21.767 | 5 | 4.900 | E-L-K-B-Ba |
| [VID-009](../references/VID-009/analysis.yaml) | modern_tropical_villa | 17.670 | 5 | 5.100 | E-L-K-B-Ba |
| [VID-010](../references/VID-010/analysis.yaml) | modern_storybook_cottage | 20.530 | 6 | 5.100 | E-L-K-B-U-Ba |
| [edh011](../references/edh011/analysis.yaml) | modern_rustic_cottage | 17.530 | 5 | 5.000 | E-L-K-B-Ba |
| [edh012](../references/edh012/analysis.yaml) | modern_contemporary_cottage | 24.400 | 5 | 4.970 | E-L-K-B-Ba |
| [edh013](../references/edh013/analysis.yaml) | whimsical_organic_mediterranean_tower_house | 21.477 | 5 | 4.600 | E-L-K-B-Ba |
| [edh015](../references/edh015/analysis.yaml) | european_rustic_stone_cottage | 20.014 | 5 | 4.133 | E-L-K-B-Ba |
| [edh016](../references/edh016/analysis.yaml) | storybook_cottage | 19.830 | 5 | 9.600* | EL-K-B-Ba/U-X |
| [edh017](../references/edh017/analysis.yaml) | victorian_influenced_american_farmhouse | 19.770 | 6 | 4.830 | E-L-K-U-B-Ba |
| [edh018](../references/edh018/analysis.yaml) | modern_farmhouse_cottage | 17.670 | 5 | 5.070 | E-L-K-B-Ba/U |
| [edh019](../references/edh019/analysis.yaml) | modern_barrel_vault_cottage | 21.480 | 5 | 3.970 | E-L-K-B-Ba |
| [edh020](../references/edh020/analysis.yaml) | storybook_stone_cottage | 18.620 | 5 | 5.070 | E-L-K-B-Ba |
| [edh021](../references/edh021/analysis.yaml) | contemporary_castle_inspired_stone_cottage | 22.800 | 5 | 4.570 | E-L-K-B-Ba |
| [edh022](../references/edh022/analysis.yaml) | contemporary_compact_minimalist_house | 21.830 | 5 | 6.570 | E-LK-B-Ba-X |
| [edh023](../references/edh023/analysis.yaml) | modern_tropical_contemporary | 22.400 | 5 | 4.670 | E-L-K-B-Ba |
| [edh024](../references/edh024/analysis.yaml) | contemporary_modern_farmhouse | 18.250 | 5 | 5.867 | E-L-K-B-Ba |
| [edh025](../references/edh025/analysis.yaml) | rustic_storybook_stone_cottage | 21.082 | 6 | 5.167 | E-L-K-U-B-Ba |
| [edh026](../references/edh026/analysis.yaml) | modern_contemporary | 21.000 | 5 | 9.667* | EL-K-B-C-Ba |
| [edh027](../references/edh027/analysis.yaml) | modern_contemporary | 21.150 | 6 | 5.470 | E-L-K-B-C-Ba |
| [edh029](../references/edh029/analysis.yaml) | contemporary_bungalow_with_modern_farmhouse_influence | 20.107 | 5 | 5.367 | E-L-K-B-Ba |
| [edh030](../references/edh030/analysis.yaml) | mediterranean_inspired_cottage | 20.460 | 5 | 5.000 | E-LK-U-B-Ba |
| [edh031](../references/edh031/analysis.yaml) | modern_contemporary | 27.233 | 5 | 11.333* | EL-K-B-C-Ba |
| [edh032](../references/edh032/analysis.yaml) | contemporary_compact_cottage | 15.300 | 4 | 7.030 | E-L-B-X |
| [edh033](../references/edh033/analysis.yaml) | contemporary_rustic_compact_house | 18.667 | 4 | 5.033 | E-LK(loft)-Ba/U-X |
| [edh034](../references/edh034/analysis.yaml) | modern_cottage | 20.200 | 5 | 5.033 | E-LK-B-Ba-X |
| [edh035](../references/edh035/analysis.yaml) | modern_cottage | 24.770 | 4 | 13.130* | EL-K-B-Ba |
| [edh036](../references/edh036/analysis.yaml) | modern_european_cottage | 27.170 | 5 | 12.500* | EL-K-B-Ba/U-X |
| [edh037](../references/edh037/analysis.yaml) | modern_transitional_with_classical_european_accents | 19.570 | 6 | 5.100 | E-L-K-B-Ba-X |
| [edh038](../references/edh038/analysis.yaml) | rustic_mediterranean_cottage | 23.520 | 5 | 6.000 | E-L-K-B-Ba |
| [edh039](../references/edh039/analysis.yaml) | contemporary_organic_mountain_modern | 20.933 | 6 | 5.300 | E-L-K-U-B-Ba |
| [edh040](../references/edh040/analysis.yaml) | modern_farmhouse | 20.898 | 5 | 4.597 | E-L-K-B-X |
| [edh041](../references/edh041/analysis.yaml) | modern_farmhouse | 22.567 | 5 | 5.367 | E-L-K-B-Ba/U |
| [edh042](../references/edh042/analysis.yaml) | modern_tropical_minimalist | 22.700 | 5 | 5.433 | E-L-K-B-Ba |
| [edh043](../references/edh043/analysis.yaml) | contemporary_european_cottage | 21.830 | 5 | 5.900 | E-L-K-B-Ba |
| [edh044](../references/edh044/analysis.yaml) | english_storybook_cottage | 21.360 | 6 | 5.130 | E-L-K-U-B-Ba |
| [edh045](../references/edh045/analysis.yaml) | contemporary_rustic_cottage | 23.293 | 5 | 5.900 | E-L-K-B-C |
| [edh046](../references/edh046/analysis.yaml) | modern_cottage_with_contemporary_farmhouse_influences | 16.881 | 5 | 5.065 | E-L-K-B-Ba |
| [edh047](../references/edh047/analysis.yaml) | modern_organic_contemporary | 18.900 | 6 | 5.067 | E-L-K-B-Ba/U-X |
| [edh048](../references/edh048/analysis.yaml) | modern_european_cottage | 20.180 | 6 | 5.100 | E-L-K-C-B-Ba/U |
| [edh049](../references/edh049/analysis.yaml) | contemporary_organic_stone_architecture | 19.090 | 4 | 5.530 | E-K-B-Ba |
| [edh050](../references/edh050/analysis.yaml) | spanish_revival_cottage | 18.230 | 5 | 5.470 | E-L-K-B-Ba/U |
| [edh051](../references/edh051/analysis.yaml) | contemporary_mediterranean | 18.370 | 6 | 5.133 | E-L-K-B-Ba-X |
| [edh052](../references/edh052/analysis.yaml) | contemporary_tropical_bungalow | 18.633 | 5 | 5.133 | E-L-K-B-Ba |
| [edh053](../references/edh053/analysis.yaml) | contemporary_mediterranean_villa | 18.633 | 5 | 5.633 | E-L-K-B-Ba |
| [edh054](../references/edh054/analysis.yaml) | contemporary_neoclassical_townhouse | 18.300 | 5 | 5.800 | E-L-K-B-Ba |
| [edh055](../references/edh055/analysis.yaml) | tropical_contemporary_villa | 19.800 | 6 | 5.900 | E-L-K-B-C-Ba |
| [edh056](../references/edh056/analysis.yaml) | modern_rustic_contemporary | 23.700 | 6 | 6.600 | E-L-K-B-Ba-X |
| [edh057](../references/edh057/analysis.yaml) | rustic_alpine_stone_cottage | 18.640 | 4 | 5.100 | E-LK-B-Ba |
| [edh058](../references/edh058/analysis.yaml) | mediterranean_cottage | 19.900 | 6 | 5.300 | E-L-K-B-C-Ba |
| [edh059](../references/edh059/analysis.yaml) | storybook_rustic_stone_cottage | 17.800 | 5 | 5.300 | E-L-K-B-Ba |
| [edh060](../references/edh060/analysis.yaml) | modern_farmhouse_tiny_house | 18.470 | 3 | 8.030 | E-LK(loft)-Ba |

For the full shot list, factual descriptions, camera motion, framing, and uncertainty, open the linked YAML and its sibling Markdown/storyboard. Source labels can be historical or filename-based; **do not allocate or migrate IDs during P1**.

## 7. Gaps and explicit boundaries (do not silently fill)

1. **Virality mechanism unknown:** selection for millions of views is provided by the owner, but performance attributes are not in the YAML. No unsupported "this element guarantees retention" or causal scoring.
2. **No audio/text DNA:** reference analysis expressly excludes audio. Do not invent soundtrack, ASMR, speech, captions, editing sound effects or typography from these files.
3. **No physical property verification:** estimated floor area, real materials, exact building location, true season and physically consistent interior/exterior plan are not proven. Style-associated regions are *not* geography.
4. **First shot ≠ exterior-only time:** mixed entry scenes require separate outdoor timing if you need exterior-only duration; actual output must be checked after generation.
5. **One image ≠ a whole video shot:** keyframe shows one representative point. Read shot start/end framing, camera movement, focal and observation notes in the YAML.
6. **No guaranteed AI edit cuts:** timestamps/hard-cut instructions are targets; generation QA can reject an output even if its prompt was structurally correct.
7. **Data freshness:** this file is grounded in the immutable commit above. Re-audit if new reference packages appear or if analysis YAML materially changes; do not silently recalculate statistics from mutable `main`.
8. **Status:** this is **P1 DNA extraction only**. P2 operational rules and template, P3 pilot, and Google Flow generated footage have NOT been implemented or tested by this change.

**P1 deliverable guarantee:** this summary and source registry cover the observable DNA needed to construct a reference-grounded **visual house tour**, not just a visual house design. P2 must turn each DNA dimension into explicit storyboard and prompt fields, and P3 must validate whether the model actually reproduces them.