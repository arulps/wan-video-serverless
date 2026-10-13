# MinMini character scale — heights and builds for every video prompt

_Generated from `comfy/character_scale.json` (version 2026-10-10) by `py comfy/scale_line.py --table`. Edit the JSON, not this file._

**Rule (Arul, 9 Oct 2026):** every character's physical size and build is passed to the video. Each prompt carries the `SIZES` line that `comfy/scale_line.py` builds for that shot's cast (ref order); `prompt_lint` R9 fails a shot without it, or with a character that has no height here or in the song's `scale.json`. The reference image must match the build too (heads tall, chubby or slim) — Wan takes body proportions from the reference before the prompt (learnings §2, §13).

Anchor: **Mintu = 1.00 m**. Children are compared to Mintu ("the tops of their heads are level"), grown-ups by where a child's head reaches (on every grown-up from 1.45 to 1.78 m it is about the waist), small creatures against a child's hand or head. Animals use the 3D staging heights (oviyan `animalHeights.ts`) where they exist; otherwise the non-human bible card size, which for four-legged, swimming and crawling characters and vehicles is read as a **length** (the model's longest side — the quadrupeds that have a staging height are all shorter than their card size).

## Children

| Character | Age | Height | vs Mintu | Build (bible words) | Source |
|---|---|---|---|---|---|
| Minnu | 5-6 | 1.02 m | 1.02× | round bright face with deep dimples, six and a half heads tall | human bible v61 + CHARACTER-HEIGHTS.md (v60: one year older than Mintu, same height) |
| Priya | 6-7 | 1.02 m | 1.02× | round bright face, rosy warm cheeks, long side braid | Arul 2026-10-09: same height as Minnu (was 1.15 m in CHARACTER-HEIGHTS.md / bible v60) |
| Mintu | 4-5 | 1.00 m | 1.00× | round chubby face, chubby hands, six and a half heads tall | human bible v61 + CHARACTER-HEIGHTS.md (locked anchor) |
| Leo | 3-4 | 0.95 m | 0.95× | round chubby face, big rosy cheeks, wild golden curls | human bible v61 + CHARACTER-HEIGHTS.md |
| Mila | 3-4 | 0.95 m | 0.95× | round chubby face, plump rosy cheeks, two afro puffs | human bible v61 + CHARACTER-HEIGHTS.md |

## Grown-ups

| Character | Age | Height | Mintu's head reaches | Build (bible words) | Source |
|---|---|---|---|---|---|
| Mr. James | late 30s | 1.78 m | waist | tall strong slim build, the tallest grown-up | human bible v61 + CHARACTER-HEIGHTS.md |
| Police Uncle | early 40s | 1.72 m | waist | tall sturdy upright build | human bible v61 (card height) |
| Doctor Uncle | early 40s | 1.70 m | waist | medium upright build | human bible v61 (card height) |
| Driver Uncle | mid 40s | 1.70 m | waist | solid dependable build | human bible v61 (card height) |
| Santa Claus | elderly | 1.70 m | waist | round plump belly | human bible v61 (card height) |
| Kalla | late 20s | 1.70 m | waist | wiry slouching build | human bible v61 (card height) |
| Mr. David | late 30s | 1.68 m | waist | tall slim build | human bible v61 + CHARACTER-HEIGHTS.md |
| Kadai Anna | early 30s | 1.68 m | waist | sturdy friendly build | human bible v61 (card height) |
| Postman Uncle | early 50s | 1.68 m | waist | lean upright build | human bible v61 (card height) |
| Ice Cream Uncle | mid 30s | 1.68 m | waist | sturdy cheerful build | human bible v61 (card height) |
| Salavaikkarar Uncle | late 30s | 1.68 m | waist | lean wiry build, long lean face | human bible v61 (card height) |
| Appa | mid 30s | 1.65 m | waist | tall lean athletic build, upright posture | human bible v61 + CHARACTER-HEIGHTS.md (locked anchor) |
| Mr. Rajan | late 30s | 1.63 m | waist | tall slim build | human bible v61 + CHARACTER-HEIGHTS.md |
| Teacher Miss | late 20s | 1.62 m | waist | slim upright build | human bible v61 (card height) |
| Ms. Amara | early 30s | 1.60 m | waist | graceful slim build | human bible v61 + CHARACTER-HEIGHTS.md |
| Librarian Aunty | late 40s | 1.60 m | waist | slim graceful build | human bible v61 (card height) |
| Amma | early 30s | 1.55 m | waist | slim build | human bible v61 + CHARACTER-HEIGHTS.md |
| Thatha | 65-70 | 1.55 m | waist | slim build, round jolly face | human bible v61 + CHARACTER-HEIGHTS.md |
| Ms. Sophie | early 30s | 1.55 m | waist | slim build | human bible v61 + CHARACTER-HEIGHTS.md |
| Mrs. Meena | early 30s | 1.52 m | waist | medium build | human bible v61 + CHARACTER-HEIGHTS.md |
| Paati | 63-68 | 1.48 m | waist | slim upright build | human bible v61 + CHARACTER-HEIGHTS.md |
| Kollu Thatha | 88-92 | 1.45 m | waist | slim upright build, very long snow-white beard | human bible v61 + CHARACTER-HEIGHTS.md |

## Mascot and creatures

| Character | What | Video size | Bible card size | In a prompt next to Mintu | Source |
|---|---|---|---|---|---|
| Thangam | little star | 0.50 m tall | 0.50 m | Thangam is about half as tall as Mintu | non-human bible v26 size_m |
| Muttai | egg fellow | 0.50 m tall | 0.50 m | Muttai is about half as tall as Mintu | non-human bible v26 size_m |
| Minmini (flying, default) | TV-firefly mascot | 0.10 m tall | 0.50 m | Minmini is a small flying firefly, about the size of a child's hand | Arul 2026-10-10 (non-human bible v26): a small flier in most scenes; up to 0.50 m only when perched, still or close up |
| Minmini (perched) | TV-firefly mascot | 0.50 m tall | | Minmini is resting or hovering still close by, up to about half a child's height | Arul 2026-10-10 (non-human bible v26): a small flier in most scenes; up to 0.50 m only when perched, still or close up — perched, hovering still, or in a close-up: up to half a child's height |

## Animals

| Character | What | Video size | Bible card size | In a prompt next to Mintu | Source |
|---|---|---|---|---|---|
| Malli | big temple elephant | 3.20 m long | 3.20 m | Malli is about 3 times as long as Mintu is tall | non-human bible v26 size_m |
| Nettai | giraffe | 3.00 m tall | 3.00 m | Nettai is about 3 times as tall as Mintu | animalHeights.ts 'giraffe' staging height (bible card 3.00 m) |
| Appu | baby elephant | 2.20 m tall | 2.20 m | Appu is about twice as tall as Mintu | animalHeights.ts 'elephant' staging height (bible card 2.20 m) |
| Thimi | whale | 1.80 m long | 1.80 m | Thimi is about one and a half times as long as Mintu is tall | non-human bible v26 size_m |
| Raja | horse | 1.45 m tall | 1.70 m | Raja is about one and a half times as tall as Mintu | animalHeights.ts 'horse' staging height (bible card 1.70 m) |
| Reindeer | reindeer | 1.40 m long | 1.40 m | Reindeer is about one and a half times as long as Mintu is tall | non-human bible v26 size_m |
| Modhu | crocodile | 1.40 m long | 1.40 m | Modhu is about one and a half times as long as Mintu is tall | non-human bible v26 size_m |
| Vari | zebra | 1.30 m long | 1.30 m | Vari is about one and a half times as long as Mintu is tall | non-human bible v26 size_m |
| Pani Karadi | polar bear | 1.30 m long | 1.30 m | Pani Karadi is about one and a half times as long as Mintu is tall | non-human bible v26 size_m |
| Karadi | bear | 1.20 m long | 1.20 m | Karadi is a little longer than Mintu is tall | non-human bible v26 size_m |
| Ammu | cow | 1.15 m tall | 1.40 m | Ammu is a little taller than Mintu | animalHeights.ts 'cow' staging height (bible card 1.40 m) |
| Singa | lion | 1.10 m long | 1.10 m | Singa is a little longer than Mintu is tall | non-human bible v26 size_m |
| Veera | tiger | 1.10 m long | 1.10 m | Veera is a little longer than Mintu is tall | non-human bible v26 size_m |
| Thulli | dolphin | 1.10 m long | 1.10 m | Thulli is a little longer than Mintu is tall | non-human bible v26 size_m |
| Chinnu | donkey | 1.05 m tall | 1.20 m | Chinnu is a little taller than Mintu | animalHeights.ts 'donkey' staging height (bible card 1.20 m) |
| Onai | wolf | 1.00 m long | 1.00 m | Onai is about as long as Mintu is tall | non-human bible v26 size_m |
| Neeri | hippo | 1.00 m long | 1.00 m | Neeri is about as long as Mintu is tall | non-human bible v26 size_m |
| Kannukutti | calf | 0.85 m tall | 0.80 m | Kannukutti is a little shorter than Mintu | animalHeights.ts 'calf' staging height (bible card 0.80 m) |
| Chella | sheep | 0.70 m tall | 0.80 m | Chella is about two-thirds as tall as Mintu | animalHeights.ts 'sheep' staging height (bible card 0.80 m) |
| Mayilu | peacock | 0.70 m tall | 0.60 m | Mayilu is about two-thirds as tall as Mintu | animalHeights.ts 'peacock' staging height (bible card 0.60 m) |
| Kadal Nai | seal | 0.70 m long | 0.70 m | Kadal Nai is about two-thirds as long as Mintu is tall | non-human bible v26 size_m |
| Kandu | goat | 0.65 m tall | 0.90 m | Kandu is about two-thirds as tall as Mintu | animalHeights.ts 'goat' staging height (bible card 0.90 m) |
| Kittu | monkey | 0.55 m tall | 0.70 m | Kittu is about half as tall as Mintu | animalHeights.ts 'monkey' staging height (bible card 0.70 m) |
| Nari | fox | 0.55 m long | 0.55 m | Nari is about half as long as Mintu is tall | non-human bible v26 size_m |
| Gundu | pig | 0.50 m tall | 0.70 m | Gundu is about half as tall as Mintu | animalHeights.ts 'pig' staging height (bible card 0.70 m) |
| Aatukutti | goat kid | 0.50 m long | 0.50 m | Aatukutti is about half as long as Mintu is tall | non-human bible v26 size_m |
| Pengu | penguin | 0.50 m tall | 0.50 m | Pengu is about half as tall as Mintu | non-human bible v26 size_m |
| Ettu | octopus | 0.50 m tall | 0.50 m | Ettu is about half as tall as Mintu | non-human bible v26 size_m |
| Biscuit | family dog | 0.45 m tall | 0.60 m | Biscuit is about half as tall as Mintu | animalHeights.ts 'dog' staging height (bible card 0.60 m) |
| Kokkarako | rooster | 0.38 m tall | 0.45 m | Kokkarako is about a third as tall as Mintu | animalHeights.ts 'rooster' staging height (bible card 0.45 m) |
| Kaaka | crow | 0.35 m tall | 0.35 m | Kaaka is about a third as tall as Mintu | non-human bible v26 size_m |
| Aamai | turtle | 0.35 m long | 0.35 m | Aamai is about a third as long as Mintu is tall | non-human bible v26 size_m |
| Kuyil | koel | 0.35 m tall | 0.35 m | Kuyil is about a third as tall as Mintu | non-human bible v26 size_m |
| Kokki | hen | 0.33 m tall | 0.35 m | Kokki is about a third as tall as Mintu | animalHeights.ts 'hen' staging height (bible card 0.35 m) |
| Misty | cat | 0.30 m tall | 0.45 m | Misty is about the size of a child's head | animalHeights.ts 'cat' staging height (bible card 0.45 m) |
| Vaathu | duck | 0.30 m tall | 0.35 m | Vaathu is about the size of a child's head | animalHeights.ts 'duck' staging height (bible card 0.35 m) |
| Anil | squirrel | 0.30 m long | 0.30 m | Anil is about the size of a child's head | non-human bible v26 size_m |
| Naaikutti | puppy | 0.30 m tall | 0.35 m | Naaikutti is about the size of a child's head | animalHeights.ts 'puppy' staging height (bible card 0.35 m) |
| Jelli | jellyfish | 0.30 m tall | 0.30 m | Jelli is about the size of a child's head | non-human bible v26 size_m |
| White Puppy | white puppy dog | 0.30 m tall | 0.30 m | White Puppy is about the size of a child's head | animalHeights.ts 'puppy' staging height (bible card 0.30 m) |
| Kutti Muyal | bunny | 0.28 m tall | 0.80 m | Kutti Muyal is about the size of a child's head | animalHeights.ts 'bunny' staging height (bible card 0.80 m) |
| Meenu | fish | 0.25 m long | 0.25 m | Meenu is about the size of a child's head | non-human bible v26 size_m |
| Kili | green parrot | 0.25 m tall | 0.30 m | Kili is about the size of a child's head | animalHeights.ts 'parrot' staging height (bible card 0.30 m) |
| Kambali | caterpillar | 0.25 m long | 0.25 m | Kambali is about the size of a child's head | non-human bible v26 size_m |
| Vanna | butterfly | 0.25 m tall | 0.25 m | Vanna is about the size of a child's head | non-human bible v26 size_m |
| Thavva | frog | 0.15 m tall | 0.20 m | Thavva is about one and a half times the size of a child's hand | animalHeights.ts 'frog' staging height (bible card 0.20 m) |
| Sili | small spider | 0.15 m long | 0.15 m | Sili is about one and a half times the size of a child's hand | non-human bible v26 size_m |
| Nathai | snail | 0.15 m long | 0.15 m | Nathai is about one and a half times the size of a child's hand | non-human bible v26 size_m |
| Vandu | bumblebee | 0.15 m tall | 0.15 m | Vandu is about one and a half times the size of a child's hand | non-human bible v26 size_m |
| Grasshopper | grasshopper | 0.15 m long | 0.15 m | Grasshopper is about one and a half times the size of a child's hand | non-human bible v26 size_m |
| Kuruvi | sparrow | 0.12 m tall | 0.12 m | Kuruvi is about the size of a child's hand | animalHeights.ts 'sparrow' staging height (bible card 0.12 m) |
| Pulli | ladybug | 0.12 m long | 0.12 m | Pulli is about the size of a child's hand | non-human bible v26 size_m |
| Erumbu | ant | 0.12 m long | 0.12 m | Erumbu is about the size of a child's hand | non-human bible v26 size_m |
| Chiku | mouse | 0.10 m tall | 0.10 m | Chiku is no bigger than a child's hand | Arul 2026-10-10: non-human bible v26 corrected 0.5 m to ~0.10 m, a child's hand |

## Vehicles

| Character | What | Video size | Bible card size | In a prompt next to Mintu | Source |
|---|---|---|---|---|---|
| Rocky | train | 2.50 m long | 2.50 m | Rocky is about twice as long as Mintu is tall | non-human bible v26 size_m — vehicle: the size is its length |
| Putt-Putt | auto-rickshaw | 1.60 m long | 1.60 m | Putt-Putt is about one and a half times as long as Mintu is tall | non-human bible v26 size_m — vehicle: the size is its length |
| Zippy | family car | 1.40 m long | 1.40 m | Zippy is about one and a half times as long as Mintu is tall | non-human bible v26 size_m — vehicle: the size is its length |
| Turbo | motorbike | 1.10 m long | 1.10 m | Turbo is a little longer than Mintu is tall | non-human bible v26 size_m — vehicle: the size is its length |
| Breezy | bicycle | 1.00 m long | 1.00 m | Breezy is about as long as Mintu is tall | non-human bible v26 size_m — vehicle: the size is its length |

## Sky

| Character | What | Video size | Bible card size | In a prompt next to Mintu | Source |
|---|---|---|---|---|---|
| Smiling Sun | sun | 1.50 m tall | 1.50 m | Smiling Sun is a big friendly face high in the sky, far away behind everyone — never down on the ground | non-human bible v26 size_m — sky object: its size in frame is a staging choice; size_m is the model scale |
| Sleepy Moon | moon | 1.20 m tall | 1.20 m | Sleepy Moon is a big friendly face high in the sky, far away behind everyone — never down on the ground | non-human bible v26 size_m — sky object: its size in frame is a staging choice; size_m is the model scale |

## Song-only characters

Kept per song in `songs/<slug>/scale.json` (same fields; `same_as` borrows a canon entry):

**a07-butterfly**

| Character | Height | Build | Source |
|---|---|---|---|
| Red Butterfly | 0.25 m | butterfly | same as Vanna (non-human bible v26 size_m) |
| Yellow Butterfly | 0.25 m | butterfly | same as Vanna (non-human bible v26 size_m) |
| Blue Butterfly | 0.25 m | butterfly | same as Vanna (non-human bible v26 size_m) |
| Green Butterfly | 0.25 m | butterfly | same as Vanna (non-human bible v26 size_m) |

**a12-karadi-w3**

| Character | Height | Build | Source |
|---|---|---|---|
| Karadi Mama | 1.90 m | big round body with a soft cream tummy, stands and walks upright on two legs | A12 concept (Arul 10 Oct): a big grown-up bear, taller than Appa standing |
| the rabbit | 0.28 m | bunny | same as Kutti Muyal (animalHeights.ts 'bunny' staging height (bible card 0.80 m)) |
| the squirrel | 0.30 m | squirrel | same as Anil (non-human bible v26 size_m) |

**l05-urulai-w3**

| Character | Height | Build | Source |
|---|---|---|---|
| Baby Potato | 0.11 m | tiny round baby potato, stubby arms and legs | L05 runsheet rev 2.7 (KIDS_SCALE) |
| Brinjal | 0.11 m | plump egg shape, wider at the bottom | L05 runsheet rev 2.7: about Baby Potato's height |
| Tomato | 0.11 m | round, a little wider than tall, roly-poly | L05 runsheet rev 2.7: the same height as Baby Potato |
| Cabbage | 0.13 m | round, about twice as wide as Baby Potato | L05 runsheet rev 2.7: a little taller than Baby Potato |
| Amma Potato | 0.17 m | bigger oval mother potato | L05 runsheet rev 2.7: about 1.5x the little vegetables |
| Okra | 0.17 m | one slim upright pod, three times as tall as wide | L05 runsheet rev 2.7: about 1.5x Baby Potato |
| Carrot | 0.17 m | tall upright carrot with a leaf tuft and big floppy feet | L05 runsheet rev 2.7: about 1.5x Baby Potato |
| Radish | 0.17 m | long white upright radish with a leaf tuft | L05 runsheet rev 2.7: about 1.5x Baby Potato |
| Beans | 0.17 m | one chunky, gently curved bean pod | L05 runsheet rev 2.7: about 1.5x Baby Potato |

