"""
Add Imperial Yeomanry battalions 1st–39th as individual forces.
Sources:
  - Wikipedia: List of Imperial Yeomanry units of the Second Boer War
  - SAMHS journal vol136sw: 'The Imperial Yeomanry Part One 1900'
  - saartillery.wordpress.com: 'The Imperial Yeomanry Part Two 1901'
  - Pakenham 'The Boer War'; Conan Doyle 'The Great Boer War'
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

SRC = "Wikipedia: List of Imperial Yeomanry units Second Boer War; SAMHS journal; Pakenham 'The Boer War'; Conan Doyle 'The Great Boer War'"
NOTE = "Auto-generated from IY battalion roster (add_iy_battalions.py); verify against unit history"
LOW = "low"

new_rows = []
a_entries = []

def add(force, date_start, event_type, action_place, description,
        from_place="", to_place="", date_end="", commander=""):
    rid = nxt()
    tp = to_place or action_place
    new_rows.append({
        "id": rid, "side": "British", "force": force,
        "commander": commander, "units": force,
        "date_start": date_start, "date_end": date_end,
        "event_type": event_type,
        "from_place": from_place, "to_place": tp, "action_place": action_place,
        "description": description,
        "confidence": LOW, "source": SRC, "note": NOTE,
    })
    reg = "north"
    if from_place and from_place != action_place:
        a_entries.append(' "%s": dict(pt="%s", line=(%r, %r), region="%s"),' % (
            rid, action_place, from_place, action_place, reg))
    else:
        a_entries.append(' "%s": dict(pt="%s", region="%s"),' % (rid, action_place, reg))

# ── IY BATTALION DEFINITIONS ──────────────────────────────────────────────────
# (name, county/nickname, arrive_date, contingent_note, special_events)
# special_events: list of (date, event_type, place, desc, from_place)

BATTALIONS = [
    # First contingent — all arrived Jan–Apr 1900
    ("1st Battalion Imperial Yeomanry",
     "Wiltshire; companies 1–4 (Wiltshire companies)",
     "1900-02-06", "First Contingent",
     []),
    ("2nd Battalion Imperial Yeomanry",
     "Cheshire/Lancashire; companies 5, 21, 22, 32",
     "1900-02-10", "First Contingent",
     []),
    ("3rd Battalion Imperial Yeomanry",
     "Yorkshire; companies 9 (Yorkshire), 10 (Sherwood Rangers), 11, 12 (South Nottingham)",
     "1900-02-15", "First Contingent",
     []),
    ("4th Battalion Imperial Yeomanry",
     "Midlands/Shropshire; companies 6, 7, 8, 28",
     "1900-02-20", "First Contingent",
     []),
    ("5th Battalion Imperial Yeomanry",
     "Northumberland/Northern; companies 13–16. Suffered heavy losses at Tweebosch, 7 Mar 1902.",
     "1900-02-20", "First Contingent",
     [("1902-03-07", "engagement", "Vryburg",
       "5th Battalion IY suffered significant losses at the Battle of Tweebosch (7 March 1902), where De la Rey ambushed Methuen's column. The 86th (Rough Riders) Company also present. One of the last major British reverses of the war.",
       "Vryburg")]),
    ("6th Battalion Imperial Yeomanry",
     "Scottish; companies 17–20. The Scottish IY companies, later contributing to Scottish Horse raised independently.",
     "1900-02-25", "First Contingent",
     []),
    ("7th Battalion Imperial Yeomanry",
     "West Country (Somerset, Dorset, Devon, Cornwall); companies 25–28",
     "1900-03-01", "First Contingent",
     []),
    ("8th Battalion Imperial Yeomanry",
     "Lancashire; companies 23, 24, 77",
     "1900-03-01", "First Contingent",
     []),
    ("9th Battalion Imperial Yeomanry",
     "Welsh; companies 29–31, 49",
     "1900-03-05", "First Contingent",
     []),
    ("10th Battalion Imperial Yeomanry",
     "Home Counties (Bucks, Beds, Berks, Herts, Oxford); companies 37–40. Present at Battle of Boshof, April 1900.",
     "1900-03-05", "First Contingent",
     [("1900-04-05", "engagement", "Kimberley",
       "10th Battalion IY engaged at the Battle of Boshof (5 April 1900) alongside the 3rd Battalion and Australian troops under Col Plumer.",
       "Kimberley")]),
    ("11th Battalion Imperial Yeomanry",
     "Kent/Middlesex/Sussex; companies 33–36. Nearly annihilated at Battle of Groenkop, Dec 1901.",
     "1900-03-10", "First Contingent",
     [("1901-12-25", "engagement", "Bloemfontein",
       "11th Battalion IY nearly annihilated at the Battle of Groenkop (Christmas Day 1901) in the OFS. A night surprise attack by De Wet's forces inflicted over 250 casualties.",
       "Bloemfontein")]),
    ("12th Battalion Imperial Yeomanry",
     "Eastern Counties (Norfolk, Suffolk, Essex, Cambridge); companies 41–44. The battalion never operated as a fully formed unit.",
     "1900-03-10", "First Contingent",
     []),
    ("13th Battalion Imperial Yeomanry",
     "Irish (Duke of Cambridge's Own); companies 45, 46, 47, 54. Ambushed at Lindley 27 May 1900 — 80 killed, 530 captured.",
     "1900-03-15", "First Contingent",
     [("1900-05-27", "engagement", "Pretoria",
       "13th Battalion IY (Duke of Cambridge's Own) ambushed and surrounded by 2,500 Boers under Christiaan de Wet at Lindley, OFS, 27 May 1900. Suffered 80 killed and 530 captured — one of the worst British disasters of the war. The Irish companies (45th Dublin, 46th, 47th) and the 54th Donegal company were largely destroyed.",
       "Pretoria")]),
    ("14th Battalion Imperial Yeomanry",
     "Various Midlands/Northern counties; companies 53, 55, 62, 69",
     "1900-03-20", "First Contingent",
     []),
    ("15th Battalion Imperial Yeomanry",
     "Various English counties; companies 56–59",
     "1900-03-20", "First Contingent",
     []),
    ("16th Battalion Imperial Yeomanry",
     "Various; companies 63, 66, 74 (74th Dublin company earned distinction at Rooikopjes Aug 1901)",
     "1900-03-25", "First Contingent",
     []),
    ("17th Battalion Imperial Yeomanry",
     "Various; companies 50, 60 (North Irish Horse), 61 (South Irish Horse), 65",
     "1900-03-25", "First Contingent",
     []),
    ("18th Battalion Imperial Yeomanry (Sharpshooters)",
     "London Sharpshooters; companies 67, 70, 71, 75. Raised by Earl of Dunraven from London expert marksmen.",
     "1900-03-28", "First Contingent",
     []),
    ("19th Battalion Imperial Yeomanry (Paget's Horse)",
     "Paget's Horse; companies 51, 52, 68, 73. Raised by George Paget from Berkshire/London gentry. Elite mounted unit.",
     "1900-03-28", "First Contingent",
     []),
    ("20th Battalion Imperial Yeomanry (Rough Riders)",
     "City of London Rough Riders; companies 72, 76, 78, 79. Raised by Earl of Lathom. Later perpetuated as City of London Yeomanry (Rough Riders).",
     "1900-04-01", "First Contingent",
     []),
    # Second contingent — arrived Feb–Jun 1901
    ("21st Battalion Imperial Yeomanry (2nd Sharpshooters)",
     "2nd Sharpshooters; Second Contingent raised early 1901, continuing the Sharpshooters tradition.",
     "1901-04-01", "Second Contingent",
     []),
    ("22nd Battalion Imperial Yeomanry (2nd Rough Riders)",
     "2nd Rough Riders; Second Contingent, City of London Yeomanry.",
     "1901-04-01", "Second Contingent",
     []),
    ("23rd Battalion Imperial Yeomanry (3rd Sharpshooters)",
     "3rd Sharpshooters; Second Contingent.",
     "1901-05-01", "Second Contingent",
     []),
    ("24th Battalion Imperial Yeomanry (Metropolitan Mounted Rifles)",
     "Metropolitan Mounted Rifles; recruited from London and home counties for Second Contingent.",
     "1901-05-01", "Second Contingent",
     []),
    ("25th Battalion Imperial Yeomanry",
     "Various; Third Contingent 1901.",
     "1901-08-01", "Third Contingent",
     []),
    ("26th Battalion Imperial Yeomanry (Younghusband's Horse)",
     "Younghusband's Horse; raised by Sir George Younghusband for Third Contingent.",
     "1901-08-01", "Third Contingent",
     []),
    ("27th Battalion Imperial Yeomanry",
     "Various; Third Contingent 1901.",
     "1901-09-01", "Third Contingent",
     []),
    ("28th Battalion Imperial Yeomanry (Westminster Dragoons)",
     "Westminster Dragoons; raised from London area for Third Contingent.",
     "1901-09-01", "Third Contingent",
     []),
    ("29th Battalion Imperial Yeomanry (Irish Horse)",
     "North and South Irish Horse; perpetuating the Irish companies of earlier contingents.",
     "1901-10-01", "Third Contingent",
     []),
    ("30th Battalion Imperial Yeomanry",
     "Various; Third Contingent.",
     "1901-10-01", "Third Contingent",
     []),
    ("31st Battalion Imperial Yeomanry (Fincastle's Horse)",
     "Fincastle's Horse; raised by Viscount Fincastle VC for Third Contingent.",
     "1901-10-01", "Third Contingent",
     []),
    ("32nd Battalion Imperial Yeomanry",
     "Various; Third Contingent.",
     "1901-11-01", "Third Contingent",
     []),
    ("33rd Battalion Imperial Yeomanry",
     "Various; Third Contingent.",
     "1901-11-01", "Third Contingent",
     []),
    ("34th Battalion Imperial Yeomanry",
     "Various; Third Contingent.",
     "1901-11-01", "Third Contingent",
     []),
    ("35th Battalion Imperial Yeomanry",
     "Various; Third Contingent.",
     "1901-12-01", "Third Contingent",
     []),
    ("36th Battalion Imperial Yeomanry",
     "Various; Third Contingent.",
     "1901-12-01", "Third Contingent",
     []),
    ("37th Battalion Imperial Yeomanry (Highland Horse)",
     "Highland Horse; raised from Scottish Highland counties for Third Contingent.",
     "1902-01-01", "Third Contingent",
     []),
    ("38th Battalion Imperial Yeomanry",
     "Various; Third Contingent.",
     "1902-01-01", "Third Contingent",
     []),
    ("39th Battalion Imperial Yeomanry",
     "Various; Third Contingent, arrived late in the war.",
     "1902-02-01", "Third Contingent",
     []),
]

# Contingent arrival/departure info
CONTINGENT_DEPART = {
    "First Contingent": "1901-06-01",   # most repatriated mid-1901
    "Second Contingent": "1902-06-01",
    "Third Contingent": "1902-07-01",
}

for force, desc, arrive, contingent, special in BATTALIONS:
    if force in by_force:
        print("SKIP (exists):", force)
        continue

    # 1. Arrival at Cape Town
    add(force, arrive, "disembark", "Cape Town",
        "%s arrived at Cape Town, %s. %s Strength ~400–500; deployed to the front for Roberts's advance or column operations." % (
            force, arrive, contingent),
        commander="")

    # 2. Roberts's advance / main campaign (first/second) or column ops (third)
    if contingent == "First Contingent":
        add(force, "1900-04-15", "redeployment", "Bloemfontein",
            "%s deployed as part of Roberts's main advance into the Orange Free State. IY battalions provided mounted infantry capability for the advance to Pretoria. Component companies: %s" % (force, desc),
            from_place="Cape Town")
        add(force, "1900-06-05", "redeployment", "Pretoria",
            "%s continued north with Roberts's main army, arriving Pretoria area June 1900. Dispersed to column duties across OFS and Transvaal for the guerrilla phase." % force,
            from_place="Bloemfontein")
    elif contingent == "Second Contingent":
        add(force, "1901-05-01", "redeployment", "Bloemfontein",
            "%s deployed into the OFS as part of the Second IY Contingent, reinforcing column operations during the guerrilla phase. Component description: %s" % (force, desc),
            from_place="Cape Town")
    else:  # Third
        add(force, "1901-10-01", "redeployment", "Pretoria",
            "%s deployed as part of the Third IY Contingent, arriving as the blockhouse line system was being established. Component description: %s" % (force, desc),
            from_place="Cape Town")

    # 3. Any special engagements
    for date, et, place, edesc, fp in special:
        add(force, date, et, place, edesc, from_place=fp)

    # 4. Stand-down / departure
    add(force, CONTINGENT_DEPART[contingent], "redeployment", "Cape Town",
        "%s repatriated to Britain following end of tour or conclusion of the war, %s." % (force, CONTINGENT_DEPART[contingent]),
        from_place="Pretoria" if contingent == "First Contingent" else "Bloemfontein")

print("\nNew rows: %d  (IDs %s-%s)" % (len(new_rows), max_id + 1, nid[0] - 1))
all_rows = rows + new_rows
with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(all_rows)
print("CSV written: %d total rows, %d forces" % (
    len(all_rows), len(set(r["force"] for r in all_rows))))

bp = open(BUILD_MAP, encoding="utf-8").read()
last_id = str(max_id)
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
    new_bp = before + '\n'.join(a_entries) + '\n}' + after
    open(BUILD_MAP, "w", encoding="utf-8").write(new_bp)
    print("A dict entries injected: %d" % len(a_entries))
else:
    print("ERROR: no injection point found")
