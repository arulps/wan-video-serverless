# item-01 — video_image: verify and commit the scale rule (re-issue 2; line-ending-proof table check)

Repo: `C:\Projects\opencode\video_image`.

1. `py tests\test_prompt_lint.py` must print `PASS: prompt_lint catches 7 failure patterns + the R10 stale age, passes 5 fixed
   ones …`.
   Anything else → **blocked**.
2. `py tests\test_wan3_mock.py` → PASS. `py tests\test_song_cuts_reuse.py` → PASS. These two only check that nothing else
   broke.
3. `py comfy\scale_line.py --song songs\l05-urulai-w3 --shot I1` must print one line that:
   - starts with `SIZES, the same in every frame: Mintu and Minnu are the same height — the tops of their heads are level;`
   - contains `Minmini is a small flying firefly, about the size of a child's hand` and `Baby Potato is about as tall as a
     child's hand`.

   Paste the whole line into the report. Then run it again with `--mode Minmini=perched`: that line must contain
   `Minmini is resting or hovering still close by, up to about half a child's height`. Paste that one too.
4. `py comfy\scale_line.py --song songs\a07-butterfly --shot I2` must say "Mintu, Minnu and Priya are the same height" and
   "Red Butterfly is about the size of a child's head". Paste it.
5. **Table is current** (compared in Python, so CRLF vs LF does not matter — that is what blocked karadi-0):
   ```
   py -c "import sys; sys.path.insert(0,'comfy'); import scale_line as SL; d=open('docs/CHARACTER-SCALE.md',encoding='utf-8').read(); print('TABLE CURRENT' if d==SL.table_md() else 'TABLE DIFFERS')"
   ```
   It must print `TABLE CURRENT`. Anything else → **blocked**, with the output. Do not overwrite or regenerate the doc. Also confirm
   the doc's `a12-karadi-w3` section lists Karadi Mama 1.90 m, the rabbit 0.28 m and the squirrel 0.30 m.
6. **R10 is clean across all songs:** run
   `py -c "import sys,glob; sys.path.insert(0,'comfy'); import prompt_lint as P, scale_line as SL; print(sum(len(P.canon_ages(d, SL.load(d))) for d in glob.glob('songs/[!_]*/') + ['songs/_selftest/']), 'R10 issues')"`.
   It must print `0 R10 issues`. Any other number → **blocked** (list the songs). The `songs\_ab*` folders are archived A/B
   tests and keep their old lock lines on purpose (they are never linted again).
7. Commit with message `scale rule: character sizes + builds in every video prompt (R9/R10), Priya = Minnu height [skip ci]`,
   then push. Add these paths explicitly:
   ```
   comfy/character_scale.json comfy/scale_line.py comfy/prompt_lint.py tests/test_prompt_lint.py
   docs/CHARACTER-SCALE.md docs/PROMPT-PLAYBOOK.md
   songs/l05-urulai-w3/scale.json songs/a07-butterfly/scale.json songs/a12-karadi-w3/scale.json
   songs/row-row-row-your-boat/characters.txt songs/shorts-learning/characters.txt songs/shorts-loops/characters.txt
   songs/twinkle-twinkle/characters.txt songs/_selftest/characters.txt
   queue/2026-10-10-scale-rule queue/2026-10-13-karadi-0-scale-rule queue/2026-10-13-karadi-1-scale-rule
   ```
   Before committing, `git status --short` must show nothing else staged.

**item-01.report.md** must cover:
- each command's last line;
- the two SIZES lines;
- the `fc` result;
- the R10 count;
- the commit hash.
