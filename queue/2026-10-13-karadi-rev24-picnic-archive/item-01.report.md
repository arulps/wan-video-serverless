# item-01 report — DONE: picnic takes, sidecars, QC sheets and the rev 1.x cut plan copied into the song folder — $0.00

Run by CC (A12 watcher), 2026-10-14 00:01–00:03 Toronto. Copy only (`cp -n`: never overwrites, never moves). Nothing in the repo's
`out\` changed. The clips were not judged.

Destination: `C:\Channel Contents\MinMiniKids\songs\A12-Karadi Mama\_picnic-version\takes\` (new; `README.md` and `_gen\` beside it
untouched).

## Summary
- **228 files, 485 MB.** 227 copied with `cp -n`, plus `cutplan-rev1.6.json` (see below). **Skipped: none** (the folder was new and
  empty, so nothing already existed).
- **22 mp4 files, 18 distinct clip IDs** (as expected): CAa CAb CQa CQb HKa HKb I1 O1 O2 O3 V1A V1Q V2A V2Q V3A V3Q V4A V4Q.
  - 14 from `out\_rev1x-2026-10-13\` (the rev 1.x takes moved aside, including HKa and O1);
  - `V1A`–`V4A-seed30313-w3.mp4` (rev 1.5 verse answers, still used by the trek — copies) and their `-v1-picnic.mp4` takes (rev 1.4).
- Sidecars (`.json`): the two in `out\_rev1x-2026-10-13\` (HKa, O1), the eight for V1A–V4A (both versions), and — beyond the item's
  wording — the **12 rev 1.x sidecars still at the top of `out\`** (CAa CAb CQa CQb HKb I1 O2 O3 V1Q V2Q V3Q V4Q). The item assumed all
  sidecars had been moved with their takes; they had not (the rev 2.1 queue moved `.mp4` only), so without these 12 the archive would
  have no sidecar for 12 of its takes. The new rev 2 `O1-seed30313-w3.json` (recovered tonight) was **not** copied.
- QC sheets: the 41 `out\_qc\*-v1-picnic*` files, the 20 in `out\_qc\_rev1x-2026-10-13\` (HKa, O1), and — beyond the item's wording —
  the **122 rev 1.x sheets still under plain names in `out\_qc\`** for the same 12 IDs (they were never moved aside). The new
  `O1-strip.png` (rev 2) was **not** copied.

## The cut plan — deviation, please check
The item says to copy `cutplan.json` → `takes\cutplan-rev1.6.json` as "the picnic slot plan". **The current `cutplan.json` is no longer
the picnic plan**: the rev 2.0 and 2.1 builds rewrote it for the family trek (21 clips). Copying it would have saved the trek plan
under a picnic name. CC instead wrote the **last picnic version from git** — `git show 322c4a1:songs/a12-karadi-w3/cutplan.json`
(the plan the ROUGH and ROUGH2 cuts were made from; 53 slots = TA 29 + EN 24, **18 distinct clips**) — as `cutplan-rev1.6.json`.
If Fable wanted the current file regardless, it is still in the repo and can be copied over.

## Listing of `takes\` (bytes, name)
```
     1593403  CAa-contact.png
     2485812  CAa-every4-all.png
     1131786  CAa-every4-first2s.png
     1077457  CAa-f000.png
     1176661  CAa-f030.png
     1181574  CAa-f060.png
     1151398  CAa-f120.png
     1110908  CAa-f180.png
     1076887  CAa-f239.png
        4749  CAa-seed30313-w3.json
     8464577  CAa-seed30313-w3.mp4
     5781712  CAa-strip.png
     1598318  CAb-contact.png
     2515577  CAb-every4-all.png
     1088782  CAb-f000.png
     1183583  CAb-f030.png
     1181225  CAb-f060.png
     1184349  CAb-f090.png
     1140669  CAb-f120.png
     1120803  CAb-f150.png
     1080429  CAb-f239.png
        4746  CAb-seed30313-w3.json
     8549520  CAb-seed30313-w3.mp4
     5778927  CAb-strip.png
     1611033  CQa-contact.png
     2669803  CQa-every4-all.png
     1233157  CQa-every4-first2s.png
     1116533  CQa-f000.png
     1186815  CQa-f030.png
     1156030  CQa-f060.png
     1130776  CQa-f120.png
     1112142  CQa-f180.png
     1143744  CQa-f239.png
        6252  CQa-seed30313-w3.json
     9555857  CQa-seed30313-w3.mp4
     5753478  CQa-strip.png
     1602993  CQb-contact.png
     2684091  CQb-every4-all.png
     1111835  CQb-f000.png
     1154748  CQb-f030.png
     1139753  CQb-f060.png
     1118730  CQb-f090.png
     1130307  CQb-f120.png
     1100311  CQb-f150.png
     1131389  CQb-f239.png
        6303  CQb-seed30313-w3.json
    10066402  CQb-seed30313-w3.mp4
     5726830  CQb-strip.png
     1598733  HKa-contact.png
     2709647  HKa-every4-all.png
     1108257  HKa-f000.png
     1107345  HKa-f030.png
     1096879  HKa-f060.png
     1093585  HKa-f090.png
     1090973  HKa-f120.png
     1128915  HKa-f150.png
     1035078  HKa-f239.png
        4243  HKa-seed30313-w3.json
    11528753  HKa-seed30313-w3.mp4
     5549324  HKa-strip.png
     1640054  HKb-contact.png
     2737796  HKb-every4-all.png
     1135811  HKb-f000.png
     1172474  HKb-f030.png
     1167962  HKb-f060.png
     1168078  HKb-f090.png
     1148358  HKb-f120.png
     1169584  HKb-f150.png
     1144780  HKb-f239.png
        5709  HKb-seed30313-w3.json
     9712256  HKb-seed30313-w3.mp4
     5797858  HKb-strip.png
     1606513  I1-contact.png
     2405498  I1-every4-all.png
     1135775  I1-f000.png
     1165790  I1-f030.png
     1156710  I1-f060.png
     1120947  I1-f090.png
     1110606  I1-f120.png
     1071761  I1-f150.png
     1088543  I1-f209.png
        5999  I1-seed30313-w3.json
     9126994  I1-seed30313-w3.mp4
     5815577  I1-strip.png
     1638949  O1-contact.png
     2438476  O1-every4-all.png
     1145908  O1-f000.png
     1167191  O1-f030.png
     1182604  O1-f060.png
     1159112  O1-f090.png
     1177640  O1-f120.png
     1143113  O1-f150.png
     1150413  O1-f209.png
        7283  O1-seed30313-w3.json
     9535535  O1-seed30313-w3.mp4
     5888405  O1-strip.png
     1622048  O2-contact.png
     2308743  O2-every4-all.png
     1128426  O2-f000.png
     1182846  O2-f030.png
     1163783  O2-f060.png
     1176671  O2-f090.png
     1178456  O2-f120.png
     1176911  O2-f150.png
     1181365  O2-f209.png
        7544  O2-seed30313-w3.json
     9869027  O2-seed30313-w3.mp4
     5821531  O2-strip.png
     1632499  O3-contact.png
     2348450  O3-every4-all.png
     1219952  O3-every4-first2s.png
     1153124  O3-f000.png
     1208013  O3-f030.png
     1178874  O3-f060.png
     1190682  O3-f090.png
     1167928  O3-f120.png
     1179387  O3-f150.png
     1157856  O3-f209.png
        8192  O3-seed30313-w3.json
     8254817  O3-seed30313-w3.mp4
     5915202  O3-strip.png
     1546582  V1A-contact-v1-picnic.png
     1702370  V1A-every4-all-v1-picnic.png
     1059663  V1A-f000-v1-picnic.png
     1139413  V1A-f030-v1-picnic.png
     1164384  V1A-f060-v1-picnic.png
     1152946  V1A-f090-v1-picnic.png
     1158548  V1A-f120-v1-picnic.png
     1160866  V1A-f150-v1-picnic.png
     1158882  V1A-f179-v1-picnic.png
        4279  V1A-seed30313-w3-v1-picnic.json
     5377988  V1A-seed30313-w3-v1-picnic.mp4
        4501  V1A-seed30313-w3.json
     8019321  V1A-seed30313-w3.mp4
     5667659  V1A-strip-v1-picnic.png
     1606294  V1Q-contact.png
     2017936  V1Q-every4-all.png
     1163097  V1Q-f000.png
     1166574  V1Q-f030.png
     1161386  V1Q-f060.png
     1143603  V1Q-f090.png
     1133744  V1Q-f120.png
     1116431  V1Q-f150.png
     1122674  V1Q-f179.png
        4673  V1Q-seed30313-w3.json
     7127647  V1Q-seed30313-w3.mp4
     5813494  V1Q-strip.png
     1608538  V2A-contact-v1-picnic.png
     1933183  V2A-every4-all-v1-picnic.png
     1131063  V2A-f000-v1-picnic.png
     1177596  V2A-f030-v1-picnic.png
     1175171  V2A-f060-v1-picnic.png
     1188648  V2A-f090-v1-picnic.png
     1181935  V2A-f120-v1-picnic.png
     1164937  V2A-f150-v1-picnic.png
     1164297  V2A-f179-v1-picnic.png
        4900  V2A-seed30313-w3-v1-picnic.json
     6599906  V2A-seed30313-w3-v1-picnic.mp4
        4585  V2A-seed30313-w3.json
     8327415  V2A-seed30313-w3.mp4
     5839025  V2A-strip-v1-picnic.png
     1578977  V2Q-contact.png
     1696622  V2Q-every4-all.png
     1108304  V2Q-f000.png
     1186916  V2Q-f030.png
     1190536  V2Q-f060.png
     1192234  V2Q-f090.png
     1187526  V2Q-f120.png
     1192167  V2Q-f150.png
     1185356  V2Q-f179.png
        4678  V2Q-seed30313-w3.json
     5681506  V2Q-seed30313-w3.mp4
     5828099  V2Q-strip.png
     1606813  V3A-contact-v1-picnic.png
     2049374  V3A-every4-all-v1-picnic.png
     1119035  V3A-f000-v1-picnic.png
     1139363  V3A-f030-v1-picnic.png
     1126040  V3A-f060-v1-picnic.png
     1089276  V3A-f090-v1-picnic.png
     1127795  V3A-f120-v1-picnic.png
     1109584  V3A-f150-v1-picnic.png
     1115457  V3A-f179-v1-picnic.png
        6022  V3A-seed30313-w3-v1-picnic.json
     8440281  V3A-seed30313-w3-v1-picnic.mp4
        5879  V3A-seed30313-w3.json
    10187556  V3A-seed30313-w3.mp4
     5695495  V3A-strip-v1-picnic.png
     1600484  V3Q-contact.png
     2041044  V3Q-every4-all.png
     1245379  V3Q-every4-first2s.png
     1108134  V3Q-f000.png
     1151581  V3Q-f030.png
     1135301  V3Q-f060.png
     1134357  V3Q-f090.png
     1099854  V3Q-f120.png
     1110742  V3Q-f150.png
     1103363  V3Q-f179.png
        5927  V3Q-seed30313-w3.json
     7491864  V3Q-seed30313-w3.mp4
     5679362  V3Q-strip.png
     1617149  V4A-contact-v1-picnic.png
     2049372  V4A-every4-all-v1-picnic.png
     1245951  V4A-every4-first2s-v1-picnic.png
     1133573  V4A-f000-v1-picnic.png
     1157940  V4A-f030-v1-picnic.png
     1149132  V4A-f060-v1-picnic.png
     1140934  V4A-f090-v1-picnic.png
     1126569  V4A-f120-v1-picnic.png
     1109074  V4A-f150-v1-picnic.png
     1122863  V4A-f179-v1-picnic.png
        6161  V4A-seed30313-w3-v1-picnic.json
     8053046  V4A-seed30313-w3-v1-picnic.mp4
        5941  V4A-seed30313-w3.json
     9370700  V4A-seed30313-w3.mp4
     5781429  V4A-strip-v1-picnic.png
     1599473  V4Q-contact.png
     1953510  V4Q-every4-all.png
     1183789  V4Q-f000.png
     1181271  V4Q-f030.png
     1164339  V4Q-f060.png
     1152511  V4Q-f090.png
     1169342  V4Q-f120.png
     1129261  V4Q-f150.png
     1117252  V4Q-f179.png
        5038  V4Q-seed30313-w3.json
     6800755  V4Q-seed30313-w3.mp4
     5871072  V4Q-strip.png
       24191  cutplan-rev1.6.json
```

## Commit
`[skip ci]`: `queue/2026-10-13-karadi-rev24-picnic-archive` and `queue/A12-WATCH-LOG.md` only. The hash is in this folder's `LOG.md` and `item-01.done` (this report is inside that commit).
