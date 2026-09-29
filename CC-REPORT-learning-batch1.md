# CC-REPORT — Learning batch 1: 69 non-animal learning Shorts on Wan 3.0 (2026-09-29)

Queue `queue\2026-09-29-learning-batch1`. **Result: 69/69 rendered, 0 failed. Estimate $34.50 at list price** (~$24.15 with
the 30% discount; cap $36.00). 720p 9:16 5 s with sound, no upscale, no pod. C1 and F3 were re-rendered with the kids; the
pilot's object-only C1/F3 files are kept under `*-objectonly` names.

## Notes
- **The item-01 `--only` list was garbled:** `D10_w3w3` plus a repeated tail (135 tokens, 70 unique). CC ran the cleaned
  69-ID list. It is exactly the 69 not-done rows of `shots.csv` and the queue's stated count; the dry-run on it gave
  69 rows / `audio=on` / **estimated $34.50**. Please fix `item-01.md`.
- Credentials: `credentials present: True`.
- **Render window:** **13:13:54 → 14:14:15 UTC, 2026-09-29** (09:13:54 → 10:14:15 Toronto EDT). 3 tasks in parallel.
- All 69 have video + audio. No URL or key appears in any sidecar or the log. `shots.csv`: all 72 rows are `done`.
- **Seam method:** OpenCV (`cv2` 4.13), the pilot's one-liner: frame 0 vs the last of 150 frames, mean abs BGR difference, 0–255.
  - Highest: D10_w3 21.4, OP1_w3 19.8, MN4_w3 18.6, FE5_w3 18.0, FM5_w3 14.9.
  - Lowest: SN1_w3 3.1, SN3_w3 3.0, SN2_w3 2.9.
- **Contact sheets:** 5×2, every 15th frame, 216 wide. **Loop previews:** `-stream_loop 2 -c copy`, 15.16 s.
- **Overview:** all 69 contact sheets stacked with the ID on the left, **1190×52992 px, 83 MB**. It is large; Fable may prefer
  the per-Short contact sheets.

## Rows
| row | refs | status | task id | wall s | length | est (list) | seam |
|---|---|---|---|---|---|---|---|
| C1_w3 | 1 | done | `e46b0f78-5dd1-417e-8a18-f2acd8007b46` | 148.4 | 5.0 s | $0.50 | **7.6** |
| C2_w3 | 1 | done | `0828e756-fec3-4233-8549-2f87879742a5` | 146.5 | 5.0 s | $0.50 | **7.3** |
| C3_w3 | 1 | done | `6d9f49b8-3a62-40a0-ae07-928a176a1473` | 146.3 | 5.0 s | $0.50 | **7.2** |
| C4_w3 | 1 | done | `951c5890-03a4-4fee-a6f1-ff2139f4ef38` | 149.8 | 5.0 s | $0.50 | **6.4** |
| C5_w3 | 1 | done | `f26cf1ac-6a8e-41ec-99e3-a33dfa628367` | 146.5 | 5.0 s | $0.50 | **7.3** |
| C6_w3 | 1 | done | `3a2c8244-8352-449b-a9b2-66bf652e4ec0` | 145.1 | 5.0 s | $0.50 | **6.6** |
| F1_w3 | 1 | done | `ac86fb5f-5b51-4ee2-aa56-ced386a3e230` | 146.4 | 5.0 s | $0.50 | **6.7** |
| F2_w3 | 1 | done | `26865db5-47d0-4cd3-83c3-cbd9c487dc76` | 145.8 | 5.0 s | $0.50 | **7.2** |
| F3_w3 | 1 | done | `fc5d9ff1-1a0c-441a-b5e1-164b7ca2a381` | 145.7 | 5.0 s | $0.50 | **7.0** |
| F4_w3 | 1 | done | `a653626c-4163-4087-b538-16f7f1ce239b` | 146.4 | 5.0 s | $0.50 | **7.8** |
| F5_w3 | 1 | done | `589fdfc7-6db7-4715-8854-74d6d40ce6b4` | 146.7 | 5.0 s | $0.50 | **6.6** |
| F6_w3 | 1 | done | `eb0815a2-b422-4e99-922b-7fd82a4e96ec` | 145.9 | 5.0 s | $0.50 | **7.3** |
| V1_w3 | 0 | done | `f2a1b6c9-180e-4927-a503-ff512100d3e2` | 240.3 | 5.0 s | $0.50 | **6.7** |
| V3_w3 | 1 | done | `ecd812b9-6055-4eff-a7a1-30915dd5aedb` | 145.6 | 5.0 s | $0.50 | **6.1** |
| V4_w3 | 0 | done | `36a7be5e-9525-4f02-821d-24ac33f3ee6e` | 254.9 | 5.0 s | $0.50 | **5.1** |
| B1_w3 | 1 | done | `055d99d2-fecd-483e-9408-0735820fda58` | 146.1 | 5.0 s | $0.50 | **14.8** |
| B2_w3 | 1 | done | `f5d06b3b-0944-4a72-9ac2-3d0663dba6ae` | 162.7 | 5.0 s | $0.50 | **7.4** |
| B3_w3 | 1 | done | `5ae4ae5f-f572-467d-88f9-6b0a7e2161fa` | 147.0 | 5.0 s | $0.50 | **11.4** |
| B4_w3 | 1 | done | `df0f1ee9-6da6-474c-942b-c464dfab5ce5` | 147.4 | 5.0 s | $0.50 | **7.3** |
| FM1_w3 | 1 | done | `7ae7a463-1b46-4fbd-ba69-3f4395380ea6` | 146.4 | 5.0 s | $0.50 | **5.1** |
| FM2_w3 | 1 | done | `21d48979-efa0-4923-a78f-116576c61e95` | 161.7 | 5.0 s | $0.50 | **6.5** |
| FM3_w3 | 1 | done | `9527ccf6-bfd6-4fd6-93b5-6fafeaac6ac9` | 145.3 | 5.0 s | $0.50 | **7.1** |
| FM4_w3 | 1 | done | `ddd454c3-542a-49a3-8761-e614a74e02e3` | 146.4 | 5.0 s | $0.50 | **7.2** |
| FM5_w3 | 1 | done | `89965caa-3468-4218-a9d4-aacd2e7a76ec` | 147.3 | 5.0 s | $0.50 | **14.9** |
| SN1_w3 | 0 | done | `5f81de65-185c-4d05-9a4b-df1d7fa29dd0` | 176.6 | 5.0 s | $0.50 | **3.1** |
| SN2_w3 | 0 | done | `1712c907-b6dc-4e1e-b14a-cca0a2aaafce` | 130.2 | 5.0 s | $0.50 | **2.9** |
| SN3_w3 | 0 | done | `64bedb0e-091c-4cce-a6de-65b58951d3e4` | 144.6 | 5.0 s | $0.50 | **3.0** |
| SN4_w3 | 0 | done | `3b4560d3-fd91-4d84-832b-39be6155386f` | 144.8 | 5.0 s | $0.50 | **3.7** |
| SN5_w3 | 1 | done | `94d71899-a232-42ef-aa60-10b6dc1107d8` | 145.5 | 5.0 s | $0.50 | **7.2** |
| SN6_w3 | 0 | done | `0e41389b-29cb-4cb9-95e4-fb23ad65315a` | 128.9 | 5.0 s | $0.50 | **4.9** |
| FD2_w3 | 1 | done | `74c7892a-ced6-41d3-8450-eebcf6c1ca6d` | 146.6 | 5.0 s | $0.50 | **7.1** |
| FD3_w3 | 1 | done | `908cee05-e937-4771-a3ae-fafe329c1e78` | 145.8 | 5.0 s | $0.50 | **6.7** |
| FD4_w3 | 1 | done | `13754f52-8a8e-4fbe-ad60-b3a6485f93d5` | 146.1 | 5.0 s | $0.50 | **7.7** |
| FD5_w3 | 1 | done | `319bed44-038f-4d7e-92ac-1127af5bbaf9` | 145.6 | 5.0 s | $0.50 | **6.6** |
| FD6_w3 | 1 | done | `ec3c63f4-ebeb-4bf7-b79d-7a68bc17a215` | 146.0 | 5.0 s | $0.50 | **8.4** |
| AC1_w3 | 1 | done | `5972af4b-fb0d-422d-ae6f-7d46ed6ecba3` | 145.5 | 5.0 s | $0.50 | **7.7** |
| AC3_w3 | 1 | done | `8d8b9958-a899-47e4-968f-e644c41bd2c8` | 145.7 | 5.0 s | $0.50 | **7.4** |
| AC4_w3 | 1 | done | `c759c2b9-5247-4f39-a507-28d7b9031ea4` | 145.9 | 5.0 s | $0.50 | **10.3** |
| AC5_w3 | 1 | done | `b365e4f1-3065-4a68-aebb-20573f435a4f` | 145.9 | 5.0 s | $0.50 | **12.8** |
| FE1_w3 | 1 | done | `efb6ece8-d676-4196-adc8-a7c4d7040692` | 146.1 | 5.0 s | $0.50 | **10.2** |
| FE2_w3 | 1 | done | `37281f46-839e-410c-9f45-6550a21fe891` | 146.3 | 5.0 s | $0.50 | **7.4** |
| FE3_w3 | 1 | done | `42f3db57-80a0-42bf-91c1-2517520932a9` | 146.5 | 5.0 s | $0.50 | **11.3** |
| FE4_w3 | 1 | done | `68c0fc7e-a663-44d1-b44e-7fbf776e69bb` | 146.8 | 5.0 s | $0.50 | **6.6** |
| FE5_w3 | 1 | done | `239c88a4-951a-4e43-aa6a-3cd6c5cabee1` | 146.9 | 5.0 s | $0.50 | **18.0** |
| OP1_w3 | 1 | done | `9e72782f-0db9-4528-8a74-cff20ce791d6` | 146.7 | 5.0 s | $0.50 | **19.8** |
| OP2_w3 | 1 | done | `b6f63d0b-791b-4ade-8239-22f3645e2cbd` | 146.2 | 5.0 s | $0.50 | **10.5** |
| OP3_w3 | 0 | done | `61d10d7f-9c5d-48e5-a300-b341cd6355db` | 113.6 | 5.0 s | $0.50 | **3.9** |
| OP4_w3 | 1 | done | `3d3590e0-aba1-4427-abcd-0f9138af4999` | 145.9 | 5.0 s | $0.50 | **9.4** |
| OP5_w3 | 1 | done | `66b1ad3a-4ca3-44d6-aa9b-f71886a056a0` | 146.7 | 5.0 s | $0.50 | **9.6** |
| MN1_w3 | 1 | done | `a82e745f-eb0a-4177-a9e4-e25eeb0af8a6` | 162.1 | 5.0 s | $0.50 | **7.8** |
| MN2_w3 | 1 | done | `b1b817c4-5c25-495e-b4c9-07d4ac73be04` | 163.9 | 5.0 s | $0.50 | **11.6** |
| MN3_w3 | 1 | done | `bb8f2204-1af9-4d77-97f9-17f2642798ec` | 145.3 | 5.0 s | $0.50 | **9.9** |
| MN4_w3 | 1 | done | `990bfb03-501f-4a50-8300-6d82ea7c5938` | 162.4 | 5.0 s | $0.50 | **18.6** |
| VG1_w3 | 1 | done | `86ffafab-53f7-48a2-91fa-6746aee96e9c` | 145.8 | 5.0 s | $0.50 | **8.7** |
| VG2_w3 | 1 | done | `2321d416-20ef-455d-a2ba-9bffdecbf5ec` | 162.0 | 5.0 s | $0.50 | **7.2** |
| VG3_w3 | 1 | done | `e2fa1121-9c4d-4a79-b130-9aaf60cd08ab` | 179.3 | 5.0 s | $0.50 | **6.5** |
| VG4_w3 | 1 | done | `44e1ba59-1aa5-45b2-a639-8834e44d5a8b` | 177.5 | 5.0 s | $0.50 | **7.4** |
| VG5_w3 | 1 | done | `e65d53cf-0b06-43ed-a0b4-b4fd153cab2f` | 161.9 | 5.0 s | $0.50 | **6.8** |
| VG6_w3 | 1 | done | `7d4f84e7-25a1-4143-8223-72bb6288cc60` | 177.4 | 5.0 s | $0.50 | **6.9** |
| D1_w3 | 2 | done | `bd5dbc2f-5dbd-468a-8ef6-9eb71658aeda` | 178.4 | 5.0 s | $0.50 | **9.3** |
| D2_w3 | 1 | done | `3e40157f-7b72-4d6a-9e42-3f94faa5e107` | 177.7 | 5.0 s | $0.50 | **7.3** |
| D3_w3 | 1 | done | `0179066e-aa5d-4f26-89b9-e0e15212da00` | 179.3 | 5.0 s | $0.50 | **12.5** |
| D4_w3 | 1 | done | `10dd7c09-29f1-4e8d-9b28-a27c27b6055b` | 161.5 | 5.0 s | $0.50 | **7.2** |
| D5_w3 | 1 | done | `0dd4edca-65be-4d70-b55c-99be5c82c4f3` | 179.6 | 5.0 s | $0.50 | **8.8** |
| D6_w3 | 1 | done | `c04d0a2b-9b4b-4fd0-806d-13baebd41139` | 162.8 | 5.0 s | $0.50 | **8.4** |
| D7_w3 | 1 | done | `e82da181-e94b-4390-8c0d-fc06f7d9cfe7` | 178.2 | 5.0 s | $0.50 | **10.3** |
| D8_w3 | 1 | done | `043bd8ce-4d59-46a9-8ac9-3bb1b4f9f842` | 178.4 | 5.0 s | $0.50 | **10.3** |
| D9_w3 | 1 | done | `f09887fe-9fec-42e2-b8c0-1a4da1dc65a5` | 161.9 | 5.0 s | $0.50 | **7.6** |
| D10_w3 | 1 | done | `0015fe2c-01e0-421c-b7d2-5263475f0c1e` | 148.2 | 5.0 s | $0.50 | **21.4** |

## Paths
Working copies, where `<ID>` is each row above:
- `C:\Projects\opencode\video_image\songs\shorts-learning\out\<ID>-seed30313-w3.mp4` (+ `.json`)
- `C:\Projects\opencode\video_image\songs\shorts-learning\out\_qc\<ID>-strip.png`, `C:\Projects\opencode\video_image\songs\shorts-learning\out\_qc\<ID>-contact.png`, `C:\Projects\opencode\video_image\songs\shorts-learning\out\_qc\<ID>-loop-x3.mp4`
- Log: `C:\Projects\opencode\video_image\songs\shorts-learning\batch_learning1.log`
- Overview: `C:\Projects\opencode\video_image\songs\shorts-learning\out\_qc\learning-batch1-overview.png`

Copies. Each folder gained exactly 3 files; no existing file was hit or overwritten, and the `<ID>-metadata.md` and
`*-objectonly*` files are untouched.
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\C1\C1_w3-seed30313-w3.mp4`, `...\C1\C1_w3-contact.png`, `...\C1\C1_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\C2\C2_w3-seed30313-w3.mp4`, `...\C2\C2_w3-contact.png`, `...\C2\C2_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\C3\C3_w3-seed30313-w3.mp4`, `...\C3\C3_w3-contact.png`, `...\C3\C3_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\C4\C4_w3-seed30313-w3.mp4`, `...\C4\C4_w3-contact.png`, `...\C4\C4_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\C5\C5_w3-seed30313-w3.mp4`, `...\C5\C5_w3-contact.png`, `...\C5\C5_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\C6\C6_w3-seed30313-w3.mp4`, `...\C6\C6_w3-contact.png`, `...\C6\C6_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\F1\F1_w3-seed30313-w3.mp4`, `...\F1\F1_w3-contact.png`, `...\F1\F1_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\F2\F2_w3-seed30313-w3.mp4`, `...\F2\F2_w3-contact.png`, `...\F2\F2_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\F3\F3_w3-seed30313-w3.mp4`, `...\F3\F3_w3-contact.png`, `...\F3\F3_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\F4\F4_w3-seed30313-w3.mp4`, `...\F4\F4_w3-contact.png`, `...\F4\F4_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\F5\F5_w3-seed30313-w3.mp4`, `...\F5\F5_w3-contact.png`, `...\F5\F5_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\F6\F6_w3-seed30313-w3.mp4`, `...\F6\F6_w3-contact.png`, `...\F6\F6_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\V1\V1_w3-seed30313-w3.mp4`, `...\V1\V1_w3-contact.png`, `...\V1\V1_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\V3\V3_w3-seed30313-w3.mp4`, `...\V3\V3_w3-contact.png`, `...\V3\V3_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\V4\V4_w3-seed30313-w3.mp4`, `...\V4\V4_w3-contact.png`, `...\V4\V4_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\B1\B1_w3-seed30313-w3.mp4`, `...\B1\B1_w3-contact.png`, `...\B1\B1_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\B2\B2_w3-seed30313-w3.mp4`, `...\B2\B2_w3-contact.png`, `...\B2\B2_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\B3\B3_w3-seed30313-w3.mp4`, `...\B3\B3_w3-contact.png`, `...\B3\B3_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\B4\B4_w3-seed30313-w3.mp4`, `...\B4\B4_w3-contact.png`, `...\B4\B4_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\FM1\FM1_w3-seed30313-w3.mp4`, `...\FM1\FM1_w3-contact.png`, `...\FM1\FM1_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\FM2\FM2_w3-seed30313-w3.mp4`, `...\FM2\FM2_w3-contact.png`, `...\FM2\FM2_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\FM3\FM3_w3-seed30313-w3.mp4`, `...\FM3\FM3_w3-contact.png`, `...\FM3\FM3_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\FM4\FM4_w3-seed30313-w3.mp4`, `...\FM4\FM4_w3-contact.png`, `...\FM4\FM4_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\FM5\FM5_w3-seed30313-w3.mp4`, `...\FM5\FM5_w3-contact.png`, `...\FM5\FM5_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\SN1\SN1_w3-seed30313-w3.mp4`, `...\SN1\SN1_w3-contact.png`, `...\SN1\SN1_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\SN2\SN2_w3-seed30313-w3.mp4`, `...\SN2\SN2_w3-contact.png`, `...\SN2\SN2_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\SN3\SN3_w3-seed30313-w3.mp4`, `...\SN3\SN3_w3-contact.png`, `...\SN3\SN3_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\SN4\SN4_w3-seed30313-w3.mp4`, `...\SN4\SN4_w3-contact.png`, `...\SN4\SN4_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\SN5\SN5_w3-seed30313-w3.mp4`, `...\SN5\SN5_w3-contact.png`, `...\SN5\SN5_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\SN6\SN6_w3-seed30313-w3.mp4`, `...\SN6\SN6_w3-contact.png`, `...\SN6\SN6_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\FD2\FD2_w3-seed30313-w3.mp4`, `...\FD2\FD2_w3-contact.png`, `...\FD2\FD2_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\FD3\FD3_w3-seed30313-w3.mp4`, `...\FD3\FD3_w3-contact.png`, `...\FD3\FD3_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\FD4\FD4_w3-seed30313-w3.mp4`, `...\FD4\FD4_w3-contact.png`, `...\FD4\FD4_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\FD5\FD5_w3-seed30313-w3.mp4`, `...\FD5\FD5_w3-contact.png`, `...\FD5\FD5_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\FD6\FD6_w3-seed30313-w3.mp4`, `...\FD6\FD6_w3-contact.png`, `...\FD6\FD6_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\AC1\AC1_w3-seed30313-w3.mp4`, `...\AC1\AC1_w3-contact.png`, `...\AC1\AC1_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\AC3\AC3_w3-seed30313-w3.mp4`, `...\AC3\AC3_w3-contact.png`, `...\AC3\AC3_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\AC4\AC4_w3-seed30313-w3.mp4`, `...\AC4\AC4_w3-contact.png`, `...\AC4\AC4_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\AC5\AC5_w3-seed30313-w3.mp4`, `...\AC5\AC5_w3-contact.png`, `...\AC5\AC5_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\FE1\FE1_w3-seed30313-w3.mp4`, `...\FE1\FE1_w3-contact.png`, `...\FE1\FE1_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\FE2\FE2_w3-seed30313-w3.mp4`, `...\FE2\FE2_w3-contact.png`, `...\FE2\FE2_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\FE3\FE3_w3-seed30313-w3.mp4`, `...\FE3\FE3_w3-contact.png`, `...\FE3\FE3_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\FE4\FE4_w3-seed30313-w3.mp4`, `...\FE4\FE4_w3-contact.png`, `...\FE4\FE4_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\FE5\FE5_w3-seed30313-w3.mp4`, `...\FE5\FE5_w3-contact.png`, `...\FE5\FE5_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\OP1\OP1_w3-seed30313-w3.mp4`, `...\OP1\OP1_w3-contact.png`, `...\OP1\OP1_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\OP2\OP2_w3-seed30313-w3.mp4`, `...\OP2\OP2_w3-contact.png`, `...\OP2\OP2_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\OP3\OP3_w3-seed30313-w3.mp4`, `...\OP3\OP3_w3-contact.png`, `...\OP3\OP3_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\OP4\OP4_w3-seed30313-w3.mp4`, `...\OP4\OP4_w3-contact.png`, `...\OP4\OP4_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\OP5\OP5_w3-seed30313-w3.mp4`, `...\OP5\OP5_w3-contact.png`, `...\OP5\OP5_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\MN1\MN1_w3-seed30313-w3.mp4`, `...\MN1\MN1_w3-contact.png`, `...\MN1\MN1_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\MN2\MN2_w3-seed30313-w3.mp4`, `...\MN2\MN2_w3-contact.png`, `...\MN2\MN2_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\MN3\MN3_w3-seed30313-w3.mp4`, `...\MN3\MN3_w3-contact.png`, `...\MN3\MN3_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\MN4\MN4_w3-seed30313-w3.mp4`, `...\MN4\MN4_w3-contact.png`, `...\MN4\MN4_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\VG1\VG1_w3-seed30313-w3.mp4`, `...\VG1\VG1_w3-contact.png`, `...\VG1\VG1_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\VG2\VG2_w3-seed30313-w3.mp4`, `...\VG2\VG2_w3-contact.png`, `...\VG2\VG2_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\VG3\VG3_w3-seed30313-w3.mp4`, `...\VG3\VG3_w3-contact.png`, `...\VG3\VG3_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\VG4\VG4_w3-seed30313-w3.mp4`, `...\VG4\VG4_w3-contact.png`, `...\VG4\VG4_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\VG5\VG5_w3-seed30313-w3.mp4`, `...\VG5\VG5_w3-contact.png`, `...\VG5\VG5_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\VG6\VG6_w3-seed30313-w3.mp4`, `...\VG6\VG6_w3-contact.png`, `...\VG6\VG6_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\D1\D1_w3-seed30313-w3.mp4`, `...\D1\D1_w3-contact.png`, `...\D1\D1_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\D2\D2_w3-seed30313-w3.mp4`, `...\D2\D2_w3-contact.png`, `...\D2\D2_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\D3\D3_w3-seed30313-w3.mp4`, `...\D3\D3_w3-contact.png`, `...\D3\D3_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\D4\D4_w3-seed30313-w3.mp4`, `...\D4\D4_w3-contact.png`, `...\D4\D4_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\D5\D5_w3-seed30313-w3.mp4`, `...\D5\D5_w3-contact.png`, `...\D5\D5_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\D6\D6_w3-seed30313-w3.mp4`, `...\D6\D6_w3-contact.png`, `...\D6\D6_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\D7\D7_w3-seed30313-w3.mp4`, `...\D7\D7_w3-contact.png`, `...\D7\D7_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\D8\D8_w3-seed30313-w3.mp4`, `...\D8\D8_w3-contact.png`, `...\D8\D8_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\D9\D9_w3-seed30313-w3.mp4`, `...\D9\D9_w3-contact.png`, `...\D9\D9_w3-loop-x3.mp4`
- `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\D10\D10_w3-seed30313-w3.mp4`, `...\D10\D10_w3-contact.png`, `...\D10\D10_w3-loop-x3.mp4`
- Overview: `C:\Channel Contents\MinMiniKids\YT Shorts\renders-learning\learning-batch1-overview.png`

## Commit
The `[skip ci]` commit containing this report. It holds `shots.csv` (72× done), `_make_shots.py`, `shots/`,
`REVIEW-learning-pilot-2026-09-29.md`, the queue folder and this report. The hash is in CC's chat reply.

## Not judged
Fable reviews.
