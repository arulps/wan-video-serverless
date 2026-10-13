"""Regression test for comfy/prompt_lint.py -- the Row Row W1 failure patterns must FAIL, their fixed versions PASS;
R9 (sizes) and R10 (canon ages, Arul 9 Oct 2026) likewise.
    python tests/test_prompt_lint.py   -> PASS line, exit 0"""
import csv, json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LINT = os.path.join(HERE, "..", "comfy", "prompt_lint.py")
sys.path.insert(0, os.path.join(HERE, "..", "comfy"))
import scale_line as SL  # noqa: E402

T = SL.load()


def sizes(labels):
    return SL.scale_line(SL.cast_for_labels(T, labels)[0])


FAMILY = ["Appa"] * 2 + ["Mintu"] * 2 + ["Minnu"] * 2
FAM = "Images 1–2 are Appa, Images 3–4 are Mintu, Images 5–6 are Minnu. Use the reference images for the look only."
KIDS = "Images 1–2 are Mintu, Images 3–4 are Minnu. Use the reference images for the look only."
CROC = "Image 1 is Modhu the crocodile. Use the reference images for the look only."
BOAT = "Appa sits at one end of the boat and rows with both oars. Mintu and Minnu sit on the bench facing him."
OWN = " Only Appa rows and holds the oars; Mintu and Minnu never row."
CASES = {  # id: (legend, labels, body, expect_fail_rules); "+S" appends the cast's SIZES line to the body
    "kids_only_boat": (KIDS, ["Mintu"] * 2 + ["Minnu"] * 2, BOAT + OWN + " Two-shot of the kids.+S", {"R2", "R3"}),
    "croc_empty_boat": (CROC, ["Modhu"], "Modhu rises beside the boat's wooden side and waves.+S", {"R3"}),
    "no_owner": (FAM, FAMILY, BOAT + "+S", {"R4"}),
    "bad_legend": (KIDS, FAMILY, BOAT + OWN + "+S", {"R1"}),
    "fixed_family": (FAM, FAMILY, BOAT + OWN + "+S", set()),
    "croc_offscreen": (CROC, ["Modhu"], "Modhu waves toward the boat just off-screen.+S", set()),
    # R9: the L05 failure -- no sizes in the prompt; a stale line (Minnu drawn as the old 'big sister'); an unknown character
    "no_sizes": (FAM, FAMILY, BOAT + OWN, {"R9"}),
    "stale_sizes": (KIDS, ["Mintu"] * 2 + ["Minnu"] * 2, "Mintu and Minnu wave. SIZES, the same in every frame: Minnu is a "
                    "little taller than Mintu.", {"R9"}),
    "unknown_char": ("Image 1 is Mintu, Image 2 is Zorbo the robot. Use the reference images for the look only.",
                     ["Mintu", "Zorbo the robot"], "Mintu waves at Zorbo.+S", {"R9"}),
    # Minmini has two sizes (non-human bible v26): either mode's line passes; a line with no Minmini size fails
    "minmini_flying": ("Image 1 is Mintu, Image 2 is Minmini. Use the reference images for the look only.",
                       ["Mintu", "Minmini"], "Minmini flies around Mintu.+S", set()),
    "minmini_perched": ("Image 1 is Mintu, Image 2 is Minmini. Use the reference images for the look only.",
                        ["Mintu", "Minmini"], "Minmini rests on Mintu's palm, close up.+P", set()),
    "set_ref_ok": ("Image 1 is Mintu, Image 2 is the kitchen shelf set. Use the reference images for the look only.",
                   ["Mintu", "the kitchen shelf set"], "Mintu waves.+S", set()),
}

def run():
    bad = []
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "shots")); os.makedirs(os.path.join(d, "refs"))
        json.dump({"audio": "no", "spaces": {"boat": ["Appa", "Mintu", "Minnu"]},
                   "owners": [{"pattern": r"\b(rows|rowing|oars?)\b(?! of)", "owner": "Appa", "space": "boat",
                               "require": "Only Appa"}]}, open(os.path.join(d, "lint.json"), "w"))
        rows = []
        for sid, (leg, labels, body, _) in CASES.items():
            refs = []
            for i, _l in enumerate(labels):
                f = f"refs/{sid}_{i}.png"; open(os.path.join(d, f), "wb").close(); refs.append(f)
            if body.endswith("+S"):
                body = body[:-2] + " " + sizes([x for x in labels if x != "Zorbo the robot"])
            elif body.endswith("+P"):
                body = body[:-2] + " " + SL.scale_line(SL.apply_modes(SL.cast_for_labels(T, labels)[0], {"Minmini": "perched"}))
            open(os.path.join(d, f"shots/{sid}.raw.txt"), "w", encoding="utf-8").write(leg + "\n\n" + body + "\n")
            rows.append(dict(shot_id=sid, ref="|".join(refs), prompt=f"shots/{sid}.raw.txt", duration_s="3",
                             engine="wan3", ref_labels="|".join(labels), audio="no"))
        with open(os.path.join(d, "shots.csv"), "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
        out = subprocess.run([sys.executable, LINT, "--song", d], capture_output=True, text=True, encoding="utf-8").stdout
        # R10: a stale lock line fails the song; the canon one passes
        open(os.path.join(d, "characters.txt"), "w", encoding="utf-8").write(
            "Minnu: girl, 6-8, pigtails; keep exactly as in the reference image.\n"
            "Appa: father, mid-30s; keep exactly as in the reference image.\n")
        out10 = subprocess.run([sys.executable, LINT, "--song", d, "--only", "fixed_family"], capture_output=True,
                               text=True, encoding="utf-8").stdout
        open(os.path.join(d, "characters.txt"), "w", encoding="utf-8").write(
            "Minnu: girl, 5-6, pigtails; keep exactly as in the reference image.\n"
            "Appa: father, mid-30s; keep exactly as in the reference image.\n")
        ok10 = subprocess.run([sys.executable, LINT, "--song", d, "--only", "fixed_family"], capture_output=True,
                              text=True, encoding="utf-8").stdout
    if "FAIL R10 characters.txt: Minnu says '6-8'" not in out10 or "Appa says" in out10:
        bad.append("R10: expected exactly Minnu's stale age to fail:\n" + out10)
    if "R10" in ok10 or "LINT PASS" not in ok10:
        bad.append("R10: the canon lock lines should pass:\n" + ok10)
    cur, got = None, {}
    for line in out.splitlines():
        if line and not line.startswith(" ") and not line.startswith("LINT"):
            cur = line.split()[0]; got[cur] = set()
        elif line.strip().startswith("FAIL R"):
            got[cur].add(line.strip()[5:7])
    for sid, (*_, want) in CASES.items():
        if got.get(sid, set()) != want:
            bad.append(f"{sid}: expected FAIL {sorted(want) or 'none'}, got {sorted(got.get(sid, set())) or 'none'}")
    if bad:
        print(out); print("FAIL:", *bad, sep="\n  "); sys.exit(1)
    print(f"PASS: prompt_lint catches {sum(1 for c in CASES.values() if c[3])} failure patterns + the R10 stale age, "
          f"passes {sum(1 for c in CASES.values() if not c[3])} fixed ones + the canon lock lines")


if __name__ == "__main__":
    run()
