# Mazhai VACE prompts
These are VACE (vace-14B, reference-to-video) prompts for three Mazhai shots.
Built from the SHARED BLOCKS + SHOT LIST in MAZHAI-OPENART-RUNSHEET.md.
No AUDIO block (this model has no audio) and no NEGATIVE block in the prompt.
Positive prompt: `-PromptFile prompts\mazhai\<name>.txt`.
Negative prompt: `-NegativePromptFile prompts\mazhai\NEGATIVE.txt`.
Refs: Minnu's four turnaround views plus Mintu's single lawn front view,
passed together via `-Refs`.
I1-opening-backview.txt is a two-child shot; V1a and V2c are solo shots.
Each file ends with a CHARACTERS lock line naming only that shot's cast.

-v2 files (2026-09-22): VACE takes camera language literally — the runsheet's "back three-quarters to camera" produced an over-the-shoulder shot with the head cropped. The -v2 prompts state camera position, framing (whole body / head to knees, never crop the head) and the contact (palms on the glass) explicitly. Use -v2 for VACE; the originals are kept for reference.
