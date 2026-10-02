"""A07 Butterfly (rev 3) -> repo song folder for the Wan 3.0 runner.

Reads the song folder's butterfly-shots.json (written by _gen\\build_butterfly_runsheet_v3.py; never edited here) and writes:
  refs\\NN-*.jpg|png            copies of the song's reference images
  shots\\NN_ID.raw.txt          the runsheet's full prompt, sent verbatim (engine wan3 *.raw.txt)
  shots.csv                    one row per CLIP (33): 1280x720, audio off, duration = the sheet's generate length
  cutplan.json                 one entry per SLOT (Tamil + English): which clip, trim point (slip), in/out -> comfy\\song_cuts.py
                               Re-used clips (RA/RB on every refrain line, CH3 on BRKa) appear in several entries with the
                               same take and their own slip; xfade 0 = hard cuts everywhere.
  style.txt / world.txt / characters.txt   minimal files the runner requires (unused by raw prompts)
Re-run after any runsheet change; status cells in shots.csv and chosen takes in cutplan.json are kept."""
import csv, json, os, shutil, sys

SONG = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/mnt/MinMiniKids/songs/A07-Butterfly")
HERE = os.path.dirname(os.path.abspath(__file__))
J = json.load(open(os.path.join(SONG, "butterfly-shots.json"), encoding="utf-8"))
assert J["rev"].startswith("rev 3"), J["rev"]

os.makedirs(os.path.join(HERE, "refs"), exist_ok=True)
os.makedirs(os.path.join(HERE, "shots"), exist_ok=True)
for f in sorted({f for s in J["shots"] for f in s["refs"]}):
    dst = os.path.join(HERE, "refs", f)
    src = os.path.join(SONG, "refs", f)
    if not os.path.exists(dst) or os.path.getsize(dst) != os.path.getsize(src):
        shutil.copy2(src, dst)

first = J["shots"][0]["prompt"].split("\n\n")
open(os.path.join(HERE, "style.txt"), "w", encoding="utf-8", newline="\n").write(first[1] + "\n")
open(os.path.join(HERE, "world.txt"), "w", encoding="utf-8", newline="\n").write("EXTERIOR DAY in a sunny park.\n\n" + first[2] + "\n")
LOCK = {"Mintu": "little boy", "Minnu": "little girl", "Leo": "little boy", "Priya": "little girl",
        "Amma": "grown-up mother (Mintu and Minnu's)", "Mrs-Meena": "grown-up mother (Priya's)"}
names = sorted({c for s in J["shots"] for c in s["cast"]})
open(os.path.join(HERE, "characters.txt"), "w", encoding="utf-8", newline="\n").write(
    "# Lock lines for the runner's checks only; butterfly prompts are sent verbatim from the runsheet (*.raw.txt).\n" +
    "".join(f"{n}: {LOCK.get(n, 'small friendly cartoon butterfly')}; keep exactly as in the reference image.\n" for n in names))

FIELDS = ["shot_id", "cast", "ref", "prompt", "world", "duration_s", "steps", "cfg", "mode", "engine", "keyframe",
          "lastframe", "ref_labels", "audio", "seed", "size", "negative", "status", "notes"]
csv_path = os.path.join(HERE, "shots.csv")
old = {}
if os.path.exists(csv_path):
    old = {r["shot_id"]: r for r in csv.DictReader(open(csv_path, encoding="utf-8", newline=""))}
rows = []
for s in J["shots"]:
    fn = f"shots/{s['n']}_{s['id']}.raw.txt"
    open(os.path.join(HERE, fn), "w", encoding="utf-8", newline="\n").write(s["prompt"].strip() + "\n")
    rows.append(dict(shot_id=s["id"], cast="+".join(s["cast"]), ref="|".join("refs/" + f for f in s["refs"]), prompt=fn,
                     world="", duration_s=str(s["duration_s"]), steps="", cfg="", mode="standard", engine="wan3",
                     keyframe="", lastframe="", ref_labels="|".join(s["ref_labels"]), audio="no", seed="30313",
                     size="1280x720", negative="", status=old.get(s["id"], {}).get("status", ""),
                     notes=f"A07 butterfly {s['n']} {s['id']} {s['title'].replace(',', '')} (uses {' '.join(s['uses'])})"))
keep = [r for k, r in old.items() if k not in {x["shot_id"] for x in rows}]     # retake rows added later
with open(csv_path, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\r\n"); w.writeheader(); w.writerows(rows + keep)

cp_path = os.path.join(HERE, "cutplan.json")
takes = {}
if os.path.exists(cp_path):                                     # keep chosen takes across re-runs (per clip)
    takes = {p["id"]: p["take"] for p in json.load(open(cp_path, encoding="utf-8"))["shots"]}
clip = {s["id"]: s for s in J["shots"]}
plan = []
for x in sorted(J["slots"], key=lambda x: (x["ta"] or [999.0])[0]):
    c = clip[x["clip"]]
    plan.append(dict(n=c["n"], id=c["id"], slot=x["slot"], slug=c["slug"], title=c["title"], kind="none", gen=c["duration_s"],
                     ta_in=x["ta"][0] if x["ta"] else None, ta_out=x["ta"][1] if x["ta"] else None,
                     en_in=x["en"][0] if x["en"] else None, en_out=x["en"][1] if x["en"] else None,
                     slip={"ta": x["offset"], "en": x["offset"]} if x["offset"] else {},
                     take=takes.get(c["id"], f"{c['id']}-seed30313-w3.mp4")))
json.dump({"song": "A07 Butterfly", "song_folder": r"C:\Channel Contents\MinMiniKids\songs\A07-Butterfly",
           "audio": J["audio_files"], "length": J["length"], "xfade": 0, "hard_cut_into": "all", "fades": J["fades"],
           "shots": plan}, open(cp_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(rows), "clips;", sum(int(r["duration_s"]) for r in rows), "s; cutplan", len(plan), "slots",
      "(ta", sum(1 for p in plan if p["ta_in"] is not None), "/ en", sum(1 for p in plan if p["en_in"] is not None), ")")
