"""L04 Row Row Row Your Boat -> repo song folder for the Wan 3.0 runner.

Reads the runsheet's own data (C:\\Channel Contents\\MinMiniKids\\songs\\L04-Row Row Row Your Boat\\_gen\\build_wan3_runsheet.py,
executed only up to its shot table -- the builder and the runsheet are never modified) and writes:
  refs\\01..10-*.jpg            copies of the song's reference images
  shots\\NN_ID.raw.txt          the runsheet's full prompt, sent verbatim (engine wan3 *.raw.txt)
  shots.csv                    one row per shot: 1280x720, audio off, duration = the sheet's generate length
  cutplan.json                 cut order, Tamil/English in-out, slips, fades -> comfy\\song_cuts.py
  style.txt / world.txt / characters.txt   minimal files the runner requires (unused by raw prompts)
Re-run after any runsheet change; status cells already in shots.csv are kept.
Seating override (Arul 2026-10-01): see SEAT_ALL / SEAT_SHOT below."""
import csv, json, os, re, shutil, sys

SONG = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/mnt/MinMiniKids/songs/L04-Row Row Row Your Boat")
HERE = os.path.dirname(os.path.abspath(__file__))
BUILDER = os.path.join(SONG, "_gen", "build_wan3_runsheet.py")
src = open(BUILDER, encoding="utf-8").read()
src = src[:src.index("GEN_SEC = ")]            # data + timing + prompts only; no file output
ns = {"__file__": BUILDER, "__name__": "rowboat_runsheet"}
exec(compile(src, BUILDER, "exec"), ns)
S, PACK, REF, SFX, B, W = ns["S"], ns["PACK"], ns["REF"], ns["SFX"], ns["B"], ns["W"]
TA_END, EN_END = ns["TA_END"], ns["EN_END"]

os.makedirs(os.path.join(HERE, "refs"), exist_ok=True)
os.makedirs(os.path.join(HERE, "shots"), exist_ok=True)
for f in REF.values():
    dst = os.path.join(HERE, "refs", f)
    if not os.path.exists(dst):
        shutil.copy2(os.path.join(SONG, "refs", f), dst)

for fn, txt in (("style.txt", B["STYLE"]), ("world.txt", "EXTERIOR DAY on a gentle storybook river.\n\n" + W["W1"][1])):
    open(os.path.join(HERE, fn), "w", encoding="utf-8", newline="\n").write(txt + "\n")
open(os.path.join(HERE, "characters.txt"), "w", encoding="utf-8", newline="\n").write(
    "# Lock lines for the runner's checks only; rowboat prompts are sent verbatim from the runsheet (*.raw.txt).\n"
    "Appa: father; keep exactly as in the reference image.\nMintu: little boy; keep exactly as in the reference image.\n"
    "Minnu: girl; keep exactly as in the reference image.\nModhu: friendly cartoon crocodile; keep exactly as in the reference image.\n"
    "Singa: friendly cartoon lion; keep exactly as in the reference image.\n"
    "Pani-Karadi: cuddly cartoon polar bear; keep exactly as in the reference image.\n"
    "Chiku: tiny cartoon mouse; keep exactly as in the reference image.\n")

LABEL = {"01": "Appa", "02": "Appa", "03": "Mintu", "04": "Mintu", "05": "Minnu", "06": "Minnu", "07": "Modhu",
         "08": "Singa", "09": "Pani Karadi", "10": "Chiku"}
def slug(t):
    t = re.sub(r"[^a-z0-9]+", "-", t.lower().replace("×", "x")).strip("-")
    return "-".join(t.split("-")[:6])

# --- Seating override (Arul, 2026-10-01, after the V1a gate) --------------------------------------------------------
# The runsheet seats the kids side by side facing Appa; in V1a they read as perched on the boat's rim. Arul's call: both
# kids in the back half on two low benches facing each other, Appa rowing in the front half facing them; the kid
# two-shots become a side-on shot of both (one shot per slot, so timings and the cut plan are unchanged).
# Applied to the prompts written here only -- the master runsheet and its builder stay untouched.
SEAT_ALL = [
    ("two wooden oars resting inside it.", "two wooden oars and three low wooden benches inside it."),   # I1, T1 empty boat
    ("with a soft teal stripe along its side and two wooden oars.",
     "with a soft teal stripe along its side, two wooden oars and three low wooden benches inside."),
    ("Appa sits in the middle and rows with both oars.",
     "Appa sits on the rowing bench in the front half of the boat, facing the back of the boat, and rows with both oars."),
    ("Mintu and Minnu sit side by side on the seat right in front of him, facing him, so he can see them as he rows and "
     "they can look ahead down the river.",
     "In the back half of the boat two low wooden benches face each other: Mintu sits on the bench at the very back, "
     "facing forward, and Minnu sits on the bench just in front of him, facing back toward him, so the two children sit "
     "face to face, knees almost touching, and Appa can watch them both as he rows. The children sit down properly on "
     "their benches, low inside the boat, legs inside the boat and only their chests, arms and heads above the side; "
     "nobody sits on the edge or rim of the boat."),
    ("Medium two-shot of Mintu and Minnu side by side on their seat facing Appa, waist up, the camera in front of the boat "
     "facing them",
     "Medium two-shot of Mintu and Minnu on their two facing benches, waist up, seen from the side at their eye level just "
     "off the side of the boat; both children turn their heads toward the camera side so both faces are clearly visible"),
]
SEAT_SHOT = {
    "V1b": [("; Appa's shoulder soft and out of focus in the foreground.", "; Appa soft and out of focus beyond them.")],
    "V6c": [("; Appa's shoulder soft in the foreground;", "; Appa soft and out of focus beyond them;")],
    "X2a": [("Locked-off medium shot from in front of the boat as it comes gently toward camera; Appa's back and rowing "
             "arms soft in the foreground, the children facing camera beyond him. Mintu and Minnu, still seated side by "
             "side, do a happy little rowing dance:",
             "Locked-off medium shot from the side of the boat at the children's eye level as it glides slowly; Appa "
             "rowing soft and out of focus beyond them. Mintu and Minnu, seated face to face on their benches, do a happy "
             "little mirror-image rowing dance toward each other:")],
    "X3b": [("medium shot from in front of the boat:", "medium shot from beside the boat:")],
}
_hits = {o: 0 for o, _ in SEAT_ALL}
for s in S:
    t = s["prompt_refs"]
    for o, n in SEAT_ALL:
        if o in t:
            _hits[o] += t.count(o); t = t.replace(o, n)
    for o, n in SEAT_SHOT.get(s["id"], []):
        assert t.count(o) == 1, f"seating override not found once in {s['id']}: {o[:50]}"
        t = t.replace(o, n)
    assert "side by side" not in t, f"'side by side' left in {s['id']}"
    s["prompt_refs"] = t
assert all(_hits.values()), f"seating override matched nothing: {[o[:50] for o, c in _hits.items() if not c]}"
print("seating override:", {o[:28]: c for o, c in _hits.items()})

FIELDS = ["shot_id", "cast", "ref", "prompt", "world", "duration_s", "steps", "cfg", "mode", "engine", "keyframe",
          "lastframe", "ref_labels", "audio", "seed", "size", "negative", "status", "notes"]
csv_path = os.path.join(HERE, "shots.csv")
old = {}
if os.path.exists(csv_path):
    old = {r["shot_id"]: r for r in csv.DictReader(open(csv_path, encoding="utf-8", newline=""))}

rows, plan = [], []
for s in S:
    keys = PACK[s["pack"]][0]
    names = [n.replace(" ", "-") for n in PACK[s["pack"]][2]]
    fn = f"shots/{s['n']}_{s['id']}.raw.txt"
    open(os.path.join(HERE, fn), "w", encoding="utf-8", newline="\n").write(s["prompt_refs"].strip() + "\n")
    row = dict(shot_id=s["id"], cast="+".join(names) if names else "none",
               ref="|".join("refs/" + REF[k] for k in keys), prompt=fn, world="", duration_s=str(s["gen"]),
               steps="", cfg="", mode="standard", engine="wan3", keyframe="", lastframe="",
               ref_labels="|".join(LABEL[k] for k in keys), audio="no", seed="30313", size="1280x720",
               negative="", status=old.get(s["id"], {}).get("status", ""),
               notes=f"L04 rowboat {s['n']} {s['id']} {s['title'].replace(',', '')} ({s['w']})")
    rows.append(row)
    sl = {}
    if s["kind"] == "sfx":
        _, ta, en = SFX[s["sec"]]
        sl = {"ta": round(1.5 - (ta[0] - s["ta_in"]), 3), "en": round(1.5 - (en[0] - s["en_in"]), 3)}
    plan.append(dict(n=s["n"], id=s["id"], slug=slug(s["title"]), title=s["title"], kind=s["kind"], gen=s["gen"],
                     use=s["use"], ta_in=s["ta_in"], ta_out=s["ta_out"], en_in=s["en_in"], en_out=s["en_out"],
                     slip=sl, take=f"{s['id']}-seed30313-w3.mp4"))
keep = [r for k, r in old.items() if k not in {x["shot_id"] for x in rows}]   # retake rows added later
with open(csv_path, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\r\n"); w.writeheader(); w.writerows(rows + keep)

# master WAVs, found by name (the Tamil file name contains a narrow no-break space before "p.m.")
wavs = [f for f in os.listdir(SONG) if f.lower().endswith(".wav")]
AUD_TA = next(f for f in wavs if "Recording" in f and "Remix" in f)
AUD_EN = next(f for f in wavs if "english" in f.lower())
cp_path = os.path.join(HERE, "cutplan.json")
takes = {}
if os.path.exists(cp_path):                                     # keep chosen takes across re-runs
    takes = {p["id"]: p["take"] for p in json.load(open(cp_path, encoding="utf-8"))["shots"]}
for p in plan:
    p["take"] = takes.get(p["id"], p["take"])
json.dump({"song": "L04 Row Row Row Your Boat", "song_folder": r"C:\Channel Contents\MinMiniKids\songs\L04-Row Row Row Your Boat",
           "audio": {"ta": AUD_TA, "en": AUD_EN},
           "length": {"ta": TA_END, "en": EN_END}, "xfade": 0.4, "hard_cut_into": "sfx",
           "fades": {"ta": {"in": 1.347, "out": 1.2}, "en": {"in": 1.347, "out": 1.0}},
           "shots": plan}, open(cp_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(rows), "shots;", sum(int(r["duration_s"]) for r in rows), "s; cutplan", len(plan))
