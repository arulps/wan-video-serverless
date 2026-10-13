# item-02 — oviyan: Priya's canon height 1.15 → 1.02 (bible v62)

Repo: `C:\Projects\oviyan`.

1. Run `git status --short`, `git diff --stat` and `git log -1 --format=%h` and record all three in the report. Fable has already
   changed exactly these three files:
   - `docs/CHARACTER-HEIGHTS.md`
   - `src/data/characterCanon.ts`
   - `src/engine/__tests__/characterCanon.test.ts`

   If any of the three shows changes that are **not** about Priya's height or the v62 bible pin, it means another thread has
   uncommitted edits in the same file → **blocked**. Do not commit someone else's work.
2. `npx vitest run src/engine/__tests__/characterCanon.test.ts` → all pass. Any failure → **blocked**, with the output.
3. **Find other places that still assume Priya is 1.15 m or taller than Minnu:**
   - `git grep -n -i "priya"` over `src/`, `docs/` and `tools/`;
   - `git grep -n "1\.15"` over the same paths.

   List every hit in the report. **Do not change any of them.** Fable decides on each one.
4. Run the full suite: `npx vitest run`.
   - Report the pass/fail totals.
   - If a test that this change touches fails (anything that asserts Priya's height), → **blocked**.
   - Report failures elsewhere that also fail on the previous commit as "pre-existing", and do not block on them. To check:
     `git stash` → run that one test → `git stash pop`. Stash **only** if `git status` showed no other changes in step 1;
     otherwise just report the failure.
5. Commit only those three files, with the message format from `docs\DISPATCH-CONVENTIONS.md`. Subject: "canon: Priya same
   height as Minnu, 1.02 m (bible v62, Arul 2026-10-09)". Then push.
6. Do **not** touch the vault/DB. In the report:
   - remind Arul to set Priya's vault height in the Oviyan UI (Vault → Priya → Edit → Height 1.02);
   - list any Chiku (mouse) or Minmini (firefly) size you can see in the repo without the DB: `git grep -n -i "chiku\|cartoon
     mouse\|firefly mascot"` over `src/` and `tools/`.

   Non-human bible v26 corrects Chiku to 0.10 m and makes Minmini a hand-sized flier, with 0.50 m only when still.

**item-02.report.md** must cover:
- the git status/diff summary;
- the canon test result;
- the full-suite totals;
- every grep hit, verbatim;
- the commit hash.
