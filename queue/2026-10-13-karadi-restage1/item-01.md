# item-01 — keep the old takes, checks, render V1A + V2A + V3A + V4A, sheets (≤ $2.50 list)

1. **Keep the old takes** (rename, never copy over or delete):
   - in `songs\a12-karadi-w3\out\`: `V1A-seed30313-w3.mp4/.json` → `V1A-seed30313-w3-v1-picnic.mp4/.json`, and the same for V2A, V3A and V4A;
   - in `out\_qc\`: every `V1A-*`, `V2A-*`, `V3A-*` and `V4A-*` file → the same name with `-v1-picnic` before the extension.

   Report the renamed files.
2. **Rev 1.5 is in place** (verify, don't edit):
   - `shots.csv` status is `todo` for V1A, V2A, V3A and V4A, and `done` for the other 14 rows;
   - `shots\09_V1A.raw.txt` contains "tall wildflowers";
   - `shots\11_V2A.raw.txt` contains "bees' nest";
   - `shots\13_V3A.raw.txt` contains "ankle-deep water";
   - `shots\15_V4A.raw.txt` contains "among the blueberry bushes".

   Any mismatch → **blocked**.
3. `py tests\test_wan3_mock.py` → PASS. Credentials check → True (print only True/False).
4. `py tests\test_prompt_lint.py` → PASS; `py comfy\prompt_lint.py --song songs\a12-karadi-w3` → `LINT PASS: 18 shots, 0 fail, 0 warn`.
   Any failure → **blocked**.
5. Dry-run: `py comfy\batch_runner.py --song songs\a12-karadi-w3 --only V1A,V2A,V3A,V4A --hosts api --dry-run` must show:
   - 4 rows, all 6 s `720P 16:9 audio=off`;
   - refs: V1A 2 (Minnu, Karadi Mama), V2A 2 (Mintu, Karadi Mama), V3A 5, V4A 5 — **no** `10-forest-picnic-set` in any of the four;
   - "estimated $2.40";
   - no `ERROR`, `unknown cast`, `MISSING`, `OVER BUDGET`, `refused` or `Traceback`.

   Otherwise → **blocked**.
6. Render:
   ```
   py comfy\batch_runner.py --song songs\a12-karadi-w3 --only V1A,V2A,V3A,V4A --hosts api --max-usd 2.50 --timeout-min 50 2>&1 | tee songs\a12-karadi-w3\batch_restage1.log
   ```
7. For each rendered clip, write into `out\_qc\`:
   - `<ID>-contact.png`;
   - `<ID>-every4-all.png` (every 4th frame, frame number burned in, 192 wide, 10 per row);
   - 100 % stills of frames 0, 30, 60, 90, 120, 150 and 179.

   Same tools as before.

**item-01.report.md** must cover:
- the renames;
- the checks;
- the dry-run rows;
- a table with one row per clip: task id, status, wall s, frames;
- every failure line verbatim (e.g. `IPInfringementSuspect`);
- the runner's final estimate.
