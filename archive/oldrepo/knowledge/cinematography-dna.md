# Cinematography and visual-storytelling DNA

This file records **source shot language**, visual interpretations and separately labeled general framing principles. It does not prescribe editing durations, mandatory movements, platform controls or a video-generation workflow.

## Composition and camera evidence

| Source / shot | Observed annotation | Visual reading |
| --- | --- | --- |
| [edh058 shot-01](../references/edh058/analysis.yaml) | `wide_front_three_quarter_view_from_lawn` → `medium_close_view_of_front_entry`; `dolly_in` + `slight_tracking_right` | Exterior scale gives way to entrance and path detail |
| [edh060 shot-01](../references/edh060/analysis.yaml) | `tracking_right` + `subtle_dolly_in`, foreground tree trunks | Near trunks shift relative to facade, revealing it across the view |
| [edh058 shot-03](../references/edh058/analysis.yaml) | Kitchen starts wide with peninsula/window, ends closer to range/cabinets | Focal shift trades global layout for cooking detail |
| [edh058 shot-04](../references/edh058/analysis.yaml) | `dolly_out` from bed detail to wider room | Wider ending reveals bedside furniture and beam/window composition |
| [edh060 shot-03](../references/edh060/analysis.yaml) | `pan_right` from vanity/toilet toward bathtub | Lateral visual discovery within a tight bathroom |
| [edh044 shot-02](../references/edh044/analysis.yaml) | Living interior focal fireplace/seating reveal | Architectural focal point broadens into an inhabitable area |

## Distinct concepts

- **Framing:** what the image contains at the beginning and end; wide/medium/close labels vary among annotated videos.
- **Visual reveal:** additional information becomes legible as objects enter/leave frame; may involve camera translation, rotation, changes of distance, occlusion, or synthesis.
- **Parallax:** relative displacement of nearer and farther objects; a clue but not conclusive proof of real-world camera movement.
- **Narrative ordering:** many sources introduce exterior then living, kitchen and private rooms; [edh060](../references/edh060/analysis.yaml) combines living/kitchen/loft and [edh047](../references/edh047/analysis.yaml) revisits exterior.
- **Transitions:** straight cuts often appear, with observed variations including blur/dissolve in [VID-001](../references/VID-001/analysis.yaml) and [VID-003](../references/VID-003/analysis.yaml). No transition is universal.

**Interpretation:** visual storytelling derives from how identity, environment, function and intimate detail are disclosed in sequence. It does not imply that a particular sequence or shot length caused audience retention. Camera names in YAML are visual-motion labels, not equipment verification.

## Motion, subject size and framing

DESIGN_PRINCIPLE / geometric reasoning: relate the camera's change of position or direction to a named subject and the information visible around it. Distinguish the subject's apparent size, the lens field of view, and the amount of scene information revealed.

Under a simplified fixed-viewing-angle model, with an unchanged lens/zoom and the same stationary subject, moving closer generally makes that subject larger in the image; moving farther away generally makes it smaller. The part of the subject's plane covered by the frame changes with distance. This does not mean the lens's angular field of view has changed.

| Change | Expected visual relationship under those assumptions |
| --- | --- |
| Dolly in toward the subject | Subject grows; its surrounding context may become tighter |
| Dolly out away from the subject | Subject becomes smaller; more surrounding context may fit, subject to occlusion |
| Pan or tilt | Viewing direction changes; different surfaces or objects enter the frame |
| Lateral tracking | Relative depth, overlap and occlusion may change; it does not inherently zoom the lens |
| Zoom from a fixed camera position | Subject size and field of view change without the camera translation of a dolly |

These are conditional relationships, not a classifier that overrides source annotations. Combined movements, changing targets, object motion, occlusion and generated deformation can produce different apparent changes. Saved camera labels remain interpretations, not certified physical camera paths.

### Revealing more does not always mean a wider field of view

An advancing camera can reveal previously hidden objects by clearing a foreground obstruction. The newly visible information can increase while the principal subject also grows. That is a deocclusion reveal, not necessarily a widening of the lens field of view.

Hypothetical examples, not additional observations from a source:

- A wide view toward a kitchen becomes medium-wide as the camera approaches the same kitchen with unchanged zoom: the named subject grows.
- An advancing viewpoint clears a foreground column and reveals more seating: the obstruction and what becomes visible explain the reveal.
- “Medium-wide to wide because of dolly in,” without identifying a changed target, reduced occlusion or another reason, leaves the visual relationship underspecified. It is not enough to equate the word “in” with “more room becomes visible.”

Wide, medium and close describe framing relative to a subject; they are not measured lens specifications. A useful description identifies which subject or scene extent the label refers to.

### Opposite views and camera paths

Looking north from living toward kitchen and looking south from kitchen toward living can describe reciprocal views of one house. They do not by themselves establish identical start/end positions or prove that the camera retraces the same segment.

In a new design, a shared circulation axis, opposite viewing directions and an exactly reversed path are different relationships. Screen-left/right may reverse with viewing direction; the house's windows, walls and fixed anchors retain their design positions. Objects behind the camera or outside its framing need not remain visible.

These principles support precise visual descriptions. Project decisions about camera positions, chosen framing and consistency between final prompts remain with the external consumer.

## Corpus-linked enrichment

Start/middle/end evidence distinguishes recorded camera labels, observed sampled framing, unknown object motion and edited transitions. VID-001 includes transition blur at the end of its first sampled shot. These samples do not certify a physical camera path.

See [counted patterns and diversity](corpus-patterns.md) and [source-bound design evidence](design-evidence/README.md). Counts describe published video references; content independence and physical-house identity are not established by unique file hashes.
