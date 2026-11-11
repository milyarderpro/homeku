# HOMEKU — Reference catalog (58 baseline references)

**Scope:** read-only index of recorded reference metadata. Table values below come from the 2026-11-09 P1 audit snapshot (source commit `80072ac`), not a fresh real-time computation. The source of record for each row is the linked `analysis.yaml`. For source refreshes, use `scripts/refresh_design_catalog.py` and review changes.

**Notation:** E exterior; L living; K kitchen; B bedroom; Ba bathroom; U laundry; C closet; X return exterior; LK combined living/kitchen; EL first-shot exterior-to-living; an asterisk means the first shot spans outdoor and indoor imagery. Camera column is the original **opening-shot motion annotation**, not a generation instruction. Styles and regions are visual classifications, not physical provenance. The format preserves the audit's original compact scene codes.

| Reference | Recorded style | Length (s) | Shots | Opening shot (s) | Annotated scenes | First-shot camera labels |
| --- | --- | ---: | ---: | ---: | --- | --- |
| [VID-001](../references/VID-001/analysis.yaml) | american_storybook_cottage | 20.030 | 5 | 6.200 | E-L-K-B-Ba | `dolly_in + tracking_right` |
| [VID-002](../references/VID-002/analysis.yaml) | modern_rustic_cottage | 20.900 | 4 | 6.310 | E-L-B-Ba | `subtle_dolly_in` |
| [VID-003](../references/VID-003/analysis.yaml) | american_cottage | 26.500 | 7 | 6.700 | E-L-K-U-B-Ba-C | `dolly_in` |
| [VID-004](../references/VID-004/analysis.yaml) | organic_modern_cottage | 18.400 | 5 | 4.730 | E-L-K-B-Ba/U | `dolly_in + slight_tracking_right` |
| [VID-005](../references/VID-005/analysis.yaml) | modern_tropical_villa | 18.850 | 6 | 4.630 | E-L-K-B-Ba-X | `dolly_in + subtle_tracking_right` |
| [VID-006](../references/VID-006/analysis.yaml) | modern_cottage | 21.780 | 5 | 4.550 | E-L-K-B-Ba | `dolly_in` |
| [VID-007](../references/VID-007/analysis.yaml) | modern_traditional_cottage | 21.500 | 7 | 5.070 | E-L-K-B-C-Ba-X | `tracking_right + dolly_in` |
| [VID-008](../references/VID-008/analysis.yaml) | modern_cottage | 21.767 | 5 | 4.900 | E-L-K-B-Ba | `dolly_in + subtle_tracking_right` |
| [VID-009](../references/VID-009/analysis.yaml) | modern_tropical_villa | 17.670 | 5 | 5.100 | E-L-K-B-Ba | `dolly_in + tracking_right` |
| [VID-010](../references/VID-010/analysis.yaml) | modern_storybook_cottage | 20.530 | 6 | 5.100 | E-L-K-B-U-Ba | `dolly_in + slight_pan_right` |
| [edh011](../references/edh011/analysis.yaml) | modern_rustic_cottage | 17.530 | 5 | 5.000 | E-L-K-B-Ba | `dolly_in + slight_tracking_right` |
| [edh012](../references/edh012/analysis.yaml) | modern_contemporary_cottage | 24.400 | 5 | 4.970 | E-L-K-B-Ba | `dolly_in + subtle_tracking_right` |
| [edh013](../references/edh013/analysis.yaml) | whimsical_organic_mediterranean_tower_house | 21.477 | 5 | 4.600 | E-L-K-B-Ba | `tracking_right + subtle_dolly_in` |
| [edh015](../references/edh015/analysis.yaml) | european_rustic_stone_cottage | 20.014 | 5 | 4.133 | E-L-K-B-Ba | `slow_dolly_in` |
| [edh016](../references/edh016/analysis.yaml) | storybook_cottage | 19.830 | 5 | 9.600* | EL-K-B-Ba/U-X | `dolly_in + tracking_right` |
| [edh017](../references/edh017/analysis.yaml) | victorian_influenced_american_farmhouse | 19.770 | 6 | 4.830 | E-L-K-U-B-Ba | `dolly_in` |
| [edh018](../references/edh018/analysis.yaml) | modern_farmhouse_cottage | 17.670 | 5 | 5.070 | E-L-K-B-Ba/U | `tracking_right + subtle_dolly_in` |
| [edh019](../references/edh019/analysis.yaml) | modern_barrel_vault_cottage | 21.480 | 5 | 3.970 | E-L-K-B-Ba | `tracking_right + dolly_in` |
| [edh020](../references/edh020/analysis.yaml) | storybook_stone_cottage | 18.620 | 5 | 5.070 | E-L-K-B-Ba | `dolly_in + tracking_right` |
| [edh021](../references/edh021/analysis.yaml) | contemporary_castle_inspired_stone_cottage | 22.800 | 5 | 4.570 | E-L-K-B-Ba | `tracking_right + slow_dolly_in` |
| [edh022](../references/edh022/analysis.yaml) | contemporary_compact_minimalist_house | 21.830 | 5 | 6.570 | E-LK-B-Ba-X | `dolly_in + tracking_right` |
| [edh023](../references/edh023/analysis.yaml) | modern_tropical_contemporary | 22.400 | 5 | 4.670 | E-L-K-B-Ba | `dolly_in + subtle_tracking_right` |
| [edh024](../references/edh024/analysis.yaml) | contemporary_modern_farmhouse | 18.250 | 5 | 5.867 | E-L-K-B-Ba | `dolly_in + tracking_right + slight_tilt_up` |
| [edh025](../references/edh025/analysis.yaml) | rustic_storybook_stone_cottage | 21.082 | 6 | 5.167 | E-L-K-U-B-Ba | `slow_dolly_in + subtle_tracking_right` |
| [edh026](../references/edh026/analysis.yaml) | modern_contemporary | 21.000 | 5 | 9.667* | EL-K-B-C-Ba | `dolly_in + tracking_right + pan_right` |
| [edh027](../references/edh027/analysis.yaml) | modern_contemporary | 21.150 | 6 | 5.470 | E-L-K-B-C-Ba | `dolly_in + slight_tracking_right` |
| [edh029](../references/edh029/analysis.yaml) | contemporary_bungalow_with_modern_farmhouse_influence | 20.107 | 5 | 5.367 | E-L-K-B-Ba | `dolly_in + slight_tracking_right` |
| [edh030](../references/edh030/analysis.yaml) | mediterranean_inspired_cottage | 20.460 | 5 | 5.000 | E-LK-U-B-Ba | `slow_dolly_in + tracking_right` |
| [edh031](../references/edh031/analysis.yaml) | modern_contemporary | 27.233 | 5 | 11.333* | EL-K-B-C-Ba | `tracking_right + dolly_in + pan_right` |
| [edh032](../references/edh032/analysis.yaml) | contemporary_compact_cottage | 15.300 | 4 | 7.030 | E-L-B-X | `dolly_in + tracking_right + slight_descending` |
| [edh033](../references/edh033/analysis.yaml) | contemporary_rustic_compact_house | 18.667 | 4 | 5.033 | E-LK(loft)-Ba/U-X | `slow_tracking_right + subtle_dolly_in` |
| [edh034](../references/edh034/analysis.yaml) | modern_cottage | 20.200 | 5 | 5.033 | E-LK-B-Ba-X | `tracking_right + subtle_dolly_in` |
| [edh035](../references/edh035/analysis.yaml) | modern_cottage | 24.770 | 4 | 13.130* | EL-K-B-Ba | `dolly_in + pan_left` |
| [edh036](../references/edh036/analysis.yaml) | modern_european_cottage | 27.170 | 5 | 12.500* | EL-K-B-Ba/U-X | `dolly_in + forward_tracking_through_door + gentle_pan_right` |
| [edh037](../references/edh037/analysis.yaml) | modern_transitional_with_classical_european_accents | 19.570 | 6 | 5.100 | E-L-K-B-Ba-X | `tracking_right + dolly_in` |
| [edh038](../references/edh038/analysis.yaml) | rustic_mediterranean_cottage | 23.520 | 5 | 6.000 | E-L-K-B-Ba | `dolly_in + tracking_right` |
| [edh039](../references/edh039/analysis.yaml) | contemporary_organic_mountain_modern | 20.933 | 6 | 5.300 | E-L-K-U-B-Ba | `slow_dolly_in + subtle_tracking_right` |
| [edh040](../references/edh040/analysis.yaml) | modern_farmhouse | 20.898 | 5 | 4.597 | E-L-K-B-X | `slow_dolly_in + subtle_tracking_right` |
| [edh041](../references/edh041/analysis.yaml) | modern_farmhouse | 22.567 | 5 | 5.367 | E-L-K-B-Ba/U | `dolly_in + slight_pan_right` |
| [edh042](../references/edh042/analysis.yaml) | modern_tropical_minimalist | 22.700 | 5 | 5.433 | E-L-K-B-Ba | `slow_dolly_in + subtle_tracking_right` |
| [edh043](../references/edh043/analysis.yaml) | contemporary_european_cottage | 21.830 | 5 | 5.900 | E-L-K-B-Ba | `dolly_in + tracking_right` |
| [edh044](../references/edh044/analysis.yaml) | english_storybook_cottage | 21.360 | 6 | 5.130 | E-L-K-U-B-Ba | `dolly_in` |
| [edh045](../references/edh045/analysis.yaml) | contemporary_rustic_cottage | 23.293 | 5 | 5.900 | E-L-K-B-C | `dolly_in + subtle_tracking_right` |
| [edh046](../references/edh046/analysis.yaml) | modern_cottage_with_contemporary_farmhouse_influences | 16.881 | 5 | 5.065 | E-L-K-B-Ba | `slow_dolly_in + slight_tracking_right` |
| [edh047](../references/edh047/analysis.yaml) | modern_organic_contemporary | 18.900 | 6 | 5.067 | E-L-K-B-Ba/U-X | `slow_dolly_in + tracking_right` |
| [edh048](../references/edh048/analysis.yaml) | modern_european_cottage | 20.180 | 6 | 5.100 | E-L-K-C-B-Ba/U | `dolly_in` |
| [edh049](../references/edh049/analysis.yaml) | contemporary_organic_stone_architecture | 19.090 | 4 | 5.530 | E-K-B-Ba | `slow_lateral_tracking + subtle_orbit` |
| [edh050](../references/edh050/analysis.yaml) | spanish_revival_cottage | 18.230 | 5 | 5.470 | E-L-K-B-Ba/U | `tracking_right + subtle_dolly_in` |
| [edh051](../references/edh051/analysis.yaml) | contemporary_mediterranean | 18.370 | 6 | 5.133 | E-L-K-B-Ba-X | `dolly_in + tracking_right` |
| [edh052](../references/edh052/analysis.yaml) | contemporary_tropical_bungalow | 18.633 | 5 | 5.133 | E-L-K-B-Ba | `slow_dolly_in + subtle_tracking_right` |
| [edh053](../references/edh053/analysis.yaml) | contemporary_mediterranean_villa | 18.633 | 5 | 5.633 | E-L-K-B-Ba | `dolly_in + tracking_right` |
| [edh054](../references/edh054/analysis.yaml) | contemporary_neoclassical_townhouse | 18.300 | 5 | 5.800 | E-L-K-B-Ba | `dolly_in + slight_pan_right` |
| [edh055](../references/edh055/analysis.yaml) | tropical_contemporary_villa | 19.800 | 6 | 5.900 | E-L-K-B-C-Ba | `dolly_in + tracking_right` |
| [edh056](../references/edh056/analysis.yaml) | modern_rustic_contemporary | 23.700 | 6 | 6.600 | E-L-K-B-Ba-X | `slow_dolly_in + gradual_tracking_right` |
| [edh057](../references/edh057/analysis.yaml) | rustic_alpine_stone_cottage | 18.640 | 4 | 5.100 | E-LK-B-Ba | `dolly_in + slight_tracking_right` |
| [edh058](../references/edh058/analysis.yaml) | mediterranean_cottage | 19.900 | 6 | 5.300 | E-L-K-B-C-Ba | `dolly_in + slight_tracking_right` |
| [edh059](../references/edh059/analysis.yaml) | storybook_rustic_stone_cottage | 17.800 | 5 | 5.300 | E-L-K-B-Ba | `slow_dolly_in + tracking_right` |
| [edh060](../references/edh060/analysis.yaml) | modern_farmhouse_tiny_house | 18.470 | 3 | 8.030 | E-LK(loft)-Ba | `tracking_right + subtle_dolly_in` |

The index is a navigation aid. After locating a reference, inspect its YAML, analysis report and original visual frames rather than asserting spatial relationships from the shorthand scene sequence.
