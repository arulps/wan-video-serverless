"""Character scale for video prompts -- every character's height and build goes into every shot that shows them.

    py comfy/scale_line.py --song songs/l05-urulai-w3 --cast "Mintu|Minnu|Minmini"   print the SIZES line for that cast
    py comfy/scale_line.py --song songs/<slug> --shot I1                               the line for a shots.csv row (ref_labels)
    py comfy/scale_line.py --song songs/<slug> --shot O2 --mode Minmini=perched        a still / close-up Minmini (half a child)
    py comfy/scale_line.py --table [--out docs/CHARACTER-SCALE.md]                     regenerate the human-readable table

Rule (Arul, 9 Oct 2026, after L05: Minnu came out about half a head shorter than Mintu): a runsheet builder must put
scale_line(cast) VERBATIM into every prompt whose refs show a character; comfy/prompt_lint.py R9 fails the shot otherwise.

Canon lives in comfy/character_scale.json (Mintu 1.00 m is the anchor; humans from the human bible + oviyan
CHARACTER-HEIGHTS.md, non-humans from the non-human bible + oviyan animalHeights.ts, plus Arul's rulings). Song-only
characters go in songs/<slug>/scale.json: {"characters": [{"name": "Baby Potato", "height_m": 0.11, "build": "...",
"source": "..."}, {"name": "Red Butterfly", "same_as": "Vanna"}]}. Ref labels are matched without a leading "the "; a label
not on record is a set/place reference only if it names one (set, room, kitchen, shelf, garden, park, background ...) or is
listed in the song's lint.json "not_characters" -- anything else is a character with no height, and R9 fails it.
"measure": "length" marks entries whose size is a length, not a height (vehicles, and four-legged or swimming characters
whose only size is the bible card's model size): above head size they are said "as long as". Wan reads relative sizes
better than metres, so the line says who is level with whom and where a child's head reaches on an adult, then lists
the metres, ages and builds once. Minmini has two sizes (non-human bible v26, Arul 10 Oct): "flying" (default, about a
child's hand) and "perched" (still or close-up, up to half a child's height); R9 accepts the line for either."""
import argparse, csv, itertools, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CANON = os.path.join(HERE, "character_scale.json")
HAND = 0.13            # m: at or under this, a creature is about the size of a child's hand
HAND15 = 0.20          # m: at or under this, about one and a half times a child's hand
HEAD = 0.30            # m: at or under this, about the size of a child's head
SAME = 0.03            # within 3 % of the anchor = "the same height" (Minnu 1.02 vs Mintu 1.00; Leo 0.95 is shorter)


def norm(s):
    s = re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
    return s[4:] if s.startswith("the ") else s


PLACE_WORDS = re.compile(r"\b(set|room|kitchen|shelf|rack|garden|park|background|backdrop|place|house|street|river|lake|"
                         r"sky|field|farm|classroom|bedroom|plate|scene)\b", re.I)


def load(song=None):
    """{normalised name or alias: entry} for the global canon plus the song's scale.json (song entries win)."""
    base = json.load(open(CANON, encoding="utf-8"))["characters"]
    table = {}
    for e in base:
        for n in [e["name"]] + e.get("aliases", []):
            table[norm(n)] = e
    if song and os.path.exists(os.path.join(song, "scale.json")):
        for e in json.load(open(os.path.join(song, "scale.json"), encoding="utf-8"))["characters"]:
            if "same_as" in e:
                src = table.get(norm(e["same_as"]))
                if src is None:
                    raise SystemExit("scale.json: %s is same_as %s, which is not in the canon" % (e["name"], e["same_as"]))
                e = dict(src, name=e["name"], aliases=e.get("aliases", []),
                         source="same as %s (%s)" % (src["name"], src.get("source", "")))
            e = dict(e, type=e.get("type", "song"))
            for n in [e["name"]] + e.get("aliases", []):
                table[norm(n)] = e
    return table


def is_place_label(label, extra=()):
    return bool(PLACE_WORDS.search(label)) or norm(label) in {norm(x) for x in extra}


def lookup(table, label):
    return table.get(norm(label))


def apply_modes(entries, modes=None):
    """entries with any requested size mode merged in ({"Minmini": "perched"}); the default mode is left as is"""
    modes = {norm(k): v for k, v in (modes or {}).items()}
    out = []
    for e in entries:
        want = modes.get(norm(e["name"]))
        if want and want != e.get("mode"):
            if want not in e.get("modes", {}):
                raise SystemExit("%s has no size mode %r (has: %s)" % (e["name"], want,
                                 ", ".join([e.get("mode", "")] + list(e.get("modes", {})))))
            e = dict(e, mode=want, **{k: v for k, v in e["modes"][want].items() if k != "use"})
        out.append(e)
    return out


def variants(entries):
    """every SIZES line the cast may legally carry (one per combination of size modes)"""
    moded = [e for e in entries if e.get("modes")]
    choices = [[e.get("mode")] + list(e["modes"]) for e in moded]
    for combo in itertools.product(*choices):
        yield scale_line(apply_modes(entries, {e["name"]: c for e, c in zip(moded, combo)}))


def m(x):
    return "%.2f m" % x


def ratio_words(r):
    """how tall X is against the anchor, as Wan-friendly words; r = h_x / h_anchor"""
    if abs(r - 1) <= SAME:
        return None                       # same height -- grouped separately
    if 1 + SAME < r <= 1.2:
        return "a little taller than"
    if 0.8 <= r < 1 - SAME:
        return "a little shorter than"
    if 1.2 < r <= 1.8:
        return "about one and a half times as tall as"
    if 1.8 < r <= 2.5:
        return "about twice as tall as"
    if r > 2.5:
        return "about %d times as tall as" % round(r)
    if 0.6 <= r < 0.8:
        return "about two-thirds as tall as"
    if 0.4 <= r < 0.6:
        return "about half as tall as"
    if 0.25 <= r < 0.4:
        return "about a third as tall as"
    return "about a quarter as tall as" if r >= 0.2 else "far smaller than"


def reach(child_h, adult_h):
    """where the top of a child's head reaches on a grown-up"""
    r = child_h / adult_h
    if r < 0.5:
        return "hip"
    if r < 0.7:
        return "waist"
    if r < 0.8:
        return "chest"
    return "shoulder"


def is_child(e):
    return e.get("type") == "human" and e["height_m"] < 1.3


def is_adult(e):
    return e.get("type") == "human" and e["height_m"] >= 1.3


def join(names):
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]


def scale_line(entries):
    """entries: canon entries in ref order (duplicates removed). Returns the SIZES sentence block."""
    seen, cast = set(), []
    for e in entries:
        if e["name"] not in seen:
            seen.add(e["name"]); cast.append(e)
    if not cast:
        return ""
    kids = [e for e in cast if is_child(e)]
    anchor = next((e for e in cast if e["name"] == "Mintu"), None) or (kids[0] if kids else cast[0])
    A, ha = anchor["name"], anchor["height_m"]
    parts = []
    same = [e["name"] for e in cast if e is not anchor and not is_adult(e) and not e.get("phrase")
            and e.get("measure") != "length" and abs(e["height_m"] / ha - 1) <= SAME]
    if same:
        group = [A] + same
        parts.append("%s are the same height — the tops of their heads are level" % join(group)
                     if len(group) > 2 else "%s and %s are the same height — the tops of their heads are level" % (A, same[0]))
    for e in cast:
        if e is anchor or e["name"] in same:
            continue
        h, n = e["height_m"], e["name"]
        if e.get("phrase"):
            parts.append("%s is %s" % (n, e["phrase"]))
        elif is_adult(e) and is_child(anchor):
            parts.append("the top of %s's head reaches about %s's %s" % (A, n, reach(ha, h)))
        elif is_child(anchor) and h <= HAND:
            parts.append("%s is about the size of a child's hand" % n)
        elif is_child(anchor) and h <= HAND15:
            parts.append("%s is about one and a half times the size of a child's hand" % n)
        elif is_child(anchor) and h <= HEAD:
            parts.append("%s is about the size of a child's head" % n)
        elif e.get("measure") == "length":
            w = (ratio_words(h / ha) or "about as tall as").replace("as tall as", "as long as").replace("taller", "longer")
            parts.append("%s is %s %s is tall" % (n, w, A))
        else:
            parts.append("%s is %s %s" % (n, ratio_words(h / ha), A))
    builds = []
    for e in cast:
        bits = [x for x in (e.get("kind"), e.get("age"), e.get("build"), e.get("mode")) if x]
        size = m(e["height_m"]) + (" long" if e.get("measure") == "length" else "")
        builds.append("%s %s%s" % (e["name"], size, (", " + ", ".join(bits)) if bits else ""))
    if not parts:                              # a single character: nothing to compare, still state the size and build
        return "SIZES: %s." % "; ".join(builds)
    s = parts[0][0].upper() + parts[0][1:]
    return "SIZES, the same in every frame: %s. (%s.)" % ("; ".join([s] + parts[1:]), "; ".join(builds))


def cast_for_labels(table, labels, not_characters=()):
    """ref_labels -> (entries in order, labels with no height on record). Canon names win over place words."""
    entries, missing = [], []
    for l in labels:
        e = lookup(table, l)
        if e is not None:
            entries.append(e)
        elif not is_place_label(l, not_characters):
            missing.append(l)
    return entries, missing


def table_md():
    d = json.load(open(CANON, encoding="utf-8"))
    ch = d["characters"]
    out = ["# MinMini character scale — heights and builds for every video prompt", "",
           "_Generated from `comfy/character_scale.json` (version %s) by `py comfy/scale_line.py --table`. Edit the JSON, "
           "not this file._" % d["version"], "",
           "**Rule (Arul, 9 Oct 2026):** every character's physical size and build is passed to the video. Each prompt carries "
           "the `SIZES` line that `comfy/scale_line.py` builds for that shot's cast (ref order); `prompt_lint` R9 fails a shot "
           "without it, or with a character that has no height here or in the song's `scale.json`. The reference image must "
           "match the build too (heads tall, chubby or slim) — Wan takes body proportions from the reference before the "
           "prompt (learnings §2, §13).", "",
           "Anchor: **Mintu = 1.00 m**. Children are compared to Mintu (\"the tops of their heads are level\"), grown-ups by "
           "where a child's head reaches (on every grown-up from 1.45 to 1.78 m it is about the waist), small creatures "
           "against a child's hand or head. Animals use the 3D staging heights (oviyan `animalHeights.ts`) where they exist; "
           "otherwise the non-human bible card size, which for four-legged, swimming and crawling characters and vehicles is "
           "read as a **length** (the model's longest side — the quadrupeds that have a staging height are all shorter than "
           "their card size).", ""]
    humans = [c for c in ch if c["type"] == "human"]
    kids = sorted([c for c in humans if c["height_m"] < 1.3], key=lambda c: -c["height_m"])
    adults = sorted([c for c in humans if c["height_m"] >= 1.3], key=lambda c: -c["height_m"])
    out += ["## Children", "", "| Character | Age | Height | vs Mintu | Build (bible words) | Source |", "|---|---|---|---|---|---|"]
    for c in kids:
        out.append("| %s | %s | %s | %.2f× | %s | %s |" % (c["name"], c["age"], m(c["height_m"]), c["height_m"], c["build"],
                                                         c["source"]))
    out += ["", "## Grown-ups", "", "| Character | Age | Height | Mintu's head reaches | Build (bible words) | Source |",
            "|---|---|---|---|---|---|"]
    for c in adults:
        out.append("| %s | %s | %s | %s | %s | %s |" % (c["name"], c["age"], m(c["height_m"]), reach(1.0, c["height_m"]),
                                                       c["build"], c["source"]))
    for title, typ in (("Mascot and creatures", "creature"), ("Animals", "animal"), ("Vehicles", "vehicle"),
                       ("Sky", "sky")):
        rows = sorted([c for c in ch if c["type"] == typ], key=lambda c: -c["height_m"])
        if not rows:
            continue
        out += ["", "## " + title, "", "| Character | What | Video size | Bible card size | In a prompt next to Mintu | Source |",
                "|---|---|---|---|---|---|"]
        for c in rows:
            said = scale_line([lookup_all(ch, "Mintu"), c]).split(": ", 1)[1].split(". (")[0]
            out.append("| %s%s | %s | %s | %s | %s | %s%s |" % (c["name"], " (%s, default)" % c["mode"] if c.get("mode") else "",
                                                            c["kind"], m(c["height_m"]) + (
                " long" if c.get("measure") == "length" else " tall"),
                                                            m(c["bible_size_m"]) if "bible_size_m" in c else "",
                                                            said, c["source"], (" — " + c["note"]) if c.get("note") else ""))
            for mode, mv in c.get("modes", {}).items():
                alt = apply_modes([c], {c["name"]: mode})[0]
                alt_said = scale_line([lookup_all(ch, "Mintu"), alt]).split(": ", 1)[1].split(". (")[0]
                out.append("| %s (%s) | %s | %s tall | | %s | %s — %s |" % (c["name"], mode, c["kind"], m(alt["height_m"]),
                                                                        alt_said, c["source"], mv.get("use", "")))
    out += ["", "## Song-only characters", "",
            "Kept per song in `songs/<slug>/scale.json` (same fields; `same_as` borrows a canon entry):", ""]
    songs = os.path.join(HERE, "..", "songs")
    for slug in sorted(os.listdir(songs)) if os.path.isdir(songs) else []:
        p = os.path.join(songs, slug, "scale.json")
        if not os.path.exists(p):
            continue
        t = load(os.path.join(songs, slug))
        rows = [t[norm(e["name"])] for e in json.load(open(p, encoding="utf-8"))["characters"]]
        out += ["**%s**" % slug, "", "| Character | Height | Build | Source |", "|---|---|---|---|"]
        for c in rows:
            out.append("| %s | %s | %s | %s |" % (c["name"], m(c["height_m"]), c.get("build") or c.get("kind", ""),
                                                  c.get("source", "")))
        out.append("")
    return "\n".join(out) + "\n"


def lookup_all(ch, name):
    return next(c for c in ch if c["name"] == name)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--song"); ap.add_argument("--cast", help="ref labels joined with |")
    ap.add_argument("--shot"); ap.add_argument("--table", action="store_true"); ap.add_argument("--out")
    ap.add_argument("--mode", action="append", default=[], help="Name=mode, e.g. Minmini=perched (repeatable)")
    a = ap.parse_args()
    if a.table:
        md = table_md()
        if a.out:
            open(a.out, "w", encoding="utf-8").write(md); print("wrote", a.out)
        else:
            print(md)
        return
    t = load(a.song)
    if a.shot:
        rows = list(csv.DictReader(open(os.path.join(a.song, "shots.csv"), encoding="utf-8", newline="")))
        row = next((r for r in rows if r["shot_id"] == a.shot), None)
        if row is None:
            sys.exit("no shot %s" % a.shot)
        labels = [x for x in (row.get("ref_labels") or "").split("|") if x]
    elif a.cast:
        labels = [x for x in a.cast.split("|") if x]
    else:
        sys.exit("give --cast, --shot or --table")
    entries, missing = cast_for_labels(t, labels)
    if missing:
        sys.exit("no height on record for: %s -- add them to comfy/character_scale.json or the song's scale.json"
                 % ", ".join(missing))
    modes = dict(x.split("=", 1) for x in a.mode)
    print(scale_line(apply_modes(entries, modes)))


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    main()
