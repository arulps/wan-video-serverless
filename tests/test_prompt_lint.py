"""Regression test for comfy/prompt_lint.py -- the Row Row W1 failure patterns must FAIL, their fixed versions PASS.
    python tests/test_prompt_lint.py   -> PASS line, exit 0"""
import csv, json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LINT = os.path.join(HERE, "..", "comfy", "prompt_lint.py")
FAM = "Images 1–2 are Appa, Images 3–4 are Mintu, Images 5–6 are Minnu. Use the reference images for the look only."
KIDS = "Images 1–2 are Mintu, Images 3–4 are Minnu. Use the reference images for the look only."
CROC = "Image 1 is Modhu the crocodile. Use the reference images for the look only."
BOAT = "Appa sits at one end of the boat and rows with both oars. Mintu and Minnu sit on the bench facing him."
OWN = " Only Appa rows and holds the oars; Mintu and Minnu never row."
CASES = {  # id: (legend, labels, body, expect_fail_rules)
    "kids_only_boat": (KIDS, ["Mintu"] * 2 + ["Minnu"] * 2, BOAT + OWN + " Two-shot of the kids.", {"R2", "R3"}),
    "croc_empty_boat": (CROC, ["Modhu"], "Modhu rises beside the boat's wooden side and waves.", {"R3"}),
    "no_owner": (FAM, ["Appa"] * 2 + ["Mintu"] * 2 + ["Minnu"] * 2, BOAT, {"R4"}),
    "bad_legend": (KIDS, ["Appa"] * 2 + ["Mintu"] * 2 + ["Minnu"] * 2, BOAT + OWN, {"R1"}),
    "fixed_family": (FAM, ["Appa"] * 2 + ["Mintu"] * 2 + ["Minnu"] * 2, BOAT + OWN, set()),
    "croc_offscreen": (CROC, ["Modhu"], "Modhu waves toward the boat just off-screen.", set()),
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
            open(os.path.join(d, f"shots/{sid}.raw.txt"), "w", encoding="utf-8").write(leg + "\n\n" + body + "\n")
            rows.append(dict(shot_id=sid, ref="|".join(refs), prompt=f"shots/{sid}.raw.txt", duration_s="3",
                             engine="wan3", ref_labels="|".join(labels), audio="no"))
        with open(os.path.join(d, "shots.csv"), "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
        out = subprocess.run([sys.executable, LINT, "--song", d], capture_output=True, text=True, encoding="utf-8").stdout
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
    print(f"PASS: prompt_lint catches {sum(1 for c in CASES.values() if c[3])} failure patterns, passes "
          f"{sum(1 for c in CASES.values() if not c[3])} fixed ones")


if __name__ == "__main__":
    run()
