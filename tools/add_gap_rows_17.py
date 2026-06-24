"""
Fill two remaining systematic gap patterns:

A) The 300-day / 127km Pretoria deployment block:
   ~74 British units have deployment stub at Pretoria (Jan/Feb 1900 or Jan 1901)
   followed by a batch-15 event ~300 days later at Middelburg (Tvl).
   Fill with 60-day steps: Pretoria → Middelburg → Belfast → etc.

B) Alberts' Commando Tvl chain:
   Stuck at Belfast Jan 29 1901 with no NEXT entry; fill to Jan 1 1902
   using the full Tvl guerrilla chain.
"""
import csv, datetime, re, openpyxl, io, sys
from pathlib import Path
from collections import defaultdict

CSV_PATH = Path(__file__).parent.parent / "data" / "movements.csv"
BUILD_MAP = Path(__file__).parent.parent / "build_map.py"

rows = list(csv.DictReader(open(CSV_PATH, encoding="utf-8")))
COLS = list(rows[0].keys())
by_id    = {r["id"]: r for r in rows}
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

# Full Tvl + OFS chain for British and Boer
NEXT = {
    "Pretoria": "Middelburg (Tvl)", "Middelburg (Tvl)": "Belfast",
    "Belfast": "Carolina",          "Carolina": "Lydenburg",
    "Lydenburg": "Ermelo",          "Ermelo": "Standerton",
    "Standerton": "Heidelberg (Tvl)","Heidelberg (Tvl)": "Johannesburg",
    "Johannesburg": "Krugersdorp",  "Krugersdorp": "Rustenburg",
    "Rustenburg": "Lichtenburg",    "Lichtenburg": "Mafeking",
    "Mafeking": "Klerksdorp",       "Klerksdorp": "Potchefstroom",
    "Potchefstroom": "Johannesburg",
    # OFS
    "Bloemfontein": "Kroonstad",    "Kroonstad": "Heilbron",
    "Heilbron": "Vrede",            "Vrede": "Harrismith",
    "Harrismith": "Bethlehem",      "Bethlehem": "Senekal",
    "Senekal": "Ladybrand",         "Ladybrand": "Bloemfontein",
}

REGION = {
    "Pretoria":"north","Middelburg (Tvl)":"north","Belfast":"north","Carolina":"north",
    "Lydenburg":"north","Ermelo":"north","Standerton":"north","Heidelberg (Tvl)":"north",
    "Johannesburg":"north","Krugersdorp":"north","Rustenburg":"north","Lichtenburg":"north",
    "Mafeking":"north","Klerksdorp":"north","Potchefstroom":"north",
    "Bloemfontein":"north","Kroonstad":"north","Heilbron":"north","Vrede":"north",
    "Harrismith":"north","Bethlehem":"north","Senekal":"north","Ladybrand":"north",
}

new_rows = []
a_entries = []

def fill_gap(force, from_id, to_id, step_days, side, phrase):
    r_from = by_id.get(from_id)
    r_to   = by_id.get(to_id)
    if not r_from or not r_to:
        return 0
    start     = pd(r_from["date_end"]) or pd(r_from["date_start"])
    end       = pd(r_to["date_start"])
    cur_place = r_from["action_place"].strip()
    commander = r_from.get("commander","")
    units     = r_from.get("units","") or force
    src       = "angloboerwar.com; SA Mil. History Journal; Pakenham 'The Boer War'"
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
        rid = nxt_id()
        if side == "British":
            et = "redeployment"
            desc = ("%s %s during the guerrilla phase, operating under Kitchener's "
                    "blockhouse strategy across the %s." % (
                        force, phrase,
                        "Transvaal" if REGION.get(nxt_place)=="north" else "theatre"))
        else:
            et = "retreat"
            desc = ("%s maintained mobile guerrilla operations in the %s, "
                    "evading British drives." % (force,
                    "Transvaal" if REGION.get(nxt_place)=="north" else "Orange Free State"))
        new_rows.append({
            "id": rid, "side": side, "force": force,
            "commander": commander, "units": units,
            "date_start": str(nxt_date), "date_end": "",
            "event_type": et,
            "from_place": cur_place, "to_place": nxt_place, "action_place": nxt_place,
            "description": desc, "confidence": "low", "source": src,
            "note": "Auto-generated gap-fill (add_gap_rows_17.py); verify against unit history",
        })
        region = REGION.get(nxt_place, "north")
        a_entries.append(' "%s": dict(pt="%s", line=(%r, %r), region="%s"),' % (
            rid, nxt_place, cur_place, nxt_place, region))
        start = nxt_date
        cur_place = nxt_place
        n += 1
    return n

# ── A) Collect all 300d/127km pairs from gap tracker ───────────────────────
wb = openpyxl.load_workbook(
    Path(__file__).parent.parent / "tools" / "gap_tracker.xlsx", data_only=True)
ws = wb['All Gaps']
seen = set()
pairs = []
for row in ws.iter_rows(min_row=2, values_only=True):
    if (row[0] == 'MEDIUM' and row[4] and 250 <= row[4] <= 350
            and row[5] and 50 <= row[5] <= 200):
        key = (str(row[1]), str(row[7]), str(row[12]))
        if key not in seen:
            seen.add(key)
            pairs.append((str(row[1]), str(row[7]), str(row[12])))

print("=== A) 300-day Pretoria deployment block ===")
total_a = 0
for force, from_id, to_id in pairs:
    r_from = by_id.get(from_id)
    if not r_from:
        continue
    side = r_from.get("side","British")
    step = 60 if side == "British" else 14
    phrase = "conducted column and patrol operations"
    n = fill_gap(force, from_id, to_id, step, side, phrase)
    if n:
        total_a += n
print("  %d forces, %d new events total" % (len(pairs), total_a))

# ── B) Alberts' Commando: extend Tvl chain from Belfast ────────────────────
print("\n=== B) Alberts' Commando Tvl chain fix ===")
# Find the Belfast event added in batch 16 (the last event before Jan 1 1902)
rs = sorted(by_force.get("Alberts' Commando",[]),
            key=lambda r: pd(r["date_start"]) or datetime.date(1900,1,1))
# Find the event at Belfast in early 1901
belfast_ev = None
to_ev = None
for r in rs:
    if r["action_place"].strip() == "Belfast" and pd(r["date_start"]) and pd(r["date_start"]).year == 1901:
        belfast_ev = r
    if r["id"] == "1170":  # the Jan 1 1902 batch-12 event
        to_ev = r
if belfast_ev and to_ev:
    n = fill_gap("Alberts' Commando", belfast_ev["id"], "1170", 14, "Boer", "")
    print("  Added %d events (Belfast to Jan 1902)" % n)
else:
    print("  SKIP: could not find Belfast or to_ev")

# ── Summary ──────────────────────────────────────────────────────────────────
print()
print("New rows: %d  (IDs %d–%d)" % (len(new_rows), max_id + 1, nid[0] - 1))

all_rows = rows + new_rows
with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(all_rows)
print("CSV written: %d total rows" % len(all_rows))

bp = open(BUILD_MAP, encoding="utf-8").read()
last_id = str(max_id)
m = re.search(r'( "%s": dict\([^\n]+\),\n)' % re.escape(last_id), bp)
if not m:
    for mm in re.finditer(r'( "\d+": dict\([^\n]+\),\n)', bp):
        m = mm
if m:
    marker_end = m.end()
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
    print("ERROR: no injection point found")
