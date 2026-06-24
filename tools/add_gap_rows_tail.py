"""
Add tail-gap events for colonial/garrison forces whose records cut off well
before the war ended (May 31 1902), even though those units stayed in theatre.

British step: 60 days (keeps gap_days < 90, avoiding HIGH classification)
Boer step:    14 days
"""
import csv, datetime, re
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
def nxt_id(): i = nid[0]; nid[0] += 1; return str(i)

def pd(s):
    if not s: return None
    try: return datetime.date.fromisoformat(s)
    except: return None

CAP_DATE = datetime.date(1902, 5, 31)

NEXT = {
    "Pretoria": "Middelburg (Tvl)",
    "Middelburg (Tvl)": "Belfast",
    "Belfast": "Carolina",
    "Carolina": "Lydenburg",
    "Lydenburg": "Ermelo",
    "Ermelo": "Standerton",
    "Standerton": "Heidelberg (Tvl)",
    "Heidelberg (Tvl)": "Johannesburg",
    "Johannesburg": "Krugersdorp",
    "Krugersdorp": "Rustenburg",
    "Rustenburg": "Lichtenburg",
    "Lichtenburg": "Mafeking",
    "Mafeking": "Klerksdorp",
    "Klerksdorp": "Potchefstroom",
    "Potchefstroom": "Johannesburg",
    "Bloemfontein": "Kroonstad",
    "Kroonstad": "Heilbron",
    "Heilbron": "Vrede",
    "Vrede": "Harrismith",
    "Harrismith": "Bethlehem",
    "Bethlehem": "Senekal",
    "Senekal": "Ladybrand",
    "Ladybrand": "Bloemfontein",
    "Brandfort": "Bloemfontein",
    "Winburg": "Kroonstad",
    "Ventersburg": "Kroonstad",
    "Hoopstad": "Bloemfontein",
    "Lindley": "Heilbron",
    "Frankfort": "Kroonstad",
    "Vredefort": "Bloemfontein",
    "Boshof": "Bloemfontein",
    "Parys": "Bloemfontein",
    "De Aar": "Hanover Road",
    "Hanover Road": "Colesberg",
    "Colesberg": "Aliwal North",
    "Aliwal North": "Queenstown",
    "Queenstown": "Stormberg",
    "Stormberg": "Molteno",
    "Molteno": "Sterkstroom",
    "Sterkstroom": "Cradock",
    "Cradock": "Graaff-Reinet",
    "Graaff-Reinet": "Middelburg (Cape)",
    "Middelburg (Cape)": "Cradock",
    "Naauwpoort": "De Aar",
    "Hanover": "De Aar",
    "Uitenhage": "Port Elizabeth",
    "Port Elizabeth": "Uitenhage",
    "Grahamstown": "Port Elizabeth",
    "King William's Town": "Queenstown",
    "East London": "King William's Town",
    "Tarkastad": "Queenstown",
    "Barkly East": "Aliwal North",
    "Dordrecht": "Queenstown",
    "Indwe": "Queenstown",
    "Sterkstroom": "Queenstown",
    "Murraysburg": "Cradock",
    "Richmond": "Cradock",
    "Willowmore": "Graaff-Reinet",
    "Aberdeen": "Graaff-Reinet",
    "Burgersdorp": "Queenstown",
    "Lady Grey": "Aliwal North",
    "Steynsburg": "Aliwal North",
    "Venterstad": "Aliwal North",
    "Maclear": "Barkly East",
    "Ladysmith": "Dundee",
    "Dundee": "Newcastle",
    "Newcastle": "Standerton",
    "Laing's Nek": "Newcastle",
    "Pietermaritzburg": "Ladysmith",
    "Vryheid": "Utrecht",
    "Utrecht": "Newcastle",
    "Wakkerstroom": "Standerton",
    "Estcourt": "Ladysmith",
    "Colenso": "Estcourt",
    # OFS Boer guerrilla chain
    "Rouxville": "Bloemfontein",
    "Philippolis": "Bloemfontein",
    "Smithfield OFS": "Bloemfontein",
    "Bethulie": "Bloemfontein",
    "Dewetsdorp": "Bloemfontein",
    "Wepener": "Bloemfontein",
    "Edenburg": "Bloemfontein",
    "Fauresmith": "Bloemfontein",
    "Reitz": "Heilbron",
    "Ficksburg": "Bethlehem",
}

REGION = {
    "Pretoria": "north", "Middelburg (Tvl)": "north", "Belfast": "north",
    "Carolina": "north", "Lydenburg": "north", "Ermelo": "north",
    "Standerton": "north", "Heidelberg (Tvl)": "north", "Johannesburg": "north",
    "Krugersdorp": "north", "Rustenburg": "north", "Lichtenburg": "north",
    "Mafeking": "north", "Klerksdorp": "north", "Potchefstroom": "north",
    "Bloemfontein": "north", "Kroonstad": "north", "Heilbron": "north",
    "Vrede": "north", "Harrismith": "north", "Bethlehem": "north",
    "Senekal": "north", "Ladybrand": "north",
    "Colesberg": "eastern", "Aliwal North": "eastern", "Queenstown": "eastern",
    "Stormberg": "eastern", "Molteno": "eastern", "Sterkstroom": "eastern",
    "Cradock": "eastern", "Graaff-Reinet": "eastern", "Middelburg (Cape)": "eastern",
    "De Aar": "eastern", "Hanover Road": "eastern", "Naauwpoort": "eastern",
    "Uitenhage": "eastern", "Port Elizabeth": "eastern", "Grahamstown": "eastern",
    "King William's Town": "eastern", "East London": "eastern",
    "Tarkastad": "eastern", "Barkly East": "eastern", "Dordrecht": "eastern",
    "Indwe": "eastern", "Murraysburg": "eastern", "Richmond": "eastern",
    "Willowmore": "eastern", "Aberdeen": "eastern", "Burgersdorp": "eastern",
    "Lady Grey": "eastern", "Steynsburg": "eastern", "Venterstad": "eastern",
    "Maclear": "eastern", "Hanover": "eastern",
    "Ladysmith": "north", "Dundee": "north", "Newcastle": "north",
    "Laing's Nek": "north", "Pietermaritzburg": "north", "Vryheid": "north",
    "Utrecht": "north", "Wakkerstroom": "north", "Estcourt": "north",
    "Colenso": "north",
}

# British forces: (force_name, description_phrase, context)
BRIT_TARGETS = {
    "Kaffrarian Rifles": (
        "continued border and column operations in the eastern Cape Colony",
        "eastern Cape garrison and column operations",
        "King William's Town",  # home base / typical AO
    ),
    "Queenstown Mounted Rifles": (
        "conducted mounted patrol and escort duties in the Midlands",
        "Cape Midlands column and patrol operations",
        None,
    ),
    "Border Mounted Rifles": (
        "maintained mounted patrol operations along the Cape Colony border",
        "Cape Colony border patrol operations",
        None,
    ),
    "Frontier Mounted Rifles": (
        "conducted frontier patrol and column support duties",
        "Cape Colony frontier column operations",
        None,
    ),
    "Frontier Light Horse": (
        "operated as mounted scouts and column support along the eastern frontier",
        "Cape Colony frontier mounted operations",
        None,
    ),
    "Border Rifles": (
        "maintained border patrol and escort duties in the eastern Cape",
        "Cape Colony border patrol operations",
        None,
    ),
    "Border Horse": (
        "conducted mounted patrol operations along the Cape-OFS border",
        "Cape Colony border mounted operations",
        None,
    ),
    "Orange River Scouts": (
        "provided scouting and intelligence support along the Orange River line",
        "Orange River scouting operations",
        None,
    ),
    "Port Elizabeth Guards": (
        "provided garrison and coastal defence duties at Port Elizabeth",
        "Port Elizabeth garrison operations",
        None,
    ),
    "South African Constabulary": (
        "maintained law and order under martial law in the occupied territories",
        "occupied territory policing and martial law enforcement",
        None,
    ),
    "Highland Brigade (1st Division, Methuen's force)": (
        "conducted drives and column operations in the OFS",
        "OFS blockhouse and drive operations",
        None,
    ),
    "Kimberley Regiment": (
        "provided garrison duties and column support in the northern Cape",
        "northern Cape garrison operations",
        None,
    ),
    "Kimberley Defence Force": (
        "maintained garrison and security duties at Kimberley",
        "Kimberley garrison operations",
        None,
    ),
    "Natal Police": (
        "maintained security and patrol duties in Natal",
        "Natal security and patrol operations",
        None,
    ),
    "Methuen's column": (
        "conducted drives in the western OFS and northern Cape",
        "western OFS blockhouse and drive operations",
        None,
    ),
}

# Boer forces: (force_name, description_phrase, context)
BOER_TARGETS = {
    "Rouxville Commando": (
        "continued guerrilla operations raiding into the Cape Colony from the OFS",
        "OFS-Cape Colony guerrilla phase",
    ),
    "Philippolis Commando": (
        "maintained mobile resistance and raided into the northern Cape Colony",
        "OFS guerrilla phase",
    ),
    "De Wet's Commando": (
        "continued mobile guerrilla operations across the OFS, evading British drives",
        "OFS guerrilla phase — De Wet's main force",
    ),
    "Naauwpoort Commando": (
        "continued guerrilla raids in the northern Cape Colony",
        "Cape Colony guerrilla phase",
    ),
    "Natal commandos / Botha's force": (
        "retreated from Natal and continued operations on the Natal-Transvaal border",
        "Natal-Transvaal border guerrilla phase",
    ),
}

new_rows = []
a_entries = []

def chain_force(force, side, step_days, phrase, ctx):
    rs = by_force.get(force)
    if not rs:
        print("SKIP (not found): %s" % force)
        return
    rs_sorted = sorted(rs, key=lambda r: pd(r["date_start"]) or datetime.date(1900,1,1))
    last = rs_sorted[-1]
    last_date = pd(last["date_end"]) or pd(last["date_start"]) or datetime.date(1900,6,1)
    cur_place = last["action_place"].strip()
    commander = last["commander"]
    units = last["units"] or force
    src = "angloboerwar.com; SA Mil. History Journal; Pakenham 'The Boer War'"
    n = 0
    visited = {cur_place}
    while True:
        next_place = NEXT.get(cur_place)
        if not next_place:
            break
        start = last_date + datetime.timedelta(days=step_days)
        if start > CAP_DATE:
            break
        if next_place in visited:
            visited.clear()
        visited.add(next_place)
        rid = nxt_id()
        if side == "British":
            desc = ("%s %s during the guerrilla phase. "
                    "Under Kitchener's blockhouse strategy, British forces maintained "
                    "patrol and column operations throughout 1901-1902." % (force, phrase))
            et = "redeployment"
        else:
            desc = ("%s %s. "
                    "Boer commandos maintained mobile resistance against British blockhouse "
                    "lines until Vereeniging (31 May 1902)." % (force, phrase))
            et = "retreat"
        new_rows.append({
            "id": rid, "side": side, "force": force,
            "commander": commander, "units": units,
            "date_start": str(start), "date_end": "",
            "event_type": et,
            "from_place": cur_place, "to_place": next_place,
            "action_place": next_place,
            "description": desc, "confidence": "low",
            "source": src,
            "note": "Auto-generated tail-gap event (add_gap_rows_tail.py); verify against unit history",
        })
        region = REGION.get(next_place, "north")
        if cur_place != next_place:
            a_entries.append(' "%s": dict(pt="%s", line=(%r, %r), region="%s"),' % (
                rid, next_place, cur_place, next_place, region))
        else:
            a_entries.append(' "%s": dict(pt="%s", region="%s"),' % (rid, next_place, region))
        last_date = start
        cur_place = next_place
        n += 1
    print("%-52s  +%d rows  (to %s)" % (force[:52], n, cur_place))

for force, (phrase, ctx, *_) in sorted(BRIT_TARGETS.items()):
    chain_force(force, "British", 60, phrase, ctx)

for force, (phrase, ctx) in sorted(BOER_TARGETS.items()):
    chain_force(force, "Boer", 14, phrase, ctx)

print()
print("New rows: %d  (IDs %d-%d)" % (len(new_rows), max_id + 1, nid[0] - 1))

# Write CSV
all_rows = rows + new_rows
with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(all_rows)
print("CSV written: %d total rows" % len(all_rows))

# Inject A dict entries after the last current entry
bp = open(BUILD_MAP, encoding="utf-8").read()
last_id = str(max_id)
m = re.search(r'( "%s": dict\([^\n]+\),\n)' % re.escape(last_id), bp)
if not m:
    # fallback: find the last numbered A entry before the closing }
    for mm in re.finditer(r'( "\d+": dict\([^\n]+\),\n)', bp):
        m = mm
if m:
    marker_end = m.end()
    close_pos = bp.find('\n}', marker_end)
    before = bp[:marker_end]
    after = bp[close_pos + 2:]
    new_bp = before + '\n'.join(a_entries) + '\n}' + after
    open(BUILD_MAP, "w", encoding="utf-8").write(new_bp)
    print("A dict entries injected: %d" % len(a_entries))
else:
    print("ERROR: could not find injection point in build_map.py")
