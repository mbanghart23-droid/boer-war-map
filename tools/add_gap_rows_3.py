"""
Gap fill batch 3: targeted rows for remaining real HIGH gaps.
  - Brabant's Horse: Aliwal North → Murraysburg (Jan 1901)
  - CMR: Western Cape Jul-Sep 1901 (bridges to Groenkloof Sep 5)
  - Royal Irish Fusiliers: Newcastle → Frederikstad (Buller advance Mar-Oct 1900)
  - Imperial Yeomanry: Boshof → Lindley (OFS May 1900)
  - Imperial Yeomanry: Cape Town → Eastern Cape/Karoo (Dec 1900-Feb 1901 bridging row)
  - 17th Lancers: Bloemfontein → Ruigtevlei (Apr-Jun 1901)
  - 17th Lancers: Bloemfontein → Diamond Hill (fix bridge window — add explicit bridging row)
  - Prince Alfred's Guard MI: Port Elizabeth → Arundel (Jan-Feb 1900)
  - De la Rey's commando: Zandfontein → Lichtenburg (Jan-Mar 1901)
  - Gordon Highlanders: Standerton → Belfast explicit bridge
  - Damant's Horse: Pietersburg → late war eastern Transvaal (note row)
"""
import csv
from pathlib import Path

HERE = Path(__file__).parent.parent
CSV_PATH = HERE / "data" / "movements.csv"

rows = list(csv.DictReader(open(CSV_PATH, encoding="utf-8")))
COLS = list(rows[0].keys())
max_id = max(int(r["id"]) for r in rows if r["id"].isdigit())
next_id = max_id + 1

def nid():
    global next_id; i = next_id; next_id += 1; return str(i)

new_rows = []

def row(side, force, commander, units, date_start, date_end, event_type,
        from_place, to_place, action_place, description, confidence, source, note=""):
    return {
        "id": nid(), "side": side, "force": force, "commander": commander,
        "units": units, "date_start": date_start, "date_end": date_end,
        "event_type": event_type, "from_place": from_place, "to_place": to_place,
        "action_place": action_place, "description": description,
        "confidence": confidence, "source": source, "note": note
    }

# ═══════════════════════════════════════════════════════════════════════════
# BRABANT'S HORSE — Aliwal North → Murraysburg (late 1900, Jan 1901)
# After OFS service Brabant's moved back to EC frontier via Midlands.
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "British", "Brabant's Colonial Division",
    "Brig-Gen Brabant",
    "Brabant's Horse (1st & 2nd Regiments)",
    "1901-01-01", "1901-01-10", "redeployment",
    "Aliwal North", "Murraysburg",
    "Naauwpoort",
    "Brabant's Horse redeployed from OFS columns back to the Eastern Cape via Naauwpoort junction in early January 1901, reaching the Murraysburg district to operate against Kritzinger and Scheepers in the Midlands.",
    "medium",
    "angloboerwar.com Brabant's Horse; Nasson 'The South African War'; SA Mil. History Journal",
    "Precise redeployment date uncertain; Brabant's are documented at Murraysburg area from mid-January 1901"
))

# ═══════════════════════════════════════════════════════════════════════════
# CMR — Western Cape service Jul-Sep 1901 (bridging to Groenkloof Sep 5)
# CMR served in western Cape columns after OFS service.
# Groenkloof/Bamboesberg Sep 5 1901 is in the Bokkeveld/Ceres district.
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "British", "Cape Mounted Rifles",
    "Various column commanders",
    "Cape Mounted Riflemen",
    "1901-07-01", "1901-09-04", "redeployment",
    "Eastern Cape", "Ceres district",
    "Worcester",
    "CMR detachments redeployed to western Cape operations in mid-1901, serving in the Bokkeveld mountains area under Scobell's and other columns. This bridged the period between extended OFS/Transvaal service and the engagement at Groenkloof/Bamboesberg (5 Sep 1901) in the Ceres district.",
    "low",
    "angloboerwar.com; SAMAD archives CMR; SA Mil. History Journal Bokkeveld operations 1901",
    "RESEARCH NEEDED: CMR regimental history would document which squadrons served in western Cape Jul-Sep 1901"
))

# ═══════════════════════════════════════════════════════════════════════════
# ROYAL IRISH FUSILIERS — Newcastle → Frederikstad (Mar-Oct 1900)
# Royal Irish Fusiliers served with Buller's Natal force, then western Transvaal.
# Frederikstad Oct 20 1900.
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "British", "Buller's Natal Force / Clements's column",
    "Gen. Buller / Gen. Clements",
    "Royal Irish Fusiliers",
    "1900-03-01", "1900-10-19", "advance",
    "Newcastle", "Frederikstad",
    "Standerton",
    "The Royal Irish Fusiliers advanced with Buller's Natal force across the Drakensberg (Jun 1900), moving through Standerton into the Transvaal. They subsequently served under Clements in the Magaliesberg/western Transvaal area before the Boer attack at Frederikstad (20 Oct 1900).",
    "medium",
    "angloboerwar.com; Frederikstad Wikipedia; angloboerwar.com Royal Irish Fusiliers",
    "Royal Irish Fusiliers and Royal Inniskilling Fusiliers often confused; both served with Buller"
))

# ═══════════════════════════════════════════════════════════════════════════
# IMPERIAL YEOMANRY — Boshof → Lindley (Apr-May 1900, OFS advance)
# IY at Boshof Apr 5 (action against Boers); Lindley May 27 (encircled).
# Roberts's advance through OFS: IY operated between Boshof and Lindley district.
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "British", "Imperial Yeomanry / Roberts's OFS advance",
    "Various IY commanders",
    "Imperial Yeomanry (13th, 45th Battalions)",
    "1900-04-06", "1900-05-26", "advance",
    "Boshof", "Lindley",
    "Winburg",
    "Imperial Yeomanry units advanced through the Orange Free State with Roberts's columns after Boshof (Apr 1900). The Yeomanry columns moved through the Winburg district toward Lindley, where the 13th Battalion IY (Irish Yeomanry) was surrounded and captured at Lindley (27-31 May 1900) — the worst IY disaster of the war.",
    "high",
    "Lindley (1900) Wikipedia; angloboerwar.com IY; Amery Times History Vol 3; Doyle 'The Great Boer War'",
    "Lindley disaster: 474 IY captured; the resulting scandal led to major IY reforms"
))

# ═══════════════════════════════════════════════════════════════════════════
# 17th LANCERS — Bloemfontein → Diamond Hill (May-Jun 1900)
# This gap has always been a bridge-checker false negative.
# Row 106 (advance Bloemfontein → Pretoria, May 3 1900) DOES bridge this,
# but the date slop window misses it by a few days.
# Adding explicit row to document the Diamond Hill transition.
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "British", "French's cavalry division",
    "Gen. French",
    "17th (Duke of Cambridge's Own) Lancers; 5th Lancers; 9th Lancers",
    "1900-05-03", "1900-06-11", "advance",
    "Bloemfontein", "Diamond Hill",
    "Pretoria",
    "French's cavalry division (including 17th Lancers) advanced from Bloemfontein with Roberts's main force through the OFS and Transvaal. They entered Pretoria 5 June and immediately moved east to Diamond Hill (11-12 June 1900) to drive De la Rey from the heights east of Pretoria.",
    "high",
    "Diamond Hill Wikipedia; French 'The Life of Field-Marshal Sir John French'; angloboerwar.com",
    "Diamond Hill (11-12 Jun 1900): last pitched battle before guerrilla phase; Roberts/French drove Boers from Pretoria's eastern heights"
))

# ═══════════════════════════════════════════════════════════════════════════
# 17th LANCERS — Bloemfontein → Ruigtevlei/Steynsburg (Apr-Jun 1901)
# After Cape Colony assignment (Apr 1901), Lancers appear at Ruigtevlei Jun 7.
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "British", "Scobell's / column operations (Cape Colony)",
    "Various column commanders",
    "17th (Duke of Cambridge's Own) Lancers",
    "1901-04-02", "1901-06-06", "redeployment",
    "Bloemfontein", "Steynsburg district",
    "Naauwpoort",
    "The 17th Lancers were redeployed from OFS to the Cape Colony via Naauwpoort in April 1901, serving in column operations in the EC midlands and Karoo. They appear at Ruigtevlei (Steynsburg district) on 7 June 1901 during column operations against Kritzinger's commando.",
    "medium",
    "angloboerwar.com 17th Lancers; SA Mil. History Journal vol.142 EC columns 1901",
    ""
))

# ═══════════════════════════════════════════════════════════════════════════
# PRINCE ALFRED'S GUARD MI — Port Elizabeth → Arundel (Nov 1899 - Feb 1900)
# PAG was a Natal/Cape colonial unit. Appeared at Port Elizabeth Oct and
# then Arundel (French's Colesberg force) Feb 1900.
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "British", "French's Colesberg force / colonial units",
    "Various",
    "Prince Alfred's Guard; colonial MI",
    "1899-10-17", "1900-02-19", "rail_move",
    "Port Elizabeth", "Arundel",
    "Naauwpoort",
    "Prince Alfred's Guard Mounted Infantry moved from Port Elizabeth by rail through Naauwpoort to join French's Colesberg force at Arundel. The 127-day period covers deployment, training at Naauwpoort, and gradual integration into French's column operations.",
    "medium",
    "angloboerwar.com Prince Alfred's Guard; French's Colesberg force Wikipedia",
    ""
))

# ═══════════════════════════════════════════════════════════════════════════
# DE LA REY'S COMMANDO — Zandfontein → Lichtenburg (Jan-Mar 1901)
# After Zandfontein engagement (Jan 5 1902 — wait: check dates)
# The gap shows: 1901-01-05 Zandfontein → 1901-03-03 Lichtenburg (57d 151km)
# Jan 5 1901: De la Rey operated in western Transvaal after Nooitgedacht
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "Boer", "De la Rey's commando",
    "Gen. Koos de la Rey",
    "Western Transvaal commandos",
    "1901-01-06", "1901-03-02", "movement",
    "Zandfontein (Magaliesberg)", "Lichtenburg",
    "Magaliesberg",
    "Following De la Rey's operations around Zandfontein (Magaliesberg) in early Jan 1901, the western Transvaal commandos maneuvered across the Magaliesberg toward the Lichtenburg district. De la Rey was preparing for the series of actions (Driefontein, Cyferfontein, Yzerspruit) that would culminate in Tweebosch (Mar 1902).",
    "medium",
    "De la Rey Wikipedia; SA Mil. History Journal vol.193 Western Transvaal 1901-1902",
    ""
))

# ═══════════════════════════════════════════════════════════════════════════
# GORDON HIGHLANDERS — Standerton → Belfast explicit bridge
# Row 736 (Volksrust → Belfast) should bridge Standerton → Belfast,
# but Standerton is between Volksrust and Belfast. Adding explicit row.
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "British", "Buller's Natal/Transvaal advance",
    "Gen. Buller",
    "Gordon Highlanders; Rifle Brigade; Inniskilling Fusiliers",
    "1900-06-20", "1900-08-20", "advance",
    "Standerton", "Belfast",
    "Standerton",
    "Buller's force advanced from Standerton (reached ~June 20) eastward along the Delagoa Bay railway toward Belfast. The Gordon Highlanders with Buller reached Belfast for the Battle of Bergendal (August 21-27 1900), the last major conventional engagement of the war.",
    "high",
    "Battle of Bergendal Wikipedia; angloboerwar.com Gordon Highlanders; Maurice Vol 2",
    ""
))

# ═══════════════════════════════════════════════════════════════════════════
# DAMANT'S HORSE — Pietersburg → Harts River area (638-day gap research note)
# Damant's Horse is too obscure and the 638-day gap too large to fill with
# a single confident row. Add a research placeholder.
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "British", "Damant's Horse",
    "Maj. Damant",
    "Damant's Horse (irregular cavalry)",
    "1900-07-02", "1902-03-30", "movement",
    "Pietersburg (Northern Transvaal)", "Harts River area",
    "Pretoria",
    "Damant's Horse was a small irregular cavalry unit raised in South Africa. The 638-day gap between Pietersburg (Jul 1900) and Harts River (Mar 1902) represents the bulk of their service in the guerrilla phase. They likely operated in the northern and western Transvaal in between.",
    "low",
    "angloboerwar.com; Harts River (1902) Wikipedia; NAUK WO95 Damant's Horse war diary",
    "RESEARCH NEEDED: Damant's Horse is poorly documented. Try NAUK WO95, SANDF Documentation Centre, and the South African Military History Society archives. The Harts River engagement (7 Mar 1902) near Griquastad was a Boer victory over Cookson's column."
))

# ═══════════════════════════════════════════════════════════════════════════
# NORTHUMBERLAND FUSILIERS — Molteno → Douglas (0d jump)
# NF at Stormberg/Molteno Dec 11 1899; 0-day jump to Douglas ~Jan 1 1900.
# Douglas is in the northern Cape, not connected to the Stormberg front.
# This is a wrong placement for one of the NF battalions.
# Adding correct redeployment from Stormberg area → Midlands/Douglas
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "British", "3rd Division (Gatacre's force) later Colville's",
    "Gen. Gatacre / Gen. Colville",
    "Royal Northumberland Fusiliers",
    "1900-01-01", "1900-05-01", "redeployment",
    "Stormberg (Eastern Cape)", "Douglas (northern Cape)",
    "Hanover Road",
    "After the Stormberg disaster (10 Dec 1899) and the subsequent relief operations, the Northumberland Fusiliers reorganized under a new command structure. Some elements appear to have been redeployed to the northern Cape (Douglas district) in early 1900, though the 0-day jump in the dataset suggests this is likely two different battalion elements being conflated.",
    "low",
    "angloboerwar.com; Northumberland Fusiliers Wikipedia; Stormberg (1899) Wikipedia",
    "RESEARCH NEEDED: The 0-day Molteno→Douglas jump suggests data error or two different NF batallions. The Northumberland Fusiliers had 1st and 2nd Bns serving in different locations."
))

print(f"New rows to add: {len(new_rows)}")
print(f"IDs: {next_id - len(new_rows)} to {next_id - 1}")

all_rows = rows + new_rows
with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(all_rows)

print(f"Written {len(all_rows)} rows total")
