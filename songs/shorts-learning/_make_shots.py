"""Generate songs/shorts-learning shot files, world files and shots.csv rows from
C:\\Channel Contents\\MinMiniKids\\YT Shorts\\LOOP-SHORTS-LEARNING-RUNSHEET.md (rev 3).
Wan 3.0, 720x1280, 5 s, audio on: soft music + an off-screen English voice at the runsheet marks.
Colours/fruits/vegetables keep the kids as in the runsheet (Arul 2026-09-29). Animals (A1-A6) are skipped for now.
Re-running overwrites shot files and rewrites the shots.csv rows it owns, keeping any status cells already set."""
import csv, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RUNSHEET = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser(
    "~/mnt/MinMiniKids/YT Shorts/LOOP-SHORTS-LEARNING-RUNSHEET.md")
t = open(RUNSHEET, encoding="utf-8").read()


def block(name):
    m = re.search(r"\*\*" + re.escape(name) + r"\*\*\s*```\n(.*?)```", t, re.S)
    return m.group(1).strip().split("\n\nAUDIO:")[0].strip()


# ---------- worlds (runsheet W blocks, with the INTERIOR/EXTERIOR line our runner expects first)
WORLDS = {
    "W1 · Living room (dry)": ("world-living.txt", "INTERIOR DAY in the family living room; everyone stays inside the room.",
                               block("W1 · Living room (dry)"), "warm soft daylight in the living room"),
    "W1 · Living room (rain)": ("world-living-rain.txt",
                                "INTERIOR DAY in the family living room while it rains outside; everyone stays inside the room.",
                                block("W1 · Living room (rain)"), "soft rain on the window, cool grey daylight and warm lamplight"),
    "W2 · Kitchen": ("world-kitchen.txt", "INTERIOR DAY in the family kitchen; everyone stays inside the kitchen.",
                     block("W2 · Kitchen"), "warm morning daylight in the kitchen"),
    "W5 · Garden": ("world-garden-gate.txt", "EXTERIOR DAY in the small back garden; the camera looks at the closed garden gate.",
                    block("W5 · Garden"), "warm soft afternoon sunlight in the garden, gentle birdsong"),
    "W6 · Street": ("world-street.txt", "EXTERIOR DAY on a quiet neighbourhood street.",
                    block("W6 · Street"), "warm soft daylight on the street, blue sky"),
}
for key, (fn, head, body, _) in WORLDS.items():
    open(os.path.join(HERE, fn), "w", encoding="utf-8", newline="\n").write(head + "\n\n" + body + "\n")

# colour shots: same living room without the loose ball on the rug (it would compete with the hero object)
_fn, _head, _body, _atm = WORLDS["W1 · Living room (dry)"]
open(os.path.join(HERE, "world-living-plain.txt"), "w", encoding="utf-8", newline="\n").write(
    _head + "\n\n" + _body.replace(" with a few wooden toys and a ball on it", "") + "\n")

# ---------- recording sheet (English lines: hook, word, repeat)
REC = {}
for m in re.finditer(r"^\| ([A-Z]+\d+) \| (.+?) \| (.+?) \| (.+?) \|$", t, re.M):
    REC[m.group(1)] = [c.split(" / ", 1)[1].strip() if " / " in c else c.strip() for c in m.group(2, 3, 4)]

# ---------- items
items = []
for p in re.split(r"\n## ", t)[1:]:
    head = p.split("\n", 1)[0]
    w = re.search(r"\*\*World:\*\* (.*?) · \*\*Cast:\*\* (.*?) · \*\*Loop:\*\* (.*)", p)
    s = re.search(r"\*\*Scene:\*\* (.*)", p)
    if w and s:
        items.append(dict(id=head.split(" ·")[0].strip(), head=head, world=w.group(1).strip(),
                          cast=w.group(2).strip(), scene=s.group(1).strip()))

REFS = {"Minnu": "refs/minnu-body-9x16.png", "Mintu": "refs/mintu-front-9x16.png", "Amma": "refs/amma-front-9x16.png",
        "Appa": "refs/appa-front-9x16.png", "Thatha": "refs/thatha-front-9x16.png", "Paati": "refs/paati-front-9x16.png",
        "Kollu-Thatha": "refs/kollu-thatha-front-9x16.png"}
LABEL = {"Kollu-Thatha": "Kollu Thatha"}
SFX = {"A": "gentle birdsong and a light breeze", "C": "a soft sparkle as it appears", "F": "a soft sparkle as it appears", "FD": "a soft clink of the steel lid",
       "V": "a soft engine hum and one friendly horn toot", "SN": "the clear, natural sound the object makes",
       "FM": "the soft creak of the door"}
MUSIC = ("A gentle, playful xylophone and ukulele melody plays softly underneath from the very first frame at one steady tempo; "
         "no singing, no other speech.")
TIMING_REVEAL = ("The reveal comes at about one and a half seconds and is held still until about three and a half seconds; "
                 "by four and a half seconds everything is back exactly as at the start")
TIMING_ACTION = ("The key moment happens between about one and a half and three and a half seconds; "
                 "by four and a half seconds everything is back exactly as at the start")
REVEAL_SERIES = ("A", "C", "F", "VG", "FD", "FM", "V")
# Arul 2026-09-29: colours and fruits keep Minnu/Mintu exactly as in the runsheet (the object itself is prompt-only, no
# object reference image). The object-only variant is kept behind this switch; C1/F3 object-only renders are *-objectonly.
OBJECT_ONLY = False


def sentences(x):
    return [s.strip() for s in re.split(r"(?<=[.])\s+(?=[A-Z])", x) if s.strip()]


def sound(id_, series, has_cast):
    hook, word, rep = REC[id_]
    out = ("Sound: a warm, cheerful off-screen female voice speaks slowly and clearly in English: at the very start she asks "
           f"\"{hook}\"; on the reveal she says \"{word}\"; a moment later she says \"{rep}\"; then she is quiet.")
    if SFX.get(series):
        out += f" Also {SFX[series]}."
    if has_cast:
        out += " The characters on screen never talk and never move their lips."
    return out + " " + MUSIC


def build(it):
    id_ = it["id"]
    series = re.match(r"[A-Z]+", id_).group(0)
    wfile, _, _, atmos = WORLDS[it["world"]]
    cast = [] if it["cast"] in ("none", "—", "") else [c.strip() for c in it["cast"].split(",")]
    cast = ["Kollu-Thatha" if c == "Kollu Thatha" else c for c in cast]
    avoid = ["on-screen text or letters", "a second object competing for attention", "extra people", "camera movement"]
    if series in ("C", "F") and OBJECT_ONLY:
        obj = re.sub(r"^one ", "a ", re.search(r"takes out (.+?) and holds it up", it["scene"]).group(1))
        cast = []
        if series == "C":
            colour = REC[id_][1].rstrip("!").lower()
            shot = "tall vertical frame, close shot of a small closed wooden toy box on the soft round rug, centred, with room above it"
            pose = "at the start the small wooden toy box is closed; nobody is in the shot"
            motion = (f"the lid gently opens by itself and {obj} rises slowly out of the box and floats in the middle of the frame, "
                      f"large, centred and facing the camera, in one solid, bright, true {colour}, gently turning; it holds there; "
                      "then it sinks back down into the box and the lid closes, exactly as at the start")
            avoid += [f"the {colour} changing to another colour", "hands"]
            wfile = "world-living-plain.txt"
        else:
            shot = ("tall vertical frame, close shot of a round woven basket covered with a small cloth on the low wooden "
                    "dining table, centred, with room above it")
            pose = "at the start the cloth covers the basket; nobody is in the shot"
            motion = (f"the cloth lifts gently off by itself and {obj} rises slowly out of the basket and floats in the middle of "
                      "the frame, large, centred, facing the camera and instantly recognisable, in its true natural colours, "
                      "gently turning; it holds there; then it sinks back into the basket and the cloth settles over it again, "
                      "exactly as at the start")
            avoid += ["the fruit changing shape or colour", "hands", "a knife"]
    else:
        ss = sentences(it["scene"])
        shot = "tall vertical frame; " + ss[0][0].lower() + ss[0][1:].rstrip(".")
        rest = " ".join(ss[1:]).rstrip(".")
        motion = rest[0].lower() + rest[1:]
        if cast:
            pose = ("the character faces the camera square-on; the key moment is big, clear and slightly exaggerated so a "
                    "toddler can read it and copy it")
            avoid += ["T-pose"] if series in ("AC", "D") else ["T-pose", "arms stiffly spread wide"]
        else:
            pose = ("one thing is the hero of the shot: large, centred and clearly visible; the background stays soft and uncluttered. "
                    "It is a cartoon object from a Pixar-soft 3D children's film, not a real product: chunky, rounded, simplified toy-like "
                    "shapes with slightly exaggerated cute proportions, smooth soft matte surfaces and bright friendly colours, "
                    "no fine realistic detail. The whole clip is one continuous shot from the same camera position, with no cuts")
            avoid += ["photorealism", "a real photograph or product shot", "realistic metal, glass or wood textures",
                      "fine realistic detail", "a cut to a closer shot", "zooming in", "a second camera angle"]
        if series == "D":
            avoid += ["travelling across the frame", "turning away from the camera"]
        if series == "C":
            wfile = "world-living-plain.txt"
            avoid += ["the hero object changing colour"]
        if series in ("F", "VG"):
            avoid += ["the fruit or vegetable changing shape or colour"]
    timing = TIMING_REVEAL if series in REVEAL_SERIES else TIMING_ACTION
    motion = f"{motion}. {timing}; one simple action, slow gentle motion. {sound(id_, series, bool(cast))}"
    txt = (f"ATMOSPHERE: {atmos}\nANGLE: the camera is at a child's eye height, square-on, locked off: no zoom, no pan\n"
           f"SHOT: {shot}\nPOSE: {pose}\nMOTION: {motion}\nNEGATIVE: {', '.join(avoid)}\n")
    fn = f"shots/{id_}-w3.txt"
    os.makedirs(os.path.join(HERE, "shots"), exist_ok=True)
    open(os.path.join(HERE, fn), "w", encoding="utf-8", newline="\n").write(txt)
    return dict(shot_id=f"{id_}_w3", cast="+".join(cast) if cast else "none",
                ref="|".join(REFS[c] for c in cast), prompt=fn, world=wfile, duration_s="5", steps="", cfg="",
                mode="standard", engine="wan3", keyframe="", lastframe="",
                ref_labels="|".join(LABEL.get(c, c) for c in cast), audio="yes", seed="30313",
                size="720x1280", negative="", status="", notes=f"Learning Short {id_} (runsheet rev 3)")


FIELDS = ["shot_id", "cast", "ref", "prompt", "world", "duration_s", "steps", "cfg", "mode", "engine", "keyframe", "lastframe",
          "ref_labels", "audio", "seed", "size", "negative", "status", "notes"]
rows = [build(it) for it in items]   # all 78 incl. animals A1-A6 (added 2026-09-29)
csv_path = os.path.join(HERE, "shots.csv")
old = {}
if os.path.exists(csv_path):
    for r in csv.DictReader(open(csv_path, encoding="utf-8", newline="")):
        old[r["shot_id"]] = r
for r in rows:
    if old.get(r["shot_id"], {}).get("status"):
        r["status"] = old[r["shot_id"]]["status"]
mine = {x["shot_id"] for x in rows}
with open(csv_path, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\r\n")
    w.writeheader()
    w.writerows(rows + [r for k, r in old.items() if k not in mine])
print(len(rows), "rows;", ", ".join(r["shot_id"] for r in rows))
