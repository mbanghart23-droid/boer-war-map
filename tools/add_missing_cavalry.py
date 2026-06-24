"""
Add 3 missing British regular cavalry regiments:
  1st (King's) Dragoon Guards — arrived Cape Colony Jan 1901
  2nd Dragoons (Royal Scots Greys) — arrived Cape Dec 1899
  8th (King's Royal Irish) Hussars — arrived Cape Town 9 Mar 1900

Sources: angloboerwar.com; scotsdg.org.uk; qrhmuseum.com; Wikipedia
"""
import csv, re
from pathlib import Path
from collections import defaultdict

CSV_PATH = Path(__file__).parent.parent / "data" / "movements.csv"
BUILD_MAP = Path(__file__).parent.parent / "build_map.py"

rows = list(csv.DictReader(open(CSV_PATH, encoding="utf-8")))
COLS = list(rows[0].keys())
by_force = defaultdict(list)
for r in rows: by_force[r["force"]].append(r)
max_id = max(int(r["id"]) for r in rows if r["id"].isdigit())
nid = [max_id + 1]
def nxt(): i = nid[0]; nid[0] += 1; return str(i)

new_rows = []
a_entries = []

def add(force, side, date_start, event_type, action_place, description,
        from_place="", to_place="", date_end="", commander="", confidence="low",
        source="angloboerwar.com; scotsdg.org.uk; qrhmuseum.com",
        note="Auto-generated from regimental histories (add_missing_cavalry.py); verify against unit diary"):
    rid = nxt()
    tp = to_place or action_place
    new_rows.append({
        "id": rid, "side": side, "force": force,
        "commander": commander, "units": force,
        "date_start": date_start, "date_end": date_end,
        "event_type": event_type,
        "from_place": from_place, "to_place": tp, "action_place": action_place,
        "description": description,
        "confidence": confidence, "source": source, "note": note,
    })
    reg = "north"
    if from_place and from_place != action_place:
        a_entries.append(' "%s": dict(pt="%s", line=(%r, %r), region="%s"),' % (
            rid, action_place, from_place, action_place, reg))
    else:
        a_entries.append(' "%s": dict(pt="%s", region="%s"),' % (rid, action_place, reg))

# ── 2nd DRAGOONS (ROYAL SCOTS GREYS) ─────────────────────────────────────────
# Arrived Cape ~7 Dec 1899; 1st Cav Brigade (Porter) with 6th DG and 6th Dragoons;
# Relief of Kimberley Feb 1900; Paardeberg; advance to Bloemfontein and Pretoria;
# Diamond Hill Jun 1900; guerrilla phase 1901-02
F2DG = "2nd Dragoons (Royal Scots Greys)"
add(F2DG, "British", "1899-12-07", "disembark", "Cape Town",
    "2nd Dragoons (Royal Scots Greys) arrived at Cape Colony aboard SS British Princess and Ranee, ~7 December 1899. Initially employed on patrol and line-of-communication protection between the Orange and Modder Rivers.",
    commander="Lt Col")
add(F2DG, "British", "1900-01-15", "redeployment", "Kimberley",
    "Royal Scots Greys assigned to 1st Cavalry Brigade (Brig Gen Porter) alongside 6th Dragoon Guards and a squadron of 6th Dragoons, plus two Australian squadrons attached. Moved to Modder River area in preparation for Roberts's advance.",
    from_place="Cape Town")
add(F2DG, "British", "1900-02-15", "engagement", "Kimberley",
    "Royal Scots Greys engaged in the Relief of Kimberley, 15 February 1900. Heavy fighting outside Kimberley on 16 February; Lt Bunbury mortally wounded, Lts Fordyce and Long severely wounded.",
    from_place="Kimberley")
add(F2DG, "British", "1900-02-18", "engagement", "Bloemfontein",
    "Royal Scots Greys present at Paardeberg operations, February 1900, following the encirclement of Cronje's force.",
    from_place="Kimberley")
add(F2DG, "British", "1900-06-11", "engagement", "Pretoria",
    "Royal Scots Greys present at the Battle of Diamond Hill, 11-12 June 1900, east of Pretoria.",
    from_place="Bloemfontein")
add(F2DG, "British", "1901-01-01", "redeployment", "Pretoria",
    "Royal Scots Greys continued column operations in the Transvaal during the guerrilla phase, 1901-02.",
    from_place="Pretoria")

# ── 1st (KING'S) DRAGOON GUARDS ───────────────────────────────────────────────
# Arrived Cape Colony late Jan 1901 (sailed on Maplemore, 8 Jan 1901);
# Formed brigade with Prince of Wales's Light Horse and G Battery RHA under Col Bethune;
# Close pursuit of De Wet; Lt Col Owen under Gen Plumer captured De Wet's 15-pdr and pom-pom;
# Cape Colony operations 1901-02
F1KDG = "1st (King's) Dragoon Guards"
add(F1KDG, "British", "1901-01-28", "disembark", "Cape Town",
    "1st (King's) Dragoon Guards arrived Cape Colony, late January 1901, having sailed on SS Maplemore from England 8 January 1901. Kitchener noted their 'timely arrival'. Formed into a brigade with Prince of Wales's Light Horse and G Battery RHA under Colonel Bethune.",
    commander="Lt Col Owen")
add(F1KDG, "British", "1901-03-01", "redeployment", "Bloemfontein",
    "1st (King's) Dragoon Guards deployed into the OFS in pursuit of De Wet's commando. Lt Col Owen commanding the regiment's mounted troops under General Plumer captured De Wet's 15-pounder gun and a pom-pom in close pursuit operations.",
    from_place="Cape Town", commander="Lt Col Owen")
add(F1KDG, "British", "1901-06-01", "redeployment", "Johannesburg",
    "1st (King's) Dragoon Guards continuing column operations in the Transvaal, 1901-02, as part of the blockhouse and drive strategy.",
    from_place="Bloemfontein", commander="Lt Col Owen")
add(F1KDG, "British", "1902-05-31", "redeployment", "Cape Town",
    "1st (King's) Dragoon Guards stood down on conclusion of the Peace of Vereeniging, 31 May 1902.",
    from_place="Johannesburg")

# ── 8th (KING'S ROYAL IRISH) HUSSARS ─────────────────────────────────────────
# Mobilised 26 Dec 1899 at Curragh; left 13 Feb 1900 on SS Norseman;
# Arrived Cape Town 9 Mar 1900; 4th Cav Brigade (Brig Gen Dickson) with 7th DG and 14th Hussars;
# Houtnek 1 May 1900 (Hamilton's force); Oct 1900 march Machadodorp to Heidelberg (heavy fighting at Geluk);
# Bothaville 6 Nov 1900 (Col Le Gallais killed); Eastern Transvaal and Zululand border 1901-02;
# Col Mahon (ex-8th Hussars) led Mafeking Relief column
F8H = "8th (King's Royal Irish) Hussars"
add(F8H, "British", "1900-03-09", "disembark", "Cape Town",
    "8th (King's Royal Irish) Hussars arrived Cape Town 9 March 1900, having sailed from Queenstown 13 February on SS Norseman. Mobilised at the Curragh 26 December 1899. Force: 19 officers, 586 NCOs and men, 458 troop horses.",
    commander="Col Clowes")
add(F8H, "British", "1900-04-01", "redeployment", "Bloemfontein",
    "8th Hussars assigned to 4th Cavalry Brigade (Brig Gen Dickson) alongside 7th Dragoon Guards and 14th Hussars. Joined Roberts's advance into the OFS.",
    from_place="Cape Town", commander="Col Clowes")
add(F8H, "British", "1900-05-01", "engagement", "Pretoria",
    "8th Hussars engaged at Houtnek, 1 May 1900, as part of Gen Hamilton's force. Roberts telegraphed: 'Hamilton speaks in high terms of the services of the 8th Hussars under Colonel Clowes... which assisted in making the Boers evacuate their position.'",
    from_place="Bloemfontein", commander="Col Clowes")
add(F8H, "British", "1900-11-06", "engagement", "Pretoria",
    "8th Hussars present at Battle of Bothaville, 6 November 1900. Colonel Le Gallais (8th Hussars), commanding mounted infantry, inflicted a severe defeat on De Wet and was killed at the moment of victory. One of the most costly days for the regiment.",
    from_place="Pretoria", commander="Col Le Gallais")
add(F8H, "British", "1900-10-13", "engagement", "Johannesburg",
    "8th Hussars heavily engaged near Geluk, 13 October 1900, on the march from Machadodorp to Heidelberg under Colonel Mahon. Against 1,100 Boers with four guns; 2 officers and 7 men killed, 2 officers and 8 men wounded.",
    from_place="Pretoria", commander="Col Mahon")
add(F8H, "British", "1901-01-01", "redeployment", "Johannesburg",
    "8th Hussars' operations during 1901-02 centred on the Eastern Transvaal to the borders of Zululand, column and pursuit work.",
    from_place="Johannesburg", commander="")
add(F8H, "British", "1902-05-31", "redeployment", "Cape Town",
    "8th (King's Royal Irish) Hussars stood down following the Peace of Vereeniging.",
    from_place="Johannesburg")

# ── WRITE ─────────────────────────────────────────────────────────────────────
print("New rows: %d  (IDs %d-%d)" % (len(new_rows), max_id + 1, nid[0] - 1))
all_rows = rows + new_rows
with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(all_rows)
print("CSV written: %d rows, %d forces" % (
    len(all_rows), len(set(r["force"] for r in all_rows))))

bp = open(BUILD_MAP, encoding="utf-8").read()
m = None
for mm in re.finditer(r'( "\d+": dict\([^\n]+\),\n)', bp):
    m = mm
if m:
    marker_end = m.end()
    if bp[marker_end] == '}':
        before, after = bp[:marker_end], bp[marker_end + 1:]
    else:
        cp = bp.find('\n}', marker_end)
        before, after = bp[:cp + 1], bp[cp + 2:]
    open(BUILD_MAP, "w", encoding="utf-8").write(
        before + '\n'.join(a_entries) + '\n}' + after)
    print("A dict entries injected: %d" % len(a_entries))
else:
    print("ERROR: no injection point")
