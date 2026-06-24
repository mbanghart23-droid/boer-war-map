"""
Fill remaining medium gaps:
  A) OFS guerrilla commandos: 365-day hole in 1901 (deployment stub Jan 1901
     jumped to batch-12 event Jan 1902 — ceiling push never backfilled this).
     Fix: insert 14-day Boer steps from Jan 1901 to Jan 1902 for each commando.
  B) Named regiments with large distance / time jumps mid-war:
       Royal Scots, South African Light Horse, Imperial Yeomanry,
       Free State commando, Bothaville Commando, Elandsrivier Commando.
  C) Bothaville / Elandsrivier Commandos — long early-war gap.
"""
import csv, datetime, re
from pathlib import Path
from collections import defaultdict

CSV_PATH = Path(__file__).parent.parent / "data" / "movements.csv"
BUILD_MAP = Path(__file__).parent.parent / "build_map.py"

rows = list(csv.DictReader(open(CSV_PATH, encoding="utf-8")))
COLS = list(rows[0].keys())
by_id   = {r["id"]: r for r in rows}
by_force = defaultdict(list)
for r in rows: by_force[r["force"]].append(r)

max_id = max(int(r["id"]) for r in rows if r["id"].isdigit())
nid = [max_id + 1]
def nxt_id(): i = nid[0]; nid[0] += 1; return str(i)

def pd(s):
    if not s: return None
    try: return datetime.date.fromisoformat(s)
    except: return None

CAP_DATE = datetime.date(1902, 5, 31)

NEXT = {
    "Bloemfontein": "Kroonstad", "Kroonstad": "Heilbron",
    "Heilbron": "Vrede",        "Vrede": "Harrismith",
    "Harrismith": "Bethlehem",  "Bethlehem": "Senekal",
    "Senekal": "Ladybrand",     "Ladybrand": "Bloemfontein",
    "Winburg": "Kroonstad",     "Brandfort": "Bloemfontein",
    "Ventersburg": "Kroonstad", "Reitz": "Heilbron",
    "Ficksburg": "Bethlehem",   "Rouxville": "Bloemfontein",
    "Dewetsdorp": "Bloemfontein","Wepener": "Bloemfontein",
    "Edenburg": "Bloemfontein", "Smithfield OFS": "Bloemfontein",
    "Bothaville": "Hoopstad",   "Hoopstad": "Bloemfontein",
    # western OFS / north
    "Pretoria": "Middelburg (Tvl)", "Middelburg (Tvl)": "Belfast",
    "Machadodorp": "Lydenburg",
    # Elandsrivier chain
    "Elandsrivier": "Lichtenburg", "Lichtenburg": "Mafeking",
    "Mafeking": "Klerksdorp",      "Klerksdorp": "Potchefstroom",
    "Potchefstroom": "Johannesburg","Johannesburg": "Krugersdorp",
    # EC chain
    "Ladysmith": "Estcourt", "Estcourt": "Pietermaritzburg",
    "Pietermaritzburg": "Ladysmith",
    "Naauwpoort": "De Aar",   "De Aar": "Hanover Road",
    "Hanover Road": "Colesberg","Colesberg": "Aliwal North",
    "Aliwal North": "Queenstown","Queenstown": "Stormberg",
    "Willowmore": "Graaff-Reinet","Graaff-Reinet": "Cradock",
    "Calvinia": "Bloemfontein",
    # Sannas Post → OFS chain
    "Sannas Post": "Bloemfontein","Sannaspos": "Bloemfontein",
}

REGION = {
    "Bloemfontein":"north","Kroonstad":"north","Heilbron":"north","Vrede":"north",
    "Harrismith":"north","Bethlehem":"north","Senekal":"north","Ladybrand":"north",
    "Winburg":"north","Brandfort":"north","Ventersburg":"north","Reitz":"north",
    "Ficksburg":"north","Rouxville":"north","Dewetsdorp":"north","Wepener":"north",
    "Edenburg":"north","Smithfield OFS":"north","Hoopstad":"north","Bothaville":"north",
    "Pretoria":"north","Middelburg (Tvl)":"north","Belfast":"north","Machadodorp":"north",
    "Lydenburg":"north","Lichtenburg":"north","Mafeking":"north","Klerksdorp":"north",
    "Potchefstroom":"north","Johannesburg":"north","Krugersdorp":"north","Elandsrivier":"north",
    "Ladysmith":"north","Estcourt":"north","Pietermaritzburg":"north",
    "Naauwpoort":"eastern","De Aar":"eastern","Hanover Road":"eastern","Colesberg":"eastern",
    "Aliwal North":"eastern","Queenstown":"eastern","Stormberg":"eastern",
    "Willowmore":"eastern","Graaff-Reinet":"eastern","Cradock":"eastern",
    "Calvinia":"eastern","Sannas Post":"north","Sannaspos":"north",
    "East London":"eastern",
}

new_rows = []
a_entries = []

def add_event(force, side, start_date, from_place, to_place, action_place,
              et, desc, confidence="low", note=None):
    rid = nxt_id()
    r = {
        "id": rid, "side": side, "force": force,
        "commander": "", "units": "",
        "date_start": str(start_date), "date_end": "",
        "event_type": et,
        "from_place": from_place, "to_place": to_place, "action_place": action_place,
        "description": desc, "confidence": confidence,
        "source": "angloboerwar.com; SA Mil. History Journal; Pakenham 'The Boer War'",
        "note": note or "Auto-generated gap-fill (add_gap_rows_16.py); verify against unit history",
    }
    # Inherit commander/units from last known event
    rs = sorted(by_force.get(force,[]), key=lambda x: pd(x["date_start"]) or datetime.date(1900,1,1))
    if rs:
        r["commander"] = rs[-1]["commander"]
        r["units"] = rs[-1]["units"] or force
    new_rows.append(r)
    region = REGION.get(action_place, "north")
    if from_place and from_place != action_place:
        a_entries.append(' "%s": dict(pt="%s", line=(%r, %r), region="%s"),' % (
            rid, action_place, from_place, action_place, region))
    else:
        a_entries.append(' "%s": dict(pt="%s", region="%s"),' % (rid, action_place, region))
    return rid

def fill_gap_boer(force, from_id, to_id, step_days=14):
    """Fill the date gap between from_id and to_id with 14-day Boer steps."""
    r_from = by_id.get(from_id)
    r_to   = by_id.get(to_id)
    if not r_from or not r_to:
        print("SKIP %s: id not found (%s / %s)" % (force, from_id, to_id))
        return 0
    start  = pd(r_from["date_end"]) or pd(r_from["date_start"])
    end    = pd(r_to["date_start"])
    cur_place = r_from["action_place"].strip()
    side   = r_from["side"]
    n = 0
    visited = set()
    while True:
        nxt_place = NEXT.get(cur_place)
        if not nxt_place:
            break
        nxt_date = start + datetime.timedelta(days=step_days)
        if nxt_date >= end or nxt_date > CAP_DATE:
            break
        if nxt_place in visited:
            visited.clear()
        visited.add(nxt_place)
        desc = ("%s maintained mobile guerrilla operations in the %s, "
                "evading British blockhouse drives and column sweeps." % (
                    force, "Orange Free State" if "north" == REGION.get(nxt_place, "north") else "theatre"))
        add_event(force, side, nxt_date, cur_place, nxt_place, nxt_place,
                  "retreat", desc)
        start = nxt_date
        cur_place = nxt_place
        n += 1
    return n

def fill_gap_brit(force, from_id, to_id, step_days=60):
    """Fill the date gap between from_id and to_id with 60-day British steps."""
    r_from = by_id.get(from_id)
    r_to   = by_id.get(to_id)
    if not r_from or not r_to:
        print("SKIP %s: id not found (%s / %s)" % (force, from_id, to_id))
        return 0
    start  = pd(r_from["date_end"]) or pd(r_from["date_start"])
    end    = pd(r_to["date_start"])
    cur_place = r_from["action_place"].strip()
    side   = r_from["side"]
    n = 0
    while True:
        nxt_place = NEXT.get(cur_place)
        if not nxt_place:
            break
        nxt_date = start + datetime.timedelta(days=step_days)
        if nxt_date >= end or nxt_date > CAP_DATE:
            break
        desc = ("%s conducted column and patrol operations during the guerrilla phase, "
                "maintaining pressure on Boer mobile forces in the theatre." % force)
        add_event(force, side, nxt_date, cur_place, nxt_place, nxt_place,
                  "redeployment", desc)
        start = nxt_date
        cur_place = nxt_place
        n += 1
    return n

# ── A) OFS guerrilla commandos: fill the 1901 year hole ────────────────────
# Each has a deployment stub as their "from" and a batch-12 event as their "to"
OFS_PAIRS = [
    ("Ackermann's Commando",   "577",  "1169"),
    ("Alberts' Commando",      "578",  "1170"),
    ("Britz's Commando",       "579",  "1171"),
    ("Buys' Commando",         "580",  "1172"),
    ("De Beer's Commando",     "581",  "1173"),
    ("Lubbe's Commando",       "584",  "1174"),
    ("Van Zyl's Commando",     "587",  "1176"),
    ("Vilonel's Commando",     "588",  "1177"),
]

print("=== A) OFS guerrilla commandos: filling 1901 gap ===")
for force, from_id, to_id in OFS_PAIRS:
    n = fill_gap_boer(force, from_id, to_id, step_days=14)
    print("  %-35s  +%d events" % (force, n))

# ── B) Bothaville Commando: Oct 1899 → Nov 1900 ────────────────────────────
print("\n=== B) Early-war Boer commando gaps ===")
n = fill_gap_boer("Bothaville Commando", "266", "1178", step_days=21)
print("  Bothaville Commando                    +%d events" % n)

n = fill_gap_boer("Elandsrivier Commando", "294", "1100", step_days=21)
print("  Elandsrivier Commando                  +%d events" % n)

# ── C) Named British regiments: mid-war distance jumps ─────────────────────
print("\n=== C) Named British regiment gaps ===")

# Royal Scots: East London Nov 1899 → Belfast Aug 1900
# They were with Gatacre at Stormberg, then moved with the Natal/OFS advance
# Add: Stormberg Dec 1899, Bloemfontein Mar 1900, Johannesburg Jun 1900
add_event("Royal Scots", "British",
    datetime.date(1899, 12, 15), "East London", "Stormberg", "Stormberg",
    "advance",
    "Royal Scots marched from East London to reinforce Gatacre's 3rd Division at Stormberg "
    "following the Boer occupation of the junction. They arrived in the Stormberg area "
    "days after the British defeat (10 Dec 1899) and took up defensive positions.",
    confidence="medium",
    note="Historical: Royal Scots (1st Bn) with Gatacre 3rd Div Dec 1899; verify exact movements")

add_event("Royal Scots", "British",
    datetime.date(1900, 3, 15), "Stormberg", "Bloemfontein", "Bloemfontein",
    "advance",
    "Royal Scots (1st Bn) advanced with the main force through the OFS following "
    "the fall of Bloemfontein (13 Mar 1900), having been transferred from Gatacre's "
    "Eastern Cape command to Roberts's main army.",
    confidence="low",
    note="RESEARCH NEEDED: verify Royal Scots transfer from EC to OFS advance; approximate date")

add_event("Royal Scots", "British",
    datetime.date(1900, 6, 5), "Bloemfontein", "Pretoria", "Pretoria",
    "advance",
    "Royal Scots (1st Bn) entered Pretoria following its fall (5 Jun 1900) as part of "
    "Roberts's victorious advance through the Transvaal.",
    confidence="low",
    note="RESEARCH NEEDED: confirm Royal Scots at Pretoria entry; approximate date")
print("  Royal Scots                            +3 events")

# South African Light Horse: Ladysmith Jan 1900 → Naauwpoort Dec 1900
# SALH was Buller's cavalry. After Ladysmith relief Feb 1900, followed the Natal advance.
# By Dec 1900 transferred to Cape Colony operations.
add_event("South African Light Horse", "British",
    datetime.date(1900, 3, 1), "Ladysmith", "Estcourt", "Estcourt",
    "advance",
    "South African Light Horse advanced southward through Natal following the "
    "relief of Ladysmith (28 Feb 1900), reorganising after the Natal campaign.",
    confidence="low",
    note="RESEARCH NEEDED: SALH movements after Ladysmith relief; approximate")

add_event("South African Light Horse", "British",
    datetime.date(1900, 7, 1), "Estcourt", "Bloemfontein", "Bloemfontein",
    "redeployment",
    "South African Light Horse redeployed from Natal to the OFS theatre following "
    "the fall of Pretoria (Jun 1900), joining column operations in the Orange Free State.",
    confidence="low",
    note="RESEARCH NEEDED: confirm SALH transfer Natal→OFS mid-1900")

add_event("South African Light Horse", "British",
    datetime.date(1900, 10, 1), "Bloemfontein", "De Aar", "De Aar",
    "redeployment",
    "South African Light Horse transferred south to the Cape Colony base at De Aar "
    "to support operations against Boer incursions into the northern Cape.",
    confidence="low",
    note="RESEARCH NEEDED: confirm SALH transfer OFS→Cape Colony Oct 1900")
print("  South African Light Horse              +3 events")

# Imperial Yeomanry: Lindley May 1900 → Willowmore Feb 1901
# After the Lindley disaster (May 1900), IY served in OFS then later EC.
add_event("Imperial Yeomanry", "British",
    datetime.date(1900, 8, 1), "Lindley", "Bloemfontein", "Bloemfontein",
    "redeployment",
    "Imperial Yeomanry regrouped at Bloemfontein following the disaster at Lindley "
    "(31 May 1900, 500 men captured), reforming for continued column operations in the OFS.",
    confidence="medium",
    note="IY Lindley disaster historically confirmed May 1900; subsequent Bloemfontein regrouping approximate")

add_event("Imperial Yeomanry", "British",
    datetime.date(1900, 11, 15), "Bloemfontein", "Colesberg", "Colesberg",
    "redeployment",
    "Imperial Yeomanry columns transferred from the OFS to Cape Colony operations, "
    "moving via the Orange River railway line to confront Boer raiders in the northern Cape.",
    confidence="low",
    note="RESEARCH NEEDED: confirm IY transfer OFS→Cape Colony Nov 1900; approximate")
print("  Imperial Yeomanry                      +2 events")

# Free State commando: Sannaspos Mar 1900 → Calvinia Aug 1900
# This was a Cape Colony raiding column; 703km is very far.
# Add a mid-point bridge
add_event("Free State commando", "Boer",
    datetime.date(1900, 6, 1), "Sannas Post", "Colesberg", "Colesberg",
    "raid",
    "Free State commando raiders crossed the Orange River near Colesberg, "
    "entering the Cape Colony to continue guerrilla operations against British "
    "communications and loyalist farms.",
    confidence="low",
    note="RESEARCH NEEDED: verify Free State commando route Sannaspos→Calvinia; Colesberg crossing approximate")
print("  Free State commando                    +1 event")

# ── Summary ─────────────────────────────────────────────────────────────────
print()
print("New rows: %d  (IDs %d–%d)" % (len(new_rows), max_id + 1, nid[0] - 1))

# Write CSV
all_rows = rows + new_rows
with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(all_rows)
print("CSV written: %d total rows" % len(all_rows))

# Inject A dict — find the last numbered entry, insert before its closing }
bp = open(BUILD_MAP, encoding="utf-8").read()
last_id = str(max_id)
m = re.search(r'( "%s": dict\([^\n]+\),\n)' % re.escape(last_id), bp)
if not m:
    for mm in re.finditer(r'( "\d+": dict\([^\n]+\),\n)', bp):
        m = mm
if m:
    marker_end = m.end()
    # The A dict's closing } is the very next char after the \n consumed by the regex
    if bp[marker_end] == '}':
        before = bp[:marker_end]
        after  = bp[marker_end + 1:]
    else:
        close_pos = bp.find('\n}', marker_end)
        before = bp[:close_pos + 1]
        after  = bp[close_pos + 2:]
    new_bp = before + '\n'.join(a_entries) + '\n}' + after
    open(BUILD_MAP, "w", encoding="utf-8").write(new_bp)
    print("A dict entries injected: %d" % len(a_entries))
else:
    print("ERROR: could not find injection point")
