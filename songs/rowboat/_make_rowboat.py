"""L04 Row Row Row Your Boat -> repo song folder for the Wan 3.0 runner.

Reads the runsheet's own data (C:\\Channel Contents\\MinMiniKids\\songs\\L04-Row Row Row Your Boat\\_gen\\build_wan3_runsheet.py,
executed only up to its shot table -- the builder and the runsheet are never modified) and writes:
  refs\\01..10-*.jpg            copies of the song's reference images
  shots\\NN_ID.raw.txt          the runsheet's full prompt, sent verbatim (engine wan3 *.raw.txt)
  shots.csv                    one row per shot: 1280x720, audio off, duration = the sheet's generate length
  cutplan.json                 cut order, Tamil/English in-out, slips, fades -> comfy\\song_cuts.py
  style.txt / world.txt / characters.txt   minimal files the runner requires (unused by raw prompts)
Re-run after any runsheet change; status cells already in shots.csv are kept.
Seating override (Arul 2026-10-01, gate-2 V1a layout): see SEAT_ALL below."""
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

# --- Seating override (Arul, 2026-10-01) ------------------------------------------------------------------------------
# Gate 1: the runsheet's wording let Wan perch the kids on the boat's rim. Gate 2 tried face-to-face benches; Wan ignored it
# and gave both kids side by side on one bench facing Appa, sitting properly inside -- Arul approved that V1a (gate 2) as
# the look-lock. So: the runsheet's layout, plus explicit bench / inside-the-boat / no-rim / no-standing wording, and every
# kid two-shot starts already seated (gate-2 V1b opened with both kids standing). The master runsheet and builder stay
# untouched; V1a was rendered from the gate-2 wording (face-to-face), its sidecar JSON holds the exact prompt.
KIDS_SEATED = ("Mintu and Minnu sit together side by side on the low wooden bench at the other end of the boat, facing Appa, "
               "so he can see them as he rows. The children sit down properly on the bench, low inside the boat, legs inside "
               "and feet on the floor of the boat, only their chests, arms and heads above the side; nobody sits on the edge "
               "or rim of the boat and nobody stands up. Only Appa, the grown-up father with the moustache and the black-and-white "
               "checked shirt, rows and holds the oars; Mintu and Minnu are small children and never row.")
SEAT_ALL = [
    ("two wooden oars resting inside it.", "two wooden oars and low wooden benches inside it."),   # I1, T1 empty boat
    ("with a soft teal stripe along its side and two wooden oars.",
     "with a soft teal stripe along its side, two wooden oars and low wooden benches inside."),
    ("Appa sits in the middle and rows with both oars.",
     "Appa sits on the rowing bench at one end of the boat and rows with both oars, facing the children."),
    ("Mintu and Minnu sit side by side on the seat right in front of him, facing him, so he can see them as he rows and "
     "they can look ahead down the river.", KIDS_SEATED),
    ("Medium two-shot of Mintu and Minnu side by side on their seat facing Appa, waist up, the camera in front of the boat "
     "facing them",
     "Both children are already sitting on their bench from the very first frame and stay seated throughout. Medium "
     "two-shot of Mintu and Minnu side by side on their bench facing Appa, waist up, the camera in front of the boat "
     "facing them"),
]
SEAT_SHOT = {}
_hits = {o: 0 for o, _ in SEAT_ALL}
for s in S:
    t = s["prompt_refs"]
    for o, n in SEAT_ALL:
        if o in t:
            _hits[o] += t.count(o); t = t.replace(o, n)
    for o, n in SEAT_SHOT.get(s["id"], []):
        assert t.count(o) == 1, f"seating override not found once in {s['id']}: {o[:50]}"
        t = t.replace(o, n)
    assert "on the seat right in front of him" not in t and "face to face" not in t, f"old seating left in {s['id']}"
    s["prompt_refs"] = t
assert all(_hits.values()), f"seating override matched nothing: {[o[:50] for o, c in _hits.items() if not c]}"
print("seating override:", {o[:28]: c for o, c in _hits.items()})

# --- Cast / pack override + W1 retake fixes (Fable, 2026-10-01, after the W1 review) -----------------------------------
# Boat shots that referenced only part of the family (KIDS, APPA packs) came back with the missing members invented
# off-model (a green-shirt "Appa", kids in blue/pink): Wan widens or pulls back and fills the boat. So every boat shot now
# carries the full family refs; V2c (croc beside the boat, which showed an empty boat) gets FAM+CROC.
PACK_SWAP = {"KIDS": "FAM", "APPA": "FAM"}
PACK_SHOT = {"V2c": "FAM+CROC"}
_v1a = next(x for x in S if x["id"] == "V1a")["prompt_refs"]
KEEP_LINE = _v1a[_v1a.index("Keep every character"):_v1a.index("are about the same size.") + len("are about the same size.")]
SHOT_FIX = {
    "V2a": [("Close-up on Appa at the oars, framed from the chest up, the bright river soft behind him.",
             "Close-up on Appa at the oars, framed from the chest up for the whole shot, the bright river soft behind him; "
             "the camera does not pull back and the children are not shown.")],
    "V2c": [("Medium shot at water level right beside the boat's wooden side. ",
             KEEP_LINE + "\n\nMedium shot at water level right beside the side of the family's small honey-wood boat with "
             "its soft teal stripe; Appa, Mintu and Minnu sit in the boat at the edge of frame, and the children lean to "
             "peek over the side with wide, delighted eyes. ")],
    "V2d": [("the camera in front of the boat facing them. [0–1.5s]",
             "the camera in front of the boat facing them; the camera stays on this two-shot for the whole shot and never "
             "cuts to a wide shot. [0–1.5s]"),
            ("mouths wide open in a huge comic play-scream, hands up beside their cheeks — joyful and funny, not frightened —",
             "mouths wide open in a huge comic play-scream with big delighted grins and eyebrows raised high, hands up "
             "beside their cheeks — joyful and funny, not frightened, not crying, no tears —")],
    "V6a": [("as the wooden side of the boat slides gently past in the foreground.",
             "toward the boat passing just off-screen; only Chiku, his lily pad and the water are in frame.")],
    "X1b": [("[4–6s] the banks open out ahead into warm, tall golden grass under a big open sky.",
             "[4–6s] the river carries on ahead between banks of warm, tall golden grass under a big open sky; the boat "
             "stays on the water the whole time.")],
}
for s in S:
    new = PACK_SHOT.get(s["id"], PACK_SWAP.get(s["pack"], s["pack"]))
    if new != s["pack"]:
        old_leg, new_leg = PACK[s["pack"]][1], PACK[new][1]
        assert s["prompt_refs"].startswith(old_leg), f"legend not at start of {s['id']}"
        s["prompt_refs"] = new_leg + s["prompt_refs"][len(old_leg):]
        s["pack"] = new
    for o, n in SHOT_FIX.get(s["id"], []):
        assert s["prompt_refs"].count(o) == 1, f"shot fix not found once in {s['id']}: {o[:50]}"
        s["prompt_refs"] = s["prompt_refs"].replace(o, n)
# Timed beats ("[0–1.5s] ...") were read as separate shots in V2d (hard cut). Every shot with beats gets an explicit
# one-take line in front of its first beat (prompt_lint R5).
_BEAT = re.compile(r"\[\d+(\.\d+)?\s*[–-]\s*\d")
for s in S:
    t = s["prompt_refs"]
    m = _BEAT.search(t)
    if m and "no cuts between" not in t:
        s["prompt_refs"] = t[:m.start()] + "One continuous take, no cuts between the timed moments: " + t[m.start():]
print("packs:", {x["id"]: x["pack"] for x in S if x["pack"] not in ("FAM",)})

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
