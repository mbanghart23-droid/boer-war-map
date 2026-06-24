"""
Cross-reference known orders of battle against movements.csv.
For each major battle, check:
  1. Are the key units present in the CSV at all?
  2. Do they have an event ON OR BEFORE the battle date
     (i.e. do we have their arrival/formation in theatre)?
  3. Flag units only found as regiment sub-entries (units col) but missing as force.

Output: a report listing missing or coverage-gap units per battle.
"""
import csv, datetime, re
from pathlib import Path
from collections import defaultdict

CSV_PATH = Path(__file__).parent.parent / "data" / "movements.csv"

rows = list(csv.DictReader(open(CSV_PATH, encoding="utf-8")))
COLS = list(rows[0].keys())

by_force = defaultdict(list)
for r in rows: by_force[r["force"]].append(r)
all_forces = set(by_force.keys())

# also index units field (regimental sub-entries)
in_units = set()
for r in rows:
    if r.get("units"):
        for u in re.split(r"[;,]+", r["units"]):
            u = u.strip()
            if u: in_units.add(u)

def pd(s):
    try: return datetime.date.fromisoformat(s)
    except: return None

def earliest_event(force_name):
    rs = by_force.get(force_name, [])
    dates = [pd(r["date_start"]) for r in rs if pd(r["date_start"])]
    return min(dates) if dates else None

def has_event_before(force_name, cutoff):
    rs = by_force.get(force_name, [])
    return any(pd(r["date_start"]) and pd(r["date_start"]) <= cutoff for r in rs)

def find_close(name, all_forces):
    """Find forces whose name contains the key terms."""
    terms = [t.lower() for t in re.split(r"[\s/]+", name) if len(t) > 3]
    matches = []
    for f in all_forces:
        fl = f.lower()
        if sum(1 for t in terms if t in fl) >= max(1, len(terms) // 2):
            matches.append(f)
    return matches[:5]

# ── ORDERS OF BATTLE ──────────────────────────────────────────────────────────
# Format: (battle_name, date_str, [list of unit names to check])
BATTLES = [

("Stormberg", "1899-12-10", [
    "2nd Northumberland Fusiliers",
    "2nd Royal Irish Rifles",
    "74th Battery Royal Field Artillery",
    "77th Battery Royal Field Artillery",
    "Frontier Mounted Rifles",
    "Queenstown Rifle Volunteers",
    # Boer
    "Rouxville Commando",
    "Bethulie Commando",
]),

("Magersfontein", "1899-12-11", [
    # Highland Brigade
    "2nd Black Watch",
    "2nd Seaforth Highlanders",
    "1st Argyll & Sutherland Highlanders",
    "1st Highland Light Infantry",
    "1st Gordon Highlanders",
    # Guards Brigade
    "3rd Grenadier Guards",
    "1st Coldstream Guards",
    "2nd Coldstream Guards",
    "1st Scots Guards",
    # 9th Brigade
    "1st Northumberland Fusiliers",
    "2nd Northamptonshire Regiment",
    "1st Loyal North Lancashire Regiment",
    "2nd KOYLI",
    "1st Manchester Regiment",
    # Cavalry
    "9th (Queen's Royal) Lancers",
    "12th (Prince of Wales's Royal) Lancers",
    "Rimington's Guides",
    # Artillery
    "G Battery Royal Horse Artillery",
    "18th Battery Royal Field Artillery",
    "62nd Battery Royal Field Artillery",
    "65th Howitzer Battery Royal Field Artillery",
    # Boer
    "Fauresmith Commando",
    "Ladybrand Commando",
    "Hoopstad Commando",
    "Kroonstad Commando",
    "Bloemhof Commando",
    "Boshof Commando",
    "Wolmaransstad Commando",
    "Lichtenburg Commando",
]),

("Colenso", "1899-12-15", [
    # 2nd Brigade (Hildyard)
    "2nd Bn West Surrey Regiment (Queen's)",
    "2nd Bn West Yorkshire Regiment",
    "2nd Bn Devonshire Regiment",
    "2nd Bn East Surrey Regiment",
    # 4th Brigade (Lyttelton)
    "2nd Bn Scottish Rifles",
    "3rd Bn King's Royal Rifle Corps",
    "1st Bn Durham Light Infantry",
    "1st Bn Rifle Brigade",
    # 5th Brigade (Hart)
    "1st Royal Dublin Fusiliers",
    "1st Inniskilling Fusiliers",
    "1st Connaught Rangers",
    "1st Border Regiment",
    # 6th Brigade (Barton)
    "2nd Royal Fusiliers",
    "2nd Royal Scots Fusiliers",
    "1st Royal Welch Fusiliers",
    "2nd Royal Irish Fusiliers",
    # Cavalry (Dundonald)
    "1st (Royal) Dragoons",
    "6th (Carabiniers) Dragoon Guards",
    "13th Hussars",
    "Thorneycroft's Mounted Infantry",
    "Natal Carabineers",
    "Imperial Light Horse",
    "South African Light Horse",
    "Bethune's Mounted Infantry",
    # Artillery
    "14th Battery Royal Field Artillery",
    "66th Battery Royal Field Artillery",
    "73rd Battery Royal Field Artillery",
    # Boer
    "Middelburg Commando",
    "Johannesburg Commando",
    "Ermelo Commando",
    "Krugersdorp Commando",
    "Standerton Commando",
    "Vryheid Commando",
    "Wakkerstroom Commando",
    "Heidelberg Commando",
]),

("Spion Kop", "1900-01-24", [
    "2nd Bn Lancaster Regiment",
    "2nd Lancashire Fusiliers",
    "2nd Dorset Regiment",
    "2nd Middlesex Regiment",
    "Thorneycroft's Mounted Infantry",
    "South African Light Horse",
    "Imperial Light Horse",
    "Natal Carabineers",
    "63rd Battery Royal Field Artillery",
    # Boer
    "Carolina Commando",
    "Pretoria Commando",
    "Heilbron Commando",
    "Vrede Commando",
]),

("Paardeberg", "1900-02-18", [
    # 6th Division (Kelly-Kenny)
    "2nd Bn Bedfordshire Regiment",
    "1st Bn Royal Irish Regiment",
    "2nd Bn Worcester Regiment",
    "2nd Bn Wiltshire Regiment",
    "2nd Bn East Kent Regiment",
    "2nd Bn Gloucester Regiment",
    "1st Bn West Riding Regiment",
    "1st Bn Oxfordshire Light Infantry",
    # 9th Division (Colville)
    "2nd Black Watch",
    "1st Highland Light Infantry",
    "2nd Seaforth Highlanders",
    "1st Argyll & Sutherland Highlanders",
    "2nd Royal Warwickshire Regiment",
    "1st Yorkshire Regiment",
    "1st Welsh Regiment",
    "1st Essex Regiment",
    # Colonial
    "Royal Canadian Regiment",
    "New Zealand Mounted Rifles",
]),

("Sanna's Post", "1900-03-31", [
    "Q Battery Royal Horse Artillery",
    "U Battery Royal Horse Artillery",
    "10th (Prince of Wales's Own Royal) Hussars",
    "Royal Irish Regiment",
    "Rimington's Guides",
    # Boer
    "De Wet's Commando",
]),

("Diamond Hill", "1900-06-11", [
    "10th (Prince of Wales's Own Royal) Hussars",
    "12th (Prince of Wales's Royal) Lancers",
    "City Imperial Volunteers",
    "2nd Coldstream Guards",
    "Sussex Regiment",
]),

("Bergendal", "1900-08-27", [
    "1st Manchester Regiment",
    "2nd Battalion Gordon Highlanders",
    "2nd Rifle Brigade",
    "1st Bn Liverpool Regiment",
    "1st Bn Leicester Regiment",
    "1st Royal Inniskilling Fusiliers",
    "1st Bn Devonshire Regiment",
    # Boer
    "Lydenburg Commando",
    "Johannesburg Commando",
    "Krugersdorp Commando",
    "Carolina Commando",
    "Heidelberg Commando",
    "Bethal Commando",
]),

("Nooitgedacht", "1900-12-13", [
    "2nd Northumberland Fusiliers",
    "1st Border Regiment",
    # Boer
    "De la Rey's Commando",
    "Beyers's Commando",
]),

("Tweebosch", "1902-03-07", [
    "Ashburner's Light Horse",
    "Diamond Fields Horse",
    "Cape Police",
    # Boer
    "Rustenburg Commando",
    "Krugersdorp Commando",
]),
]

# ── RUN CHECKS ────────────────────────────────────────────────────────────────
report = []
for battle, date_str, units in BATTLES:
    cutoff = datetime.date.fromisoformat(date_str)
    missing_entirely = []
    late_arrival = []
    units_col_only = []
    ok = []

    for u in units:
        if u in by_force:
            if has_event_before(u, cutoff):
                ok.append(u)
            else:
                late_arrival.append((u, earliest_event(u)))
        else:
            # check units column
            close = find_close(u, all_forces)
            if close:
                # pick best match
                best = close[0]
                if has_event_before(best, cutoff):
                    ok.append("%s → %s" % (u, best))
                else:
                    late_arrival.append(("%s (matched: %s)" % (u, best), earliest_event(best)))
            elif u in in_units:
                units_col_only.append(u)
            else:
                missing_entirely.append(u)

    report.append((battle, date_str, missing_entirely, late_arrival, units_col_only, ok))

# ── OUTPUT ────────────────────────────────────────────────────────────────────
out = open(Path(__file__).parent / "battle_audit.txt", "w", encoding="utf-8")
def p(s): print(s); out.write(s+"\n")

p("=" * 70)
p("BATTLE UNIT AUDIT — movements.csv vs known orders of battle")
p("=" * 70)
total_missing = 0
total_late = 0
total_ok = 0

for battle, date_str, missing, late, ucol, ok in report:
    p("\n[%s — %s]" % (battle, date_str))
    p("  OK (in CSV with pre-battle event): %d" % len(ok))
    total_ok += len(ok)
    if late:
        p("  LATE / NO PRE-BATTLE EVENTS (%d):" % len(late))
        for u, earliest in late:
            p("    - %-52s  first event: %s" % (u, earliest or "NONE"))
        total_late += len(late)
    if missing:
        p("  MISSING FROM CSV ENTIRELY (%d):" % len(missing))
        for u in missing:
            p("    - %s" % u)
        total_missing += len(missing)
    if ucol:
        p("  IN units COLUMN ONLY (not a force) (%d):" % len(ucol))
        for u in ucol: p("    - %s" % u)

p("\n" + "=" * 70)
p("TOTALS: OK=%d  LATE=%d  MISSING=%d" % (total_ok, total_late, total_missing))
out.close()
print("\nFull report: tools/battle_audit.txt")
