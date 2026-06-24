"""
Add all units identified as missing from major battle orders of battle.
Groups:
  A: Stormberg forces (Eastern Cape)
  B: Magersfontein forces (Highland Brigade, Guards Brigade, 9th Brigade)
  C: Colenso / Natal forces (Hildyard, Lyttelton, Hart, Barton brigades)
  D: Spion Kop additional units
  E: Paardeberg additional infantry (6th/9th Divisions)
  F: Other missing (Royal Irish Regiment, Sussex, Rifle Brigade, De la Rey, Beyers, etc.)

Also prepend arrival events for 17 LATE units (in CSV but first event after battle).
"""
import csv, datetime, re
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
def nxt(): i = nid[0]; nid[0] += 1; return str(i)

def pd(s):
    try: return datetime.date.fromisoformat(s)
    except: return None

SRC_BRIT = "Pakenham 'The Boer War'; Conan Doyle 'The Great Boer War'; britishbattles.com; angloboerwar.com"
SRC_BOER = "Pakenham 'The Boer War'; De Wet 'Three Years War'; angloboerwar.com"
LOW = "low"
NOTE_AUTO = "Auto-generated from battle OOB (add_battle_units.py); verify against regimental history"

new_rows = []
a_entries = []

def ev(id, side, force, commander, units, date_start, date_end,
       event_type, from_place, to_place, action_place, description,
       confidence=LOW, source=SRC_BRIT, note=NOTE_AUTO, region="eastern"):
    new_rows.append({
        "id": id, "side": side, "force": force,
        "commander": commander or "", "units": units or force,
        "date_start": date_start, "date_end": date_end or "",
        "event_type": event_type,
        "from_place": from_place or "", "to_place": to_place or "",
        "action_place": action_place,
        "description": description,
        "confidence": confidence,
        "source": source, "note": note,
    })
    lp = to_place or action_place
    fp = from_place or ""
    if fp and fp != lp:
        a_entries.append(' "%s": dict(pt="%s", line=(%r, %r), region="%s"),' % (
            id, lp, fp, lp, region))
    else:
        a_entries.append(' "%s": dict(pt="%s", region="%s"),' % (id, lp, region))

def reg_ev(side, force, commander, units, date_start, date_end,
           event_type, from_place, to_place, action_place, description,
           confidence=LOW, source=SRC_BRIT, note=NOTE_AUTO, region="eastern"):
    i = nxt()
    ev(i, side, force, commander, units, date_start, date_end,
       event_type, from_place, to_place, action_place, description,
       confidence, source, note, region)
    return i

# shorthand
def brit(force, commander, date_start, event_type, from_place, to_place, action_place, desc,
         date_end="", units="", region="eastern", confidence=LOW):
    reg_ev("British", force, commander, units or force, date_start, date_end,
           event_type, from_place, to_place, action_place, desc,
           confidence=confidence, region=region)

def boer(force, commander, date_start, event_type, from_place, to_place, action_place, desc,
         date_end="", units="", region="north", confidence=LOW):
    reg_ev("Boer", force, commander, units or force, date_start, date_end,
           event_type, from_place, to_place, action_place, desc,
           confidence=confidence, source=SRC_BOER, region=region)

# ── A: STORMBERG FORCES ──────────────────────────────────────────────────────
# 2nd Northumberland Fusiliers
# Served in Gatacre's 3rd Division; captured en masse at Stormberg
brit("2nd Northumberland Fusiliers", "Lt Col Wilford",
     "1899-10-20", "disembark", "", "Cape Town", "Cape Town",
     "2nd Northumberland Fusiliers disembarked at Cape Town, assigned to Gatacre's 3rd Division for operations in the eastern Cape Colony.")
brit("2nd Northumberland Fusiliers", "Lt Col Wilford",
     "1899-11-15", "redeployment", "Cape Town", "Queenstown", "Queenstown",
     "2nd Northumberland Fusiliers deployed forward to Queenstown area to join Gatacre's column in the eastern Cape.")
brit("2nd Northumberland Fusiliers", "Lt Col Wilford",
     "1899-12-10", "engagement", "Queenstown", "Stormberg", "Stormberg",
     "2nd Northumberland Fusiliers engaged at the Battle of Stormberg. The unit suffered heavy losses; approximately 500 men were captured when Gatacre's column was ambushed by Boer forces under General Olivier.",
     confidence="high", region="eastern")
brit("2nd Northumberland Fusiliers", "",
     "1900-01-10", "redeployment", "Stormberg", "Queenstown", "Queenstown",
     "Survivors of the 2nd Northumberland Fusiliers reassembled at Queenstown following the Stormberg disaster and continued garrison operations in the eastern Cape.")
brit("2nd Northumberland Fusiliers", "",
     "1900-12-13", "engagement", "Pretoria", "Nooitgedacht", "Nooitgedacht",
     "2nd Northumberland Fusiliers engaged at Nooitgedacht (Yeomanry Hill) under Major-General Clements. The battalion was ambushed by De la Rey and Beyers and suffered significant casualties.",
     region="north", confidence="high")

# 2nd Royal Irish Rifles
brit("2nd Royal Irish Rifles", "Lt Col Eager",
     "1899-10-20", "disembark", "", "Cape Town", "Cape Town",
     "2nd Royal Irish Rifles (Royal Ulster Rifles) disembarked at Cape Town, assigned to Gatacre's 3rd Division.")
brit("2nd Royal Irish Rifles", "Lt Col Eager",
     "1899-11-15", "redeployment", "Cape Town", "Queenstown", "Queenstown",
     "2nd Royal Irish Rifles deployed to the Queenstown area as part of Gatacre's column, eastern Cape.")
brit("2nd Royal Irish Rifles", "Lt Col Eager",
     "1899-12-10", "engagement", "Queenstown", "Stormberg", "Stormberg",
     "2nd Royal Irish Rifles fought at the Battle of Stormberg. Together with the 2nd Northumberland Fusiliers they bore the brunt of the Boer ambush; around 600 men were captured.",
     confidence="high", region="eastern")
brit("2nd Royal Irish Rifles", "",
     "1900-01-10", "redeployment", "Stormberg", "Queenstown", "Queenstown",
     "Surviving companies of the 2nd Royal Irish Rifles reconstituted at Queenstown and continued eastern Cape operations under the reorganised 3rd Division.")

# 74th Battery RFA
brit("74th Battery Royal Field Artillery", "Major",
     "1899-11-01", "disembark", "", "Cape Town", "Cape Town",
     "74th Battery Royal Field Artillery arrived at Cape Town and joined Gatacre's column for eastern Cape operations.")
brit("74th Battery Royal Field Artillery", "",
     "1899-12-10", "engagement", "Cape Town", "Stormberg", "Stormberg",
     "74th Battery Royal Field Artillery provided artillery support at the Battle of Stormberg.",
     confidence="high", region="eastern")
brit("74th Battery Royal Field Artillery", "",
     "1900-06-01", "redeployment", "Stormberg", "Bloemfontein", "Bloemfontein",
     "74th Battery Royal Field Artillery redeployed north after the Cape Colony columns advanced into the Orange Free State.", region="north")

# Queenstown Rifle Volunteers
brit("Queenstown Rifle Volunteers", "",
     "1899-11-01", "garrison", "", "Queenstown", "Queenstown",
     "Queenstown Rifle Volunteers, a colonial unit formed from the Queenstown district, mobilised for garrison and column operations in the eastern Cape midlands.")
brit("Queenstown Rifle Volunteers", "",
     "1899-12-10", "engagement", "Queenstown", "Stormberg", "Stormberg",
     "Queenstown Rifle Volunteers attached to Gatacre's column at Stormberg.",
     confidence="high", region="eastern")
brit("Queenstown Rifle Volunteers", "",
     "1900-03-01", "garrison", "Stormberg", "Queenstown", "Queenstown",
     "Queenstown Rifle Volunteers returned to Queenstown and continued local defence and escort duties.")

# ── B: MAGERSFONTEIN FORCES ───────────────────────────────────────────────────
# Highland Brigade units (all arrived Cape Town Oct-Nov 1899, deployed Kimberley front)
HIGHLAND = [
    ("2nd Black Watch", "Lt Col Hughes-Hallett"),
    ("2nd Seaforth Highlanders", "Lt Col Mathias"),
    ("1st Argyll & Sutherland Highlanders", "Lt Col Goff"),
    ("1st Highland Light Infantry", "Lt Col Kelham"),
    ("1st Gordon Highlanders", "Lt Col Downman"),
]
for unit, co in HIGHLAND:
    brit(unit, co,
         "1899-10-20", "disembark", "", "Cape Town", "Cape Town",
         "%s disembarked at Cape Town and joined Methuen's 1st Division, Highland Brigade for the advance towards Kimberley." % unit,
         region="north")
    brit(unit, co,
         "1899-11-20", "redeployment", "Cape Town", "Orange River Station", "Orange River Station",
         "%s moved north to Orange River Station, staging point for Methuen's advance to relieve Kimberley." % unit,
         region="north")
    brit(unit, co,
         "1899-12-11", "engagement", "Orange River Station", "Magersfontein", "Magersfontein",
         "%s fought at the Battle of Magersfontein as part of the Highland Brigade under General Wauchope. The brigade suffered catastrophic losses in a night attack on the Boer trenches." % unit,
         confidence="high", region="north")
    brit(unit, "",
         "1900-02-15", "redeployment", "Magersfontein", "Kimberley", "Kimberley",
         "%s advanced to relieve Kimberley following Roberts's flanking movement via Paardeberg." % unit,
         region="north")
    brit(unit, "",
         "1900-03-01", "redeployment", "Kimberley", "Bloemfontein", "Bloemfontein",
         "%s continued the advance towards Bloemfontein with Methuen's division following relief of Kimberley." % unit,
         region="north")

# Guards Brigade
GUARDS = [
    ("3rd Grenadier Guards", "Lt Col Stopford"),
    ("1st Coldstream Guards", "Lt Col Codrington"),
    ("2nd Coldstream Guards", "Lt Col Crabbe"),
    ("1st Scots Guards", "Lt Col Downman"),
]
for unit, co in GUARDS:
    brit(unit, co,
         "1899-11-10", "disembark", "", "Cape Town", "Cape Town",
         "%s arrived at Cape Town and joined the Guards Brigade under Methuen's 1st Division." % unit,
         region="north")
    brit(unit, co,
         "1899-11-25", "engagement", "Cape Town", "Modder River", "Modder River",
         "%s engaged at the Battle of Modder River (28 Nov 1899) during Methuen's advance." % unit,
         region="north")
    brit(unit, co,
         "1899-12-11", "engagement", "Modder River", "Magersfontein", "Magersfontein",
         "%s fought at the Battle of Magersfontein (11 Dec 1899) under Methuen. The attack failed to dislodge Cronje's Boers from their prepared positions." % unit,
         confidence="high", region="north")
    brit(unit, "",
         "1900-02-15", "redeployment", "Magersfontein", "Kimberley", "Kimberley",
         "%s advanced to Kimberley after Roberts outflanked Cronje via Paardeberg." % unit,
         region="north")
    brit(unit, "",
         "1900-06-11", "engagement", "Kimberley", "Diamond Hill", "Diamond Hill",
         "%s engaged at Diamond Hill (11-12 Jun 1900) during Roberts's advance past Pretoria." % unit,
         confidence="high", region="north")

# 9th Brigade (Magersfontein)
NINTH_BDE = [
    ("1st Northumberland Fusiliers", "Lt Col Cholmeley"),
    ("2nd Northamptonshire Regiment", "Lt Col Stockley"),
    ("1st Loyal North Lancashire Regiment", "Lt Col Doughty"),
    ("1st Manchester Regiment", "Lt Col Curran"),
]
for unit, co in NINTH_BDE:
    brit(unit, co,
         "1899-10-20", "disembark", "", "Cape Town", "Cape Town",
         "%s arrived at Cape Town and joined the 9th Brigade under Methuen's 1st Division." % unit,
         region="north")
    brit(unit, co,
         "1899-11-23", "engagement", "Cape Town", "Belmont", "Belmont",
         "%s fought at the Battle of Belmont (23 Nov 1899) during Methuen's advance to relieve Kimberley." % unit,
         region="north")
    brit(unit, co,
         "1899-12-11", "engagement", "Belmont", "Magersfontein", "Magersfontein",
         "%s engaged at the Battle of Magersfontein (11 Dec 1899) as part of Methuen's force." % unit,
         confidence="high", region="north")
    brit(unit, "",
         "1900-02-15", "redeployment", "Magersfontein", "Kimberley", "Kimberley",
         "%s advanced to Kimberley following Roberts's successful outflanking move." % unit,
         region="north")
    brit(unit, "",
         "1900-08-27", "engagement", "Kimberley", "Bergendal", "Bergendal",
         "%s participated in operations around Bergendal during the advance into the eastern Transvaal." % unit,
         region="north")

# Rimington's Guides (colonial scouts, present throughout campaign)
brit("Rimington's Guides", "Major Rimington",
     "1899-11-01", "garrison", "", "Orange River Station", "Orange River Station",
     "Rimington's Guides (Tigers), a colonial scout corps raised in South Africa, deployed with Methuen's advance column as intelligence and reconnaissance.",
     region="north")
brit("Rimington's Guides", "Major Rimington",
     "1899-12-11", "engagement", "Orange River Station", "Magersfontein", "Magersfontein",
     "Rimington's Guides acted as flanking scouts at Magersfontein.",
     confidence="high", region="north")
brit("Rimington's Guides", "Major Rimington",
     "1900-03-31", "engagement", "Magersfontein", "Sanna's Post", "Sanna's Post",
     "Rimington's Guides present at the Battle of Sanna's Post (Koorn Spruit) as De Wet ambushed Broadwood's column.",
     confidence="high", region="north")

# Wolmaransstad Commando
boer("Wolmaransstad Commando", "",
     "1899-10-11", "engagement", "Wolmaransstad", "Kimberley", "Kimberley",
     "Wolmaransstad Commando mobilised and joined the siege of Kimberley as part of De la Rey's western Transvaal force.",
     confidence="high")
boer("Wolmaransstad Commando", "",
     "1899-12-11", "engagement", "Kimberley", "Magersfontein", "Magersfontein",
     "Wolmaransstad Commando fought at Magersfontein under De la Rey, defending the prepared trenches against Methuen's assault.",
     confidence="high")

# ── C: COLENSO / NATAL FORCES ────────────────────────────────────────────────
# Hildyard's 2nd Brigade
HILDYARD = [
    ("2nd Bn West Yorkshire Regiment", "Lt Col Goff"),
    ("2nd Bn Devonshire Regiment", "Lt Col Park"),
    ("2nd Bn East Surrey Regiment", "Lt Col Kitchener"),
]
for unit, co in HILDYARD:
    brit(unit, co,
         "1899-11-01", "disembark", "", "Durban", "Durban",
         "%s disembarked at Durban and joined Hildyard's 2nd Brigade for the Natal campaign." % unit,
         region="north")
    brit(unit, co,
         "1899-11-20", "redeployment", "Durban", "Estcourt", "Estcourt",
         "%s deployed forward to Estcourt as Buller's Natal Field Force concentrated to relieve Ladysmith." % unit,
         region="north")
    brit(unit, co,
         "1899-12-15", "engagement", "Estcourt", "Colenso", "Colenso",
         "%s fought in Hildyard's 2nd Brigade at the Battle of Colenso (15 Dec 1899) under Buller." % unit,
         confidence="high", region="north")
    brit(unit, "",
         "1900-01-24", "engagement", "Colenso", "Spion Kop", "Spion Kop",
         "%s participated in operations around Spion Kop (24 Jan 1900) in Buller's second attempt to relieve Ladysmith." % unit,
         region="north")
    brit(unit, "",
         "1900-02-28", "redeployment", "Spion Kop", "Ladysmith", "Ladysmith",
         "%s entered Ladysmith with Buller's force on 28 February 1900, ending the 118-day siege." % unit,
         region="north")

# Lyttelton's 4th Brigade
LYTTELTON = [
    ("3rd Bn King's Royal Rifle Corps", "Lt Col Buchanan-Riddell"),
    ("1st Bn Durham Light Infantry", "Lt Col Fitzgerald"),
    ("1st Bn Rifle Brigade", "Lt Col Buchanan"),
]
for unit, co in LYTTELTON:
    brit(unit, co,
         "1899-11-01", "disembark", "", "Durban", "Durban",
         "%s disembarked at Durban and joined Lyttelton's 4th Brigade, Natal Field Force." % unit,
         region="north")
    brit(unit, co,
         "1899-11-20", "redeployment", "Durban", "Frere", "Frere",
         "%s deployed to Frere camp as Buller's force assembled for the Colenso attack." % unit,
         region="north")
    brit(unit, co,
         "1899-12-15", "engagement", "Frere", "Colenso", "Colenso",
         "%s fought at the Battle of Colenso (15 Dec 1899) in Lyttelton's 4th Brigade." % unit,
         confidence="high", region="north")
    brit(unit, "",
         "1900-02-28", "redeployment", "Colenso", "Ladysmith", "Ladysmith",
         "%s reached Ladysmith with Buller's relieving force (28 Feb 1900)." % unit,
         region="north")

# Hart's 5th Irish Brigade
HART = [
    ("1st Royal Dublin Fusiliers", "Lt Col Sitwell"),
    ("1st Inniskilling Fusiliers", "Lt Col Payne"),
    ("1st Connaught Rangers", "Lt Col Brooke"),
    ("1st Border Regiment", "Lt Col Thorold"),
]
for unit, co in HART:
    brit(unit, co,
         "1899-11-01", "disembark", "", "Durban", "Durban",
         "%s disembarked at Durban and joined Hart's 5th (Irish) Brigade, Natal Field Force." % unit,
         region="north")
    brit(unit, co,
         "1899-11-20", "redeployment", "Durban", "Frere", "Frere",
         "%s moved forward to Frere as the Irish Brigade prepared for the assault on Colenso." % unit,
         region="north")
    brit(unit, co,
         "1899-12-15", "engagement", "Frere", "Colenso", "Colenso",
         "%s attacked through the Tugela drift at Colenso (15 Dec 1899). Hart's brigade suffered heavy losses in the frontal assault across the Tugela loop." % unit,
         confidence="high", region="north")
    brit(unit, "",
         "1900-02-28", "redeployment", "Colenso", "Ladysmith", "Ladysmith",
         "%s marched into Ladysmith with Buller's relief force (28 Feb 1900), ending the siege." % unit,
         region="north")
    brit(unit, "",
         "1900-12-13", "redeployment", "Ladysmith", "Nooitgedacht", "Nooitgedacht",
         "%s participated in Clements's column which was ambushed at Nooitgedacht (13 Dec 1900) by De la Rey." % unit,
         region="north")

# Barton's 6th Fusilier Brigade
BARTON = [
    ("2nd Royal Fusiliers", "Lt Col Davis"),
    ("2nd Royal Scots Fusiliers", "Lt Col Jones"),
    ("1st Royal Welch Fusiliers", "Lt Col Hicks"),
    ("2nd Royal Irish Fusiliers", "Lt Col Brooke"),
]
for unit, co in BARTON:
    brit(unit, co,
         "1899-11-01", "disembark", "", "Durban", "Durban",
         "%s disembarked at Durban and joined Barton's 6th (Fusilier) Brigade, Natal Field Force." % unit,
         region="north")
    brit(unit, co,
         "1899-11-20", "redeployment", "Durban", "Frere", "Frere",
         "%s deployed forward to Frere camp as part of Buller's concentration for Colenso." % unit,
         region="north")
    brit(unit, co,
         "1899-12-15", "engagement", "Frere", "Colenso", "Colenso",
         "%s fought in Barton's Fusilier Brigade at the Battle of Colenso." % unit,
         confidence="high", region="north")
    brit(unit, "",
         "1900-02-28", "redeployment", "Colenso", "Ladysmith", "Ladysmith",
         "%s entered Ladysmith with Buller on 28 February 1900." % unit,
         region="north")

# Natal Carabineers
brit("Natal Carabineers", "",
     "1899-10-11", "garrison", "", "Pietermaritzburg", "Pietermaritzburg",
     "Natal Carabineers, a colonial mounted corps, mobilised at the outbreak of war to defend Natal and support the field force.",
     confidence="high", region="north")
brit("Natal Carabineers", "",
     "1899-12-15", "engagement", "Pietermaritzburg", "Colenso", "Colenso",
     "Natal Carabineers attached to Dundonald's cavalry brigade at the Battle of Colenso.",
     confidence="high", region="north")
brit("Natal Carabineers", "",
     "1900-01-24", "engagement", "Colenso", "Spion Kop", "Spion Kop",
     "Natal Carabineers participated in the Spion Kop operations (24 Jan 1900).",
     region="north")
brit("Natal Carabineers", "",
     "1900-02-28", "redeployment", "Spion Kop", "Ladysmith", "Ladysmith",
     "Natal Carabineers entered Ladysmith with Buller's relief force.",
     region="north")

# ── D: SPION KOP ADDITIONAL UNITS ────────────────────────────────────────────
SPION_KOP = [
    ("2nd Bn Lancaster Regiment", "Lt Col Malby Crofton"),
    ("2nd Lancashire Fusiliers", "Lt Col Blomfield"),
    ("2nd Dorset Regiment", "Lt Col Hannay"),
    ("2nd Middlesex Regiment", "Lt Col Hill"),
]
for unit, co in SPION_KOP:
    brit(unit, co,
         "1899-11-15", "disembark", "", "Durban", "Durban",
         "%s arrived in Natal and joined Warren's 5th Division for the Spion Kop operations." % unit,
         region="north")
    brit(unit, co,
         "1900-01-24", "engagement", "Durban", "Spion Kop", "Spion Kop",
         "%s was heavily engaged at the Battle of Spion Kop (24 Jan 1900) in the assault on the summit." % unit,
         confidence="high", region="north")
    brit(unit, "",
         "1900-02-28", "redeployment", "Spion Kop", "Ladysmith", "Ladysmith",
         "%s advanced into Ladysmith with Buller's relieving force (28 Feb 1900)." % unit,
         region="north")
    brit(unit, "",
         "1900-05-01", "redeployment", "Ladysmith", "Newcastle", "Newcastle",
         "%s moved with Buller's column through Laing's Nek into the Transvaal." % unit,
         region="north")

# ── E: PAARDEBERG ADDITIONAL INFANTRY ────────────────────────────────────────
# 6th Division (Kelly-Kenny)
SIXTH_DIV = [
    ("2nd Bn Bedfordshire Regiment", "Lt Col Bullock"),
    ("1st Bn Royal Irish Regiment", "Lt Col Hughes"),
    ("2nd Bn Wiltshire Regiment", "Lt Col Shervinton"),
    ("2nd Bn East Kent Regiment", "Lt Col Ormerod"),
]
for unit, co in SIXTH_DIV:
    brit(unit, co,
         "1900-01-01", "disembark", "", "Cape Town", "Cape Town",
         "%s arrived at Cape Town with Roberts's reinforcements and joined the 6th Division (Kelly-Kenny) for the advance to Paardeberg." % unit,
         region="north")
    brit(unit, co,
         "1900-02-18", "engagement", "Cape Town", "Paardeberg", "Paardeberg",
         "%s fought at the Battle of Paardeberg (18-27 Feb 1900) surrounding Cronje's laager." % unit,
         confidence="high", region="north")
    brit(unit, "",
         "1900-03-13", "redeployment", "Paardeberg", "Bloemfontein", "Bloemfontein",
         "%s marched to Bloemfontein with Roberts's main force after Cronje's surrender at Paardeberg." % unit,
         region="north")

# 9th Division (Colville) — additional units
NINTH_DIV = [
    ("2nd Royal Warwickshire Regiment", "Lt Col Gordon"),
    ("1st Yorkshire Regiment", "Lt Col Hughes"),
    ("1st Welsh Regiment", "Lt Col Arnold"),
    ("1st Essex Regiment", "Lt Col Kenna"),
]
for unit, co in NINTH_DIV:
    brit(unit, co,
         "1900-01-01", "disembark", "", "Cape Town", "Cape Town",
         "%s arrived at Cape Town with Roberts's main force and joined the 9th Division (Colville) for the Paardeberg campaign." % unit,
         region="north")
    brit(unit, co,
         "1900-02-18", "engagement", "Cape Town", "Paardeberg", "Paardeberg",
         "%s engaged at Paardeberg (18-27 Feb 1900) as part of the 9th Division encircling Cronje's force." % unit,
         confidence="high", region="north")
    brit(unit, "",
         "1900-03-13", "redeployment", "Paardeberg", "Bloemfontein", "Bloemfontein",
         "%s advanced to Bloemfontein following Cronje's surrender." % unit,
         region="north")

# ── F: OTHER MISSING UNITS ───────────────────────────────────────────────────
# Royal Irish Regiment (at Sanna's Post)
brit("Royal Irish Regiment", "Lt Col",
     "1899-11-01", "disembark", "", "Cape Town", "Cape Town",
     "Royal Irish Regiment arrived in South Africa and joined Roberts's forces for the advance into the Orange Free State.",
     region="north")
brit("Royal Irish Regiment", "",
     "1900-02-01", "redeployment", "Cape Town", "Bloemfontein", "Bloemfontein",
     "Royal Irish Regiment advanced to Bloemfontein with Roberts's main column.",
     region="north")
brit("Royal Irish Regiment", "",
     "1900-03-31", "engagement", "Bloemfontein", "Sanna's Post", "Sanna's Post",
     "Royal Irish Regiment present at the Battle of Sanna's Post (31 Mar 1900) when De Wet ambushed Broadwood's column.",
     confidence="high", region="north")

# Sussex Regiment (at Diamond Hill)
brit("Sussex Regiment", "",
     "1900-02-01", "disembark", "", "Cape Town", "Cape Town",
     "Sussex Regiment (Royal Sussex) arrived in South Africa and served with Roberts's main force in the advance towards Pretoria.",
     region="north")
brit("Sussex Regiment", "",
     "1900-06-11", "engagement", "Cape Town", "Diamond Hill", "Diamond Hill",
     "Sussex Regiment fought at the Battle of Diamond Hill (11-12 Jun 1900) under Hamilton's right flank force.",
     confidence="high", region="north")

# 2nd Rifle Brigade (at Bergendal)
brit("2nd Rifle Brigade", "Lt Col",
     "1900-03-01", "disembark", "", "Cape Town", "Cape Town",
     "2nd Rifle Brigade arrived in South Africa and joined Buller's force in Natal for the advance into the Transvaal.",
     region="north")
brit("2nd Rifle Brigade", "",
     "1900-08-27", "engagement", "Cape Town", "Bergendal", "Bergendal",
     "2nd Rifle Brigade fought at the Battle of Bergendal (27 Aug 1900) under Kitchener's 7th Brigade, the last conventional battle of the war.",
     confidence="high", region="north")

# 1st Royal Inniskilling Fusiliers (at Bergendal)
brit("1st Royal Inniskilling Fusiliers", "Lt Col",
     "1900-01-01", "disembark", "", "Durban", "Durban",
     "1st Royal Inniskilling Fusiliers disembarked at Durban and joined Buller's Natal Field Force.",
     region="north")
brit("1st Royal Inniskilling Fusiliers", "",
     "1900-08-27", "engagement", "Durban", "Bergendal", "Bergendal",
     "1st Royal Inniskilling Fusiliers fought at Bergendal (27 Aug 1900) under Lyttelton's 4th Division in the assault on the Boer rearguard.",
     confidence="high", region="north")

# 1st Bn Devonshire Regiment (at Bergendal)
brit("1st Bn Devonshire Regiment", "Lt Col Bullock",
     "1900-01-01", "disembark", "", "Durban", "Durban",
     "1st Bn Devonshire Regiment disembarked at Durban with Buller's force. Distinct from the 2nd Bn which served in the Natal Field Force from the beginning of the campaign.",
     region="north")
brit("1st Bn Devonshire Regiment", "",
     "1900-08-27", "engagement", "Durban", "Bergendal", "Bergendal",
     "1st Bn Devonshire Regiment led the assault at Bergendal (27 Aug 1900), the final set-piece battle of the war; the Devon's attack broke the Boer line and drove Botha from his prepared positions.",
     confidence="high", region="north")
brit("1st Bn Devonshire Regiment", "",
     "1900-09-01", "redeployment", "Bergendal", "Lydenburg", "Lydenburg",
     "1st Bn Devonshire Regiment continued the pursuit of Botha's force east towards Lydenburg following Bergendal.",
     region="north")

# De la Rey's Commando (Nooitgedacht)
boer("De la Rey's Commando", "Gen Koos de la Rey",
     "1899-10-11", "engagement", "", "Kimberley", "Kimberley",
     "De la Rey's western Transvaal commando besieged Kimberley from the outset of the war, holding the Kimberley front under De la Rey's command.",
     confidence="high")
boer("De la Rey's Commando", "Gen Koos de la Rey",
     "1899-12-11", "engagement", "Kimberley", "Magersfontein", "Magersfontein",
     "De la Rey commanded the Boer right at Magersfontein, where his prepared trenches inflicted catastrophic casualties on the Highland Brigade.",
     confidence="high")
boer("De la Rey's Commando", "Gen Koos de la Rey",
     "1900-12-13", "engagement", "Krugersdorp", "Nooitgedacht", "Nooitgedacht",
     "De la Rey led the assault at Nooitgedacht (13 Dec 1900), ambushing Clements's brigade on Yeomanry Hill with devastating effect.",
     confidence="high")
boer("De la Rey's Commando", "Gen Koos de la Rey",
     "1902-03-07", "engagement", "Nooitgedacht", "Tweebosch", "Tweebosch",
     "De la Rey defeated and captured General Methuen at the Battle of Tweebosch (7 Mar 1902), the last major Boer victory of the war.",
     confidence="high")

# Beyers's Commando (Nooitgedacht)
boer("Beyers's Commando", "Gen Christiaan Beyers",
     "1900-06-01", "redeployment", "", "Pretoria", "Pretoria",
     "Beyers's commando operated in the northern Transvaal under General Beyers, eventually becoming active in the western guerrilla theatre.",
     region="north")
boer("Beyers's Commando", "Gen Christiaan Beyers",
     "1900-12-13", "engagement", "Pretoria", "Nooitgedacht", "Nooitgedacht",
     "Beyers's commando attacked from the mountaintop at Nooitgedacht (13 Dec 1900), catching Clements's British force in a pincer with De la Rey.",
     confidence="high", region="north")

# Diamond Fields Horse (Tweebosch)
brit("Diamond Fields Horse", "",
     "1900-01-01", "garrison", "", "Kimberley", "Kimberley",
     "Diamond Fields Horse, a colonial mounted corps recruited from the Kimberley diamond fields, deployed for mounted operations in the northern Cape and western Transvaal.",
     region="north")
brit("Diamond Fields Horse", "",
     "1902-03-07", "engagement", "Kimberley", "Tweebosch", "Tweebosch",
     "Diamond Fields Horse served as part of Methuen's rearguard column at the Battle of Tweebosch (7 Mar 1902) and were routed by De la Rey's commando.",
     confidence="high", region="north")

# Cape Police (Tweebosch)
brit("Cape Police", "",
     "1899-11-01", "garrison", "", "Cape Town", "Cape Town",
     "Cape Police (Cape Mounted Police / Cape Colony Police Force) mobilised for border patrol, convoy escort and garrison duties throughout the colony under martial law.",
     region="eastern")
brit("Cape Police", "",
     "1900-01-01", "redeployment", "Cape Town", "Colesberg", "Colesberg",
     "Cape Police deployed to the northern frontier zone around Colesberg and Aliwal North to support French's cavalry operations.",
     region="eastern")
brit("Cape Police", "",
     "1902-03-07", "engagement", "Colesberg", "Tweebosch", "Tweebosch",
     "Detachment of Cape Police served with Methuen's column at Tweebosch (7 Mar 1902) and were captured when De la Rey overwhelmed the British convoy.",
     confidence="high", region="north")

# ── LATE UNITS: push arrival event back before battle ─────────────────────────
LATE_ARRIVALS = [
    # (force_name, arrival_date, arrival_place, departure_place, description)
    ("Frontier Mounted Rifles", "1899-11-01", "Queenstown", "",
     "Frontier Mounted Rifles mobilised for active service at the outbreak of war, providing scouting and patrol support in the eastern Cape Colony."),
    ("2nd Bn West Surrey Regiment (Queen's)", "1899-11-01", "Durban", "",
     "2nd Bn West Surrey Regiment (Queen's) disembarked at Durban and joined Hildyard's 2nd Brigade for the Natal campaign."),
    ("2nd Bn Scottish Rifles", "1899-11-01", "Durban", "",
     "2nd Bn Scottish Rifles (Cameronians) disembarked at Durban and joined Lyttelton's 4th Brigade, Natal Field Force."),
    ("6th (Carabiniers) Dragoon Guards", "1899-11-01", "Durban", "",
     "6th Dragoon Guards (Carabiniers) disembarked at Durban and joined Dundonald's cavalry brigade, Natal Field Force."),
    ("Thorneycroft's Mounted Infantry", "1899-11-01", "Durban", "",
     "Thorneycroft's Mounted Infantry, raised in Natal, mobilised for service with Buller's column."),
    ("South African Light Horse", "1899-11-01", "Durban", "",
     "South African Light Horse, a colonial mounted corps, mobilised for service with Dundonald's cavalry in the Natal campaign."),
    ("G Battery Royal Horse Artillery", "1899-11-01", "Cape Town", "",
     "G Battery Royal Horse Artillery arrived at Cape Town and joined Methuen's 1st Division advance column."),
    ("62nd Battery Royal Field Artillery", "1899-11-01", "Cape Town", "",
     "62nd Battery Royal Field Artillery arrived at Cape Town and joined Methuen's column for the Magersfontein operations."),
    ("65th Howitzer Battery Royal Field Artillery", "1899-11-01", "Cape Town", "",
     "65th Howitzer Battery Royal Field Artillery joined Methuen's 1st Division for the Kimberley relief advance."),
    ("1st (Royal) Dragoons", "1899-11-01", "Durban", "",
     "1st Royal Dragoons disembarked at Durban and joined Dundonald's cavalry brigade for the Natal campaign."),
    ("13th Hussars", "1899-11-01", "Durban", "",
     "13th Hussars disembarked at Durban and served with Dundonald's cavalry in the Natal Field Force."),
    ("66th Battery Royal Field Artillery", "1899-11-01", "Durban", "",
     "66th Battery Royal Field Artillery arrived in Natal and joined Buller's Natal Field Force for the Colenso campaign."),
    ("73rd Battery Royal Field Artillery", "1899-11-01", "Durban", "",
     "73rd Battery Royal Field Artillery disembarked in Natal and provided artillery support at Colenso and subsequent battles."),
    ("2nd KOYLI", "1899-11-01", "Cape Town", "",
     "2nd Bn King's Own Yorkshire Light Infantry (KOYLI) disembarked at Cape Town and joined Methuen's 1st Division."),
]

for force, date, place, dep, desc in LATE_ARRIVALS:
    if force in by_force:
        # check if we already have an event before the needed date
        dates = [pd(r["date_start"]) for r in by_force[force] if pd(r["date_start"])]
        cutoff = pd(date)
        if not dates or min(dates) > cutoff:
            reg_ev("British", force, "", force, date, "",
                   "disembark", dep, place, place, desc,
                   confidence=LOW, region="north" if place in ("Durban","Cape Town") else "eastern")
            print("  Added arrival for: %s (%s)" % (force, date))
        else:
            print("  SKIP (already early enough): %s" % force)
    else:
        print("  SKIP (not in CSV): %s" % force)

# Also add 77th Battery RFA arrival (in CSV but first event Jun 1900)
brit("77th Battery Royal Field Artillery", "",
     "1899-11-01", "disembark", "", "Cape Town", "Cape Town",
     "77th Battery Royal Field Artillery arrived at Cape Town and joined Gatacre's column in the eastern Cape.",
     region="eastern")

# 12th Lancers arrival (in CSV as '12th Prince of Wales's Royal Lancers (2nd)', first event Jan 1901)
# Need to find and add pre-Magersfontein event
force_12th = "12th Prince of Wales's Royal Lancers (2nd)"
if force_12th in by_force:
    dates = [pd(r["date_start"]) for r in by_force[force_12th] if pd(r["date_start"])]
    if not dates or min(dates) > pd("1899-12-11"):
        reg_ev("British", force_12th, "", force_12th,
               "1899-11-01", "", "disembark", "", "Cape Town", "Cape Town",
               "12th (Prince of Wales's Royal) Lancers (2nd) arrived at Cape Town and joined Methuen's cavalry for the Kimberley relief advance.",
               confidence=LOW, region="north")
        print("  Added arrival for: %s" % force_12th)

# Bethune's Mounted Infantry (first event May 1900, but at Colenso Dec 1899)
force_beth = "Bethune's Mounted Infantry"
if force_beth in by_force:
    dates = [pd(r["date_start"]) for r in by_force[force_beth] if pd(r["date_start"])]
    if not dates or min(dates) > pd("1899-12-15"):
        reg_ev("British", force_beth, "Lt Col Bethune", force_beth,
               "1899-11-01", "", "disembark", "", "Durban", "Durban",
               "Bethune's Mounted Infantry, raised in Natal, mobilised and joined Dundonald's cavalry brigade for the Natal campaign.",
               confidence=LOW, region="north")
        print("  Added arrival for: %s" % force_beth)

# ── WRITE CSV ─────────────────────────────────────────────────────────────────
print()
print("New rows: %d  (IDs %d-%d)" % (len(new_rows), max_id + 1, nid[0] - 1))

all_rows = rows + new_rows
with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(all_rows)
print("CSV written: %d total rows" % len(all_rows))

# ── INJECT INTO build_map.py ──────────────────────────────────────────────────
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
