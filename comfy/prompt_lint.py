"""Pre-dispatch prompt lint for Wan 3.0 song folders -- run BEFORE a queue goes to CC (and CC runs it again as a gate).

    python comfy/prompt_lint.py --song songs/rowboat [--only V1b,V2c] [--quiet]

Checks every shots.csv row (engine wan3) against the rules learned in production
(C:\\Channel Contents\\MinMiniKids\\WAN3-PRODUCTION-LEARNINGS.md). FAIL = must fix before dispatch; WARN = look at it.

  R1 legend     the "Images 1-2 are X ..." line matches ref_labels (order, count) and every ref file exists.
  R2 cast       every character named in the shot (or via an alias such as "the children") is in its refs --
                otherwise Wan invents them off-model (Row Row W1: green-shirt "Appa" = Mintu's look on an adult).
  R3 space      a shared space in frame (e.g. "boat") with no refs for the group that lives there -> FAIL
                (Row Row V2c: croc beside an empty boat); partial group refs -> FAIL (W1 kids-only close-ups).
  R4 owner      an exclusive action (e.g. rowing) appears but the ownership line ("Only Appa ...") is missing
                (Row Row: Mintu drawn as the rower).
  R5 beats      timed beats "[0-1.5s] ..." without a shot-specific "stays on this shot / never cuts" line -> WARN
                (Row Row V2d cut between beats).
  R6 words      risky words from the learnings (sneeze, scream without "no tears", ...) -> WARN.
  R7 basics     duration 2-30 s, audio=no for songs (lint.json "audio"), prompt file exists and is non-empty.
  R8 no-cast    a shot with no refs at all -> WARN (style can drift photoreal; outdoor scenes usually hold).

Per-song rules live in <song>/lint.json (all keys optional):
  {"audio": "no",
   "aliases": {"the children": ["Mintu", "Minnu"]},
   "spaces": {"boat": ["Appa", "Mintu", "Minnu"]},
   "exempt": ["off-screen", "out of frame"],            # a sentence with one of these doesn't put anyone in frame
   "owners": [{"pattern": "\\\\b(rows|rowing|oars?)\\\\b", "owner": "Appa", "require": "Only Appa"}],
   "risky": {"sneeze": "runny nose risk -- hide it (elbow)"},
   "allow": {"I1": {"R3": "empty boat at the jetty, on purpose"}}}   # reviewed exceptions, each with its reason
Exit code 0 = no FAIL, 1 = at least one FAIL, 2 = usage error.
"""
import argparse, csv, json, os, re, sys

DEFAULT_EXEMPT = ["off-screen", "off screen", "out of frame", "not shown", "not in frame", "as if seen from",
                  "empty", "nobody ", "no one ", "never ", "do not ", "don't "]
DEFAULT_RISKY = {
    r"\bsneez": "sneeze -> runny-nose artefacts; let the action hide it (sneeze into the elbow)",
    r"\bscream": "a wide-mouthed, eyes-shut scream reads as crying -- ask for grins/raised brows and avoid tears",
    r"\bmirror": "mirrors render badly -- avoid or keep incidental",
    r"\bthe [\w-]+ (?:passing |going )?just off-?screen": "naming an object 'just off-screen' pulls it into frame "
        "(Row Row V3b drew an empty sailboat) -- describe the gaze instead ('waves toward the camera')",
    r"\b(sign|label|written|letters?)\b": "text renders badly -- keep incidental",
}
BEAT_RE = re.compile(r"\[\s*\d+(\.\d+)?\s*[–-]\s*\d+(\.\d+)?\s*s\s*\]")
HOLD_RE = re.compile(r"(no cuts between|stays on this|never cuts|does not cut|doesn't cut|no cut to|holds? (?:steady|on)|"
                     r"camera does not|whole shot|for the whole)", re.I)
AVOID_START = re.compile(r"^\s*(no |nothing |avoid|ambient|keep every character|use the reference)", re.I)


def sentences(text):
    out = []
    for line in text.splitlines():
        for s in re.split(r"(?<=[.!?;])\s+", line.strip()):
            if s:
                out.append(s)
    return out


def parse_legend(first_line):
    """'Images 1–2 are Appa, Image 7 is Modhu the crocodile.' -> ['Appa','Appa',...,'Modhu the crocodile']"""
    labels = []
    for m in re.finditer(r"Images?\s+(\d+)(?:\s*[–-]\s*(\d+))?\s+(?:is|are)\s+([^,.]+)", first_line):
        a, b = int(m.group(1)), int(m.group(2) or m.group(1))
        if a != len(labels) + 1:
            return None
        labels += [m.group(3).strip()] * (b - a + 1)
    return labels


def name_re(name):
    parts = re.split(r"[\s-]+", name)
    return re.compile(r"\b" + r"[\s-]+".join(map(re.escape, parts)) + r"\b")


def lint(song, only=None, quiet=False):
    cfg_path = os.path.join(song, "lint.json")
    cfg = json.load(open(cfg_path, encoding="utf-8")) if os.path.exists(cfg_path) else {}
    exempt = [e.lower() for e in DEFAULT_EXEMPT + cfg.get("exempt", [])]
    aliases = cfg.get("aliases", {})
    spaces = cfg.get("spaces", {})
    owners = cfg.get("owners", [])
    risky = dict(DEFAULT_RISKY, **cfg.get("risky", {}))
    want_audio = cfg.get("audio")
    allow = cfg.get("allow", {})          # {"I1": {"R3": "empty boat on purpose"}} -- a reviewed, written-down exception

    rows = list(csv.DictReader(open(os.path.join(song, "shots.csv"), encoding="utf-8", newline="")))
    cast_all = set()
    for r in rows:
        cast_all.update(x for x in (r.get("ref_labels") or "").split("|") if x)
    fails = warns = n = 0
    for r in rows:
        sid = r["shot_id"]
        if only and sid not in only:
            continue
        if (r.get("engine") or "").strip().lower() != "wan3":
            continue
        n += 1
        msgs = []
        F = lambda m: msgs.append(("FAIL", m))
        W = lambda m: msgs.append(("WARN", m))

        # R7 basics
        pth = os.path.join(song, r.get("prompt", ""))
        if not r.get("prompt") or not os.path.exists(pth):
            F(f"R7 prompt file missing: {r.get('prompt')}")
            text = ""
        else:
            text = open(pth, encoding="utf-8").read().strip()
            if not text:
                F("R7 prompt file is empty")
        try:
            d = float(r.get("duration_s") or 0)
            if not 2 <= d <= 30:
                F(f"R7 duration {d} s outside 2-30")
        except ValueError:
            F(f"R7 duration not a number: {r.get('duration_s')}")
        if want_audio and (r.get("audio") or "").strip().lower() != want_audio:
            F(f"R7 audio={r.get('audio')} but this song wants audio={want_audio}")

        labels = [x for x in (r.get("ref_labels") or "").split("|") if x]
        refs = [x for x in (r.get("ref") or "").split("|") if x]
        if len(labels) != len(refs):
            F(f"R1 {len(refs)} ref files but {len(labels)} ref_labels")
        for f in refs:
            if not os.path.exists(os.path.join(song, f)):
                F(f"R1 ref file missing: {f}")
        in_refs = set(labels)

        lines = text.splitlines()
        body = text
        if labels:
            leg = parse_legend(lines[0] if lines else "")
            norm = lambda x: x.replace("-", " ").strip().lower()
            if leg is None or len(leg) != len(labels) or \
                    any(not norm(g).startswith(norm(l)) for g, l in zip(leg, labels)):
                F(f"R1 legend {leg} does not match ref_labels {labels}")
            body = "\n".join(lines[1:])
        elif lines and re.match(r"\s*Images?\s+\d", lines[0]):
            F("R1 prompt has an image legend but the row has no refs")
        if not labels:
            W("R8 no reference images -- check the style holds (object-only shots drift photoreal)")

        # R2 cast / R3 spaces, sentence by sentence; avoid-lines and exempt sentences don't put anyone in frame
        named_missing, space_hits = {}, {}
        for s in sentences(body):
            low = s.lower()
            if AVOID_START.match(s) or any(e in low for e in exempt):
                continue
            for c in cast_all:
                if c not in in_refs and name_re(c).search(s):
                    named_missing.setdefault(c, s)
            for a, members in aliases.items():
                if re.search(r"\b" + re.escape(a.lower()) + r"\b", low):
                    for c in members:
                        if c not in in_refs:
                            named_missing.setdefault(c, s)
            for sp, members in spaces.items():
                if re.search(r"\b" + re.escape(sp.lower()) + r"\b", low):
                    space_hits.setdefault(sp, s)
        for c, s in sorted(named_missing.items()):
            F(f"R2 '{c}' is in frame but not in the refs -> Wan invents them off-model. «{s[:110]}»")
        for sp, s in space_hits.items():
            members = spaces[sp]
            have = [c for c in members if c in in_refs]
            if not have:
                F(f"R3 the {sp} is in frame but none of its people ({', '.join(members)}) are referenced -> it shows up "
                  f"empty or with invented people; add the group's refs or keep the {sp} off-screen. «{s[:90]}»")
            elif len(have) < len(members):
                F(f"R3 the {sp} is in frame with only {have} referenced -> the rest get invented; reference all of "
                  f"{members}")

        # R4 exclusive actions need an ownership line
        for o in owners:
            people = spaces.get(o.get("space", ""), []) or [o["owner"]]
            if not any(c in in_refs for c in people + [o["owner"]]):
                continue
            hit = None
            for s in sentences(body):
                if AVOID_START.match(s):
                    continue
                if re.search(o["pattern"], s, re.I):
                    hit = s
                    break
            if hit and o["require"] not in body:
                F(f"R4 '{o['owner']}' must own this action but the line \"{o['require']} ...\" is missing. «{hit[:90]}»")

        # R5 timed beats
        if BEAT_RE.search(body) and not HOLD_RE.search(body.replace("One continuous shot with no cuts", "")):
            W("R5 timed beats without a shot-specific hold line -> may cut between beats; add 'the camera stays on this "
              "shot the whole time and never cuts'")
        # R6 risky words
        for pat, why in risky.items():
            for s in sentences(body):
                if AVOID_START.match(s):
                    continue
                if re.search(pat, s, re.I):
                    if "scream" in pat and re.search(r"no tears|not crying", body, re.I):
                        break
                    W(f"R6 {why}. «{s[:80]}»")
                    break

        allowed = allow.get(sid, {})
        msgs = [(("ALLOW" if k == "FAIL" and m[:2] in allowed else k), (m + f"  [allowed: {allowed[m[:2]]}]"
                 if k == "FAIL" and m[:2] in allowed else m)) for k, m in msgs]
        fs = sum(1 for k, _ in msgs if k == "FAIL")
        ws = sum(1 for k, _ in msgs if k == "WARN")
        fails += fs
        warns += ws
        if msgs or not quiet:
            print(f"{sid:6} {'FAIL' if fs else ('warn' if ws else 'ok')}")
            for k, m in msgs:
                print(f"   {k} {m}")
    print(f"LINT {'FAIL' if fails else 'PASS'}: {n} shots, {fails} fail, {warns} warn")
    return 1 if fails else 0


if __name__ == "__main__":
    try:                                   # Windows consoles default to cp1252; the report quotes prompt text (–, «»)
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--song", required=True)
    ap.add_argument("--only", default="")
    ap.add_argument("--quiet", action="store_true", help="print only shots with findings")
    a = ap.parse_args()
    if not os.path.exists(os.path.join(a.song, "shots.csv")):
        sys.exit(2)
    only = {x.strip() for x in a.only.split(",") if x.strip()} or None
    sys.exit(lint(a.song, only, a.quiet))
