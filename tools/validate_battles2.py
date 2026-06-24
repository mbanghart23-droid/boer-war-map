"""
Strict battle audit: exact name match + curated aliases only.
Separates truly missing units from late-arrival (in CSV but first event after battle).
"""
import csv, datetime, re
from pathlib import Path
from collections import defaultdict

CSV_PATH = Path(__file__).parent.parent / "data" / "movements.csv"
rows = list(csv.DictReader(open(CSV_PATH, encoding="utf-8")))

by_force = defaultdict(list)
for r in rows: by_force[r["force"]].append(r)

def pd(s):
    try: return datetime.date.fromisoformat(s)
    except: return None

def earliest(force_name):
    dates = [pd(r["date_start"]) for r in by_force.get(force_name,[]) if pd(r["date_start"])]
    return min(dates) if dates else None

def has_before(force_name, cutoff):
    return any(pd(r["date_start"]) and pd(r["date_start"]) <= cutoff
               for r in by_force.get(force_name, []))

# Curated alias map: canonical name -> name as stored in CSV
ALIAS = {
    "2nd Black Watch":                          "2nd Bn Black Watch",
    "2nd Northumberland Fusiliers":             "2nd Northumberland Fusiliers",
    "1st Northumberland Fusiliers":             "1st Northumberland Fusiliers",
    "2nd Royal Irish Rifles":                   "2nd Royal Irish Rifles",
    "1st Loyal North Lancashire Regiment":      "1st Loyal North Lancashire Regiment",
    "2nd Lancashire Fusiliers":                 "2nd Lancashire Fusiliers",
    "1st Argyll & Sutherland Highlanders":      "1st Argyll & Sutherland Highlanders",
    "1st Highland Light Infantry":              "1st Bn Highland Light Infantry",
    "1st Gordon Highlanders":                   "1st Bn Gordon Highlanders",
    "2nd Seaforth Highlanders":                 "2nd Bn Seaforth Highlanders",
    "2nd Northamptonshire Regiment":            "2nd Northamptonshire Regiment",
    "2nd KOYLI":                                "2nd Bn KOYLI (Yorkshire Light Infantry)",
    "1st Manchester Regiment":                  "1st Manchester Regiment",
    "12th (Prince of Wales's Royal) Lancers":  "12th Prince of Wales's Royal Lancers (2nd)",
    "9th (Queen's Royal) Lancers":             "9th Queen's Royal Lancers",
    "Rimington's Guides":                       "Rimington's Guides",
    "G Battery Royal Horse Artillery":          "G Battery Royal Horse Artillery",
    "18th Battery Royal Field Artillery":       "18th Battery Royal Field Artillery",
    "62nd Battery Royal Field Artillery":       "62nd Battery Royal Field Artillery",
    "65th Howitzer Battery Royal Field Artillery": "65th Howitzer Battery Royal Field Artillery",
    "3rd Grenadier Guards":                     "3rd Grenadier Guards",
    "1st Coldstream Guards":                    "1st Coldstream Guards",
    "2nd Coldstream Guards":                    "2nd Coldstream Guards",
    "1st Scots Guards":                         "1st Scots Guards",
    "2nd Bn West Surrey Regiment (Queen's)":    "2nd Bn West Surrey Regiment (Queen's)",
    "2nd Bn West Yorkshire Regiment":           "2nd Bn West Yorkshire Regiment",
    "2nd Bn Devonshire Regiment":               "2nd Bn Devonshire Regiment",
    "2nd Bn East Surrey Regiment":              "2nd Bn East Surrey Regiment",
    "2nd Bn Scottish Rifles":                   "2nd Bn Scottish Rifles",
    "3rd Bn King's Royal Rifle Corps":          "3rd Bn King's Royal Rifle Corps",
    "1st Bn Durham Light Infantry":             "1st Bn Durham Light Infantry",
    "1st Bn Rifle Brigade":                     "1st Bn Rifle Brigade",
    "1st Royal Dublin Fusiliers":               "1st Royal Dublin Fusiliers",
    "1st Inniskilling Fusiliers":               "1st Inniskilling Fusiliers",
    "1st Connaught Rangers":                    "1st Connaught Rangers",
    "1st Border Regiment":                      "1st Border Regiment",
    "2nd Royal Fusiliers":                      "2nd Royal Fusiliers",
    "2nd Royal Scots Fusiliers":                "2nd Royal Scots Fusiliers",
    "1st Royal Welch Fusiliers":                "1st Royal Welch Fusiliers",
    "2nd Royal Irish Fusiliers":                "2nd Royal Irish Fusiliers",
    "1st (Royal) Dragoons":                     "1st (Royal) Dragoons",
    "6th (Carabiniers) Dragoon Guards":         "6th (Carabiniers) Dragoon Guards",
    "13th Hussars":                             "13th Hussars",
    "Thorneycroft's Mounted Infantry":          "Thorneycroft's Mounted Infantry",
    "Natal Carabineers":                        "Natal Carabineers",
    "Imperial Light Horse":                     "Imperial Light Horse",
    "South African Light Horse":                "South African Light Horse",
    "Bethune's Mounted Infantry":               "Bethune's Mounted Infantry",
    "14th Battery Royal Field Artillery":       "14th Battery Royal Field Artillery",
    "66th Battery Royal Field Artillery":       "66th Battery Royal Field Artillery",
    "73rd Battery Royal Field Artillery":       "73rd Battery Royal Field Artillery",
    "2nd Bn Lancaster Regiment":                "2nd Bn Lancaster Regiment",
    "2nd Dorset Regiment":                      "2nd Dorset Regiment",
    "2nd Middlesex Regiment":                   "2nd Middlesex Regiment",
    "63rd Battery Royal Field Artillery":       "63rd Battery Royal Field Artillery",
    "Carolina Commando":                        "Carolina Commando",
    "Pretoria Commando":                        "Pretoria Commando",
    "Heilbron Commando":                        "Heilbron Commando",
    "Vrede Commando":                           "Vrede Commando",
    "2nd Bn Bedfordshire Regiment":             "2nd Bn Bedfordshire Regiment",
    "1st Bn Royal Irish Regiment":              "1st Bn Royal Irish Regiment",
    "2nd Bn Worcester Regiment":                "2nd Bn Worcester Regiment",
    "2nd Bn Wiltshire Regiment":                "2nd Bn Wiltshire Regiment",
    "2nd Bn East Kent Regiment":                "2nd Bn East Kent Regiment",
    "2nd Bn Gloucester Regiment":               "2nd Bn Gloucester Regiment",
    "1st Bn West Riding Regiment":              "1st Bn West Riding Regiment",
    "1st Bn Oxfordshire Light Infantry":        "1st Bn Oxfordshire Light Infantry",
    "2nd Royal Warwickshire Regiment":          "2nd Royal Warwickshire Regiment",
    "1st Yorkshire Regiment":                   "1st Yorkshire Regiment",
    "1st Welsh Regiment":                       "1st Welsh Regiment",
    "1st Essex Regiment":                       "1st Essex Regiment",
    "Royal Canadian Regiment":                  "Royal Canadian Regiment",
    "New Zealand Mounted Rifles":               "New Zealand Mounted Rifles",
    "Q Battery Royal Horse Artillery":          "Q Battery Royal Horse Artillery",
    "U Battery Royal Horse Artillery":          "U Battery Royal Horse Artillery",
    "10th (Prince of Wales's Own Royal) Hussars": "10th (Prince of Wales's Own Royal) Hussars",
    "Royal Irish Regiment":                     "Royal Irish Regiment",
    "De Wet's Commando":                        "De Wet's Commando",
    "City Imperial Volunteers":                 "City Imperial Volunteers",
    "Sussex Regiment":                          "Sussex Regiment",
    "2nd Battalion Gordon Highlanders":         "2nd Battalion Gordon Highlanders",
    "2nd Rifle Brigade":                        "2nd Rifle Brigade",
    "1st Bn Liverpool Regiment":                "1st Bn Liverpool Regiment",
    "1st Bn Leicester Regiment":                "1st Bn Leicester Regiment",
    "1st Royal Inniskilling Fusiliers":         "1st Royal Inniskilling Fusiliers",
    "1st Bn Devonshire Regiment":               "1st Bn Devonshire Regiment",
    "Lydenburg Commando":                       "Lydenburg Commando",
    "Johannesburg Commando":                    "Johannesburg Commando",
    "Krugersdorp Commando":                     "Krugersdorp Commando",
    "Bethal Commando":                          "Bethal Commando",
    "Heidelberg Commando":                      "Heidelberg Commando",
    "De la Rey's Commando":                     "De la Rey's Commando",
    "Beyers's Commando":                        "Beyers's Commando",
    "Ashburner's Light Horse":                  "Ashburner's Light Horse",
    "Diamond Fields Horse":                     "Diamond Fields Horse",
    "Cape Police":                              "Cape Police",
    "Rustenburg Commando":                      "Rustenburg Commando",
    "Queenstown Rifle Volunteers":              "Queenstown Rifle Volunteers",
    "74th Battery Royal Field Artillery":       "74th Battery Royal Field Artillery",
    "77th Battery Royal Field Artillery":       "77th Battery Royal Field Artillery",
    "Frontier Mounted Rifles":                  "Frontier Mounted Rifles",
    "Rouxville Commando":                       "Rouxville Commando",
    "Bethulie Commando":                        "Bethulie Commando",
    "Fauresmith Commando":                      "Fauresmith Commando",
    "Ladybrand Commando":                       "Ladybrand Commando",
    "Hoopstad Commando":                        "Hoopstad Commando",
    "Kroonstad Commando":                       "Kroonstad Commando",
    "Bloemhof Commando":                        "Bloemhof Commando",
    "Boshof Commando":                          "Boshof Commando",
    "Wolmaransstad Commando":                   "Wolmaransstad Commando",
    "Lichtenburg Commando":                     "Lichtenburg Commando",
    "Middelburg Commando":                      "Middelburg Commando",
    "Ermelo Commando":                          "Ermelo Commando",
    "Standerton Commando":                      "Standerton Commando",
    "Vryheid Commando":                         "Vryheid Commando",
    "Wakkerstroom Commando":                    "Wakkerstroom Commando",
    "Heidelberg Commando":                      "Heidelberg Commando",
    "1st Argyll & Sutherland Highlanders":      "1st Argyll & Sutherland Highlanders",
    "2nd Seaforth Highlanders":                 "2nd Bn Seaforth Highlanders",
    "1st Highland Light Infantry":              "1st Bn Highland Light Infantry",
    "2nd Seaforth Highlanders":                 "2nd Bn Seaforth Highlanders",
}

BATTLES = [
("Stormberg", "1899-12-10", [
    "2nd Northumberland Fusiliers","2nd Royal Irish Rifles",
    "74th Battery Royal Field Artillery","77th Battery Royal Field Artillery",
    "Frontier Mounted Rifles","Queenstown Rifle Volunteers",
    "Rouxville Commando","Bethulie Commando",
]),
("Magersfontein", "1899-12-11", [
    "2nd Black Watch","2nd Seaforth Highlanders","1st Argyll & Sutherland Highlanders",
    "1st Highland Light Infantry","1st Gordon Highlanders",
    "3rd Grenadier Guards","1st Coldstream Guards","2nd Coldstream Guards","1st Scots Guards",
    "1st Northumberland Fusiliers","2nd Northamptonshire Regiment",
    "1st Loyal North Lancashire Regiment","2nd KOYLI","1st Manchester Regiment",
    "9th (Queen's Royal) Lancers","12th (Prince of Wales's Royal) Lancers","Rimington's Guides",
    "G Battery Royal Horse Artillery","18th Battery Royal Field Artillery",
    "62nd Battery Royal Field Artillery","65th Howitzer Battery Royal Field Artillery",
    "Fauresmith Commando","Ladybrand Commando","Hoopstad Commando","Kroonstad Commando",
    "Bloemhof Commando","Boshof Commando","Wolmaransstad Commando","Lichtenburg Commando",
]),
("Colenso", "1899-12-15", [
    "2nd Bn West Surrey Regiment (Queen's)","2nd Bn West Yorkshire Regiment",
    "2nd Bn Devonshire Regiment","2nd Bn East Surrey Regiment",
    "2nd Bn Scottish Rifles","3rd Bn King's Royal Rifle Corps",
    "1st Bn Durham Light Infantry","1st Bn Rifle Brigade",
    "1st Royal Dublin Fusiliers","1st Inniskilling Fusiliers",
    "1st Connaught Rangers","1st Border Regiment",
    "2nd Royal Fusiliers","2nd Royal Scots Fusiliers",
    "1st Royal Welch Fusiliers","2nd Royal Irish Fusiliers",
    "1st (Royal) Dragoons","6th (Carabiniers) Dragoon Guards","13th Hussars",
    "Thorneycroft's Mounted Infantry","Natal Carabineers","Imperial Light Horse",
    "South African Light Horse","Bethune's Mounted Infantry",
    "14th Battery Royal Field Artillery","66th Battery Royal Field Artillery",
    "73rd Battery Royal Field Artillery",
    "Middelburg Commando","Johannesburg Commando","Ermelo Commando",
    "Krugersdorp Commando","Standerton Commando","Vryheid Commando",
    "Wakkerstroom Commando","Heidelberg Commando",
]),
("Spion Kop", "1900-01-24", [
    "2nd Bn Lancaster Regiment","2nd Lancashire Fusiliers","2nd Dorset Regiment",
    "2nd Middlesex Regiment","Thorneycroft's Mounted Infantry","South African Light Horse",
    "Imperial Light Horse","Natal Carabineers","63rd Battery Royal Field Artillery",
    "Carolina Commando","Pretoria Commando","Heilbron Commando","Vrede Commando",
]),
("Paardeberg", "1900-02-18", [
    "2nd Black Watch","2nd Bn Bedfordshire Regiment","1st Bn Royal Irish Regiment",
    "2nd Bn Worcester Regiment","2nd Bn Wiltshire Regiment","2nd Bn East Kent Regiment",
    "2nd Bn Gloucester Regiment","1st Bn West Riding Regiment","1st Bn Oxfordshire Light Infantry",
    "1st Argyll & Sutherland Highlanders","1st Highland Light Infantry","2nd Seaforth Highlanders",
    "2nd Royal Warwickshire Regiment","1st Yorkshire Regiment","1st Welsh Regiment","1st Essex Regiment",
    "Royal Canadian Regiment","New Zealand Mounted Rifles",
]),
("Sanna's Post", "1900-03-31", [
    "Q Battery Royal Horse Artillery","U Battery Royal Horse Artillery",
    "10th (Prince of Wales's Own Royal) Hussars","Royal Irish Regiment",
    "Rimington's Guides","De Wet's Commando",
]),
("Diamond Hill", "1900-06-11", [
    "10th (Prince of Wales's Own Royal) Hussars","12th (Prince of Wales's Royal) Lancers",
    "City Imperial Volunteers","2nd Coldstream Guards","Sussex Regiment",
]),
("Bergendal", "1900-08-27", [
    "1st Manchester Regiment","2nd Battalion Gordon Highlanders","2nd Rifle Brigade",
    "1st Bn Liverpool Regiment","1st Bn Leicester Regiment",
    "1st Royal Inniskilling Fusiliers","1st Bn Devonshire Regiment",
    "Lydenburg Commando","Johannesburg Commando","Krugersdorp Commando",
    "Carolina Commando","Heidelberg Commando","Bethal Commando",
]),
("Nooitgedacht", "1900-12-13", [
    "2nd Northumberland Fusiliers","1st Border Regiment",
    "De la Rey's Commando","Beyers's Commando",
]),
("Tweebosch", "1902-03-07", [
    "Ashburner's Light Horse","Diamond Fields Horse","Cape Police",
    "Rustenburg Commando","Krugersdorp Commando",
]),
]

out = open(Path(__file__).parent / "battle_audit2.txt", "w", encoding="utf-8")
def p(s): print(s); out.write(s+"\n")

p("=" * 70)
p("BATTLE AUDIT v2 — strict name matching + curated aliases")
p("=" * 70)

all_missing = []
all_late = []

for battle, date_str, units in BATTLES:
    cutoff = datetime.date.fromisoformat(date_str)
    missing = []
    late = []
    ok = []
    for u in units:
        csv_name = ALIAS.get(u, u)
        if csv_name in by_force:
            e = earliest(csv_name)
            if has_before(csv_name, cutoff):
                ok.append(u)
            else:
                late.append((u, csv_name, e))
                all_late.append((battle, u, csv_name, e))
        else:
            missing.append(u)
            all_missing.append((battle, u))

    p("\n[%s — %s]" % (battle, date_str))
    p("  OK: %d" % len(ok))
    if late:
        p("  LATE (in CSV, first event AFTER battle):")
        for u, csv_name, e in late:
            nm = "" if u == csv_name else " (as '%s')" % csv_name
            p("    - %-50s%s  first: %s" % (u, nm, e))
    if missing:
        p("  MISSING FROM CSV ENTIRELY:")
        for u in missing:
            p("    - %s" % u)

p("\n" + "=" * 70)
p("ALL MISSING UNITS (need to add):")
seen = set()
for battle, u in all_missing:
    if u not in seen:
        p("  %-55s  [first at: %s]" % (u, battle))
        seen.add(u)

p("\nALL LATE UNITS (pre-battle event needed):")
seen2 = {}
for battle, u, csv_name, e in all_late:
    if u not in seen2:
        seen2[u] = (battle, csv_name, e)
for u, (battle, csv_name, e) in sorted(seen2.items(), key=lambda x: x[1][2] or datetime.date(1900,1,1)):
    p("  %-50s  first: %s  [battle: %s]" % (u, e, battle))

out.close()
print("\nReport: tools/battle_audit2.txt")
