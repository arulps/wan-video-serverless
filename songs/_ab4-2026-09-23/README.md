# A/B round 4 (2026-09-23): SEPARATE reference images for the two-child shots. 832x480, seed 30313, same prompts as the song.

The two-child failures (T17/T18/T20 in the 4j batch) put both children on ONE sheet (`kids-16x9.png`). Core ComfyUI
`WanVaceToVideo` uses only the first image of a reference batch, so "separate tiles" needs a node that encodes each
image on its own: `comfy/custom_nodes/wan_vace_multiref.py` (engine `vace`, rows `*_vsep`) or Phantom-Wan-14B,
whose native node already does (engine `phantom`, rows `*_ph`). T17 is the shot that failed at full sampling with the
sheet (boy got Minnu's pigtails, Minnu absent); T07 is the control that HELD at full sampling with the sheet.

| item | rows | what decides |
|---|---|---|
| 1 | T17_vsep, T07_vsep (full), T17_vsep_d (distilled, cheap) | two distinct children in T17 with the right outfits/hair, T07 still fine → separate refs on VACE work; no new model |
| 2 | T17_ph, T07_ph (full), T17_ph_d (distilled) | same test on Phantom; also whether the lightx2v LoRA applies to Phantom (T17_ph_d) |

`ref` column: paths joined with `|`, cast order = ref order (Minnu first, as in the song rows). `engine` column picks the workflow.
