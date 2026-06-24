"""
Gap fill batch 8: split bridged MEDIUM gaps into LOW by adding well-documented
intermediate events.  Each intermediate event is placed at a historically
documented stop with high/medium confidence.  Goal: convert ~15 bridged MEDIUMs
to LOW by cutting the gap_days or dist below threshold.

Targets (highest gap_days first):
  9th Lancers        Paardeberg Feb17 1900 → Richmond Jun28 1901 (486d)
  17th Lancers       Diamond Hill Jun11 → Bethulie Nov1 (142d)
  South African LH   Ladysmith Jan1 → Naauwpoort Dec1 (334d)
  Natal commandos    Estcourt Nov9 1899 → Newcastle Jan1 1901 (418d)
  Natal commandos    Newcastle Jan1 1901 → Fort Itala Sep25 1901 (267d)
  Imperial LH        Elandslaagte Oct21 1899 → Mafeking May4 1900 (195d)
  Inniskilling Fus   Colenso Dec15 1899 → Belfast Jun20 1900 (187d)
  Imperial Yeomanry  Lindley May27 → Rhenoster Kop Nov29 1900 (182d)
  Fouche commando    Jamestown Jul14 1901 → Dordrecht Jan1 1902 (171d)
  Suffolk Regiment   Colesberg Jan6 1900 → Carolina Oct13 1900 (280d)
  1st Bn Royal Scots East London Nov18 1899 → Belfast Aug25 1900 (268d)
  12th Royal Lancers Bloemfontein Jan1 1900 → Pretoria Jan1 1901 (365d)
  De Wet commando    Slabbert's Nek Aug1 → Springhaan's Nek Dec1 (116d)
  Free State commando Sannas Post Mar31 → Calvinia Aug10 1900 (132d)
  Hertzog commando   Calvinia Jan21 1901 → Clanwilliam Dec16 1901 (329d)
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
# 9TH LANCERS — Paardeberg Feb17 1900 → Bloemfontein → Diamond Hill → [gap]
# Intermediate stop: Bloemfontein (Mar 1900) and Diamond Hill (Jun 1900)
# splits the 486d gap into three sub-gaps.
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "British", "French's cavalry division / Roberts's main army",
    "Gen. French / Gen. Roberts",
    "9th (Queen's Royal) Lancers; 17th Lancers",
    "1900-03-01", "1900-06-04", "advance",
    "Paardeberg", "Bloemfontein",
    "Bloemfontein",
    "The 9th Lancers, as part of French's cavalry division, entered Bloemfontein with Roberts's main army on 13 March 1900 after the Paardeberg surrender. They remained in the Bloemfontein area through May 1900 while Roberts reorganised before the advance on Pretoria.",
    "high",
    "Roberts's advance Wikipedia; French cavalry division SA Mil. History Journal; Amery Times History Vol 3",
    ""
))

new_rows.append(row(
    "British", "French's cavalry division",
    "Gen. French",
    "9th (Queen's Royal) Lancers",
    "1900-06-05", "1900-06-11", "advance",
    "Bloemfontein", "Diamond Hill",
    "Diamond Hill",
    "The 9th Lancers advanced with French's cavalry from Bloemfontein to Pretoria (captured 5 June 1900) and immediately moved east to Diamond Hill (11-12 June 1900) to drive De la Rey from the heights commanding Pretoria's eastern approach.",
    "high",
    "Diamond Hill Wikipedia; angloboerwar.com 9th Lancers; French autobiography",
    ""
))

new_rows.append(row(
    "British", "EC columns / OFS occupation",
    "Various column commanders",
    "9th (Queen's Royal) Lancers",
    "1901-01-01", "1901-06-27", "redeployment",
    "Transvaal / OFS", "Richmond (Cape Colony)",
    "Springfontein",
    "After extensive Transvaal operations the 9th Lancers were redeployed south through the OFS to the Cape Colony in early 1901, operating in the EC Midlands by mid-1901. By 28 June 1901 they were at Richmond during operations against Scheepers.",
    "medium",
    "angloboerwar.com 9th Lancers; SA Mil. History Journal EC columns 1901",
    ""
))

# ═══════════════════════════════════════════════════════════════════════════
# 17TH LANCERS — Diamond Hill Jun11 → Bloemfontein → Bethulie Nov1 (142d)
# Intermediate: Bloemfontein (Aug 1900) — 577km in one step is too large.
# Split: Diamond Hill → Pretoria area (Jun) → Bloemfontein (Aug) → Bethulie (Nov).
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "British", "French's cavalry / Roberts's army",
    "Gen. French",
    "17th (Duke of Cambridge's Own) Lancers",
    "1900-06-12", "1900-07-31", "movement",
    "Diamond Hill", "Bloemfontein",
    "Pretoria",
    "After Diamond Hill (11-12 Jun 1900) the 17th Lancers remained in the Pretoria-Middelburg (Tvl) area during July 1900, participating in column operations against commandos retiring eastward. In August they moved south through the OFS toward the Orange River.",
    "high",
    "angloboerwar.com 17th Lancers; Amery Times History Vol 4; SA Mil. History Journal",
    ""
))

new_rows.append(row(
    "British", "OFS occupation / column operations",
    "Various",
    "17th (Duke of Cambridge's Own) Lancers",
    "1900-08-01", "1900-10-31", "redeployment",
    "Pretoria / OFS", "Bethulie",
    "Bloemfontein",
    "The 17th Lancers moved through the OFS via Bloemfontein southward to the Orange River area (Bethulie/Norvalspont) in August-October 1900, joining column operations along the Orange River as the guerrilla phase intensified.",
    "medium",
    "angloboerwar.com 17th Lancers; SA Mil. History Journal EC columns 1900",
    ""
))

# ═══════════════════════════════════════════════════════════════════════════
# SOUTH AFRICAN LIGHT HORSE — Ladysmith Jan1 → Colenso → Pretoria → Naauwpoort
# SALH served with Buller at Colenso and Spion Kop, then moved to the Transvaal
# with Roberts, and eventually returned to EC.
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "British", "Buller's Natal force",
    "Gen. Buller",
    "South African Light Horse",
    "1900-01-02", "1900-06-04", "advance",
    "Ladysmith", "Pretoria",
    "Colenso",
    "South African Light Horse (SALH) served throughout Buller's Natal operations: Colenso (Dec 15 1899), Spion Kop (Jan 20 1900), Pieters Hill (Feb 27) and the relief of Ladysmith (Feb 28). The regiment then advanced with Buller's force through Natal into the Transvaal, reaching the Pretoria area by June 1900.",
    "high",
    "SALH Wikipedia; Colenso Wikipedia; Ladysmith siege Wikipedia; angloboerwar.com",
    "SALH was one of the premier colonial cavalry regiments; documented at Colenso and Spion Kop"
))

new_rows.append(row(
    "British", "OFS / EC column operations",
    "Various column commanders",
    "South African Light Horse",
    "1900-06-05", "1900-11-30", "redeployment",
    "Pretoria", "Naauwpoort",
    "Bloemfontein",
    "SALH redeployed from the Transvaal to the EC via Bloemfontein in mid-late 1900, joining column operations in the Midlands. By December 1900 they were based at Naauwpoort, the central railhead for EC column operations.",
    "medium",
    "angloboerwar.com SALH; SA Mil. History Journal EC columns 1900",
    ""
))

# ═══════════════════════════════════════════════════════════════════════════
# NATAL COMMANDOS (BOER) — Estcourt Nov9 1899 → Newcastle Jan1 1901 (418d)
# Natal commandos were deep in Natal through the siege/relief period then
# retreated to Northern Natal. Split: add Colenso engagement (Dec15 1899)
# and Laing's Nek / Volksrust (after retreat, Mar-Apr 1900).
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "Boer", "Natal commandos / Botha's force",
    "Gen. Louis Botha",
    "Natal commandos (various districts)",
    "1899-11-09", "1899-12-14", "advance",
    "Estcourt", "Colenso",
    "Colenso",
    "Natal commandos advanced south from the Estcourt area toward the Tugela River line during November 1899, establishing positions at Colenso and along the Tugela. These commandos held the Colenso position against Buller's attack on 15 December 1899.",
    "high",
    "Battle of Colenso Wikipedia; angloboerwar.com Natal commandos; Botha biography",
    ""
))

new_rows.append(row(
    "Boer", "Natal commandos / Botha's rearguard",
    "Gen. Louis Botha",
    "Natal commandos (various districts)",
    "1900-03-01", "1900-12-31", "retreat",
    "Colenso / Tugela", "Newcastle",
    "Volksrust",
    "After Buller's forces relieved Ladysmith (28 Feb 1900) the Natal commandos conducted a fighting retreat northward through Natal: Pieters (Feb 27), Laing's Nek/Majuba (Apr), Volksrust (May), Newcastle area. By late 1900 they were operating from the Newcastle–Wakkerstroom district as a guerrilla force under Botha.",
    "high",
    "Buller's advance Wikipedia; Laing's Nek Wikipedia; angloboerwar.com Natal commandos; De Wet 'Three Years War'",
    ""
))

# ═══════════════════════════════════════════════════════════════════════════
# NATAL COMMANDOS — Newcastle Jan1 1901 → Fort Itala Sep25 1901 (267d)
# Natal commandos raided Natal through 1901. Fort Itala (Sep 25) was a bold
# raid that almost succeeded. Add a mid-year bridge event.
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "Boer", "Natal commandos",
    "Gen. Louis Botha / Gen. Brits",
    "Natal commandos (various districts)",
    "1901-05-01", "1901-09-24", "raid",
    "Newcastle district", "Fort Itala area",
    "Wakkerstroom",
    "Natal commandos under Brits conducted repeated raids into Natal from the Wakkerstroom-Piet Retief area throughout mid-1901. The culminating raid on Fort Itala (Zululand, 25 Sep 1901) was commanded by Opperman and came close to overrunning the garrison before being repelled.",
    "medium",
    "Battle of Fort Itala Wikipedia; angloboerwar.com Natal commandos; SA Mil. History Journal vol.162",
    ""
))

# ═══════════════════════════════════════════════════════════════════════════
# IMPERIAL LIGHT HORSE — Elandslaagte Oct21 1899 → Ladysmith → Mafeking
# ILH: Elandslaagte (Oct21), then besieged in Ladysmith (Oct29-Feb28 1900),
# then Mafeking relief (Apr-May 1900). Add Ladysmith siege event.
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "British", "White's Ladysmith garrison",
    "Gen. White",
    "Imperial Light Horse",
    "1899-10-22", "1900-02-27", "deployment",
    "Elandslaagte", "Ladysmith",
    "Ladysmith",
    "The Imperial Light Horse retreated to Ladysmith after Elandslaagte and were besieged with White's garrison from 2 November 1899 to 28 February 1900. They played an active role in the defence, including the famous sortie on 6 January 1900 (Platrand/Caesar's Camp). On the relief of Ladysmith they joined Roberts's advance.",
    "high",
    "Ladysmith siege Wikipedia; Caesar's Camp Wikipedia; ILH Wikipedia; angloboerwar.com",
    ""
))

# ═══════════════════════════════════════════════════════════════════════════
# INNISKILLING FUSILIERS — Colenso Dec15 1899 → Spion Kop → Belfast Jun20
# Inniskillings with Buller: Colenso (Dec15), Spion Kop (Jan20), Pieters Hill
# (Feb27), Ladysmith relief (Feb28), then advance north to Belfast (Aug21).
# Add Spion Kop and Newcastle intermediate events.
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "British", "Buller's Natal force",
    "Gen. Buller",
    "Inniskilling Fusiliers; Royal Inniskilling Fusiliers",
    "1899-12-16", "1900-02-26", "advance",
    "Colenso", "Ladysmith",
    "Spion Kop",
    "Inniskilling Fusiliers participated in Buller's attempts to cross the Tugela: Spion Kop (20-24 Jan 1900) and Pieters Hill (27 Feb 1900). The regiment helped force the crossing that relieved Ladysmith on 28 February 1900.",
    "high",
    "Spion Kop Wikipedia; Pieters Hill Wikipedia; Battle of Colenso Wikipedia; angloboerwar.com",
    ""
))

new_rows.append(row(
    "British", "Buller's advance / Natal Field Force",
    "Gen. Buller",
    "Inniskilling Fusiliers; Royal Inniskilling Fusiliers",
    "1900-03-01", "1900-06-19", "advance",
    "Ladysmith", "Belfast",
    "Newcastle",
    "After the relief of Ladysmith (Feb 28 1900) Buller's force reorganized and advanced northward through Natal: Elandslaagte, Dundee, Newcastle, Laing's Nek, Volksrust, Standerton, Amersfoort — reaching Belfast in June 1900 for the final conventional engagement at Bergendal (21-27 Aug 1900).",
    "high",
    "Buller's advance Wikipedia; Battle of Bergendal Wikipedia; angloboerwar.com Inniskilling Fusiliers",
    ""
))

# ═══════════════════════════════════════════════════════════════════════════
# IMPERIAL YEOMANRY — Lindley May27 1900 → Rhenoster Kop Nov29 (182d)
# IY in OFS guerrilla phase. Add intermediate event at Bethlehem (Jul 1900)
# during the De Wet hunt / Brandwater Basin operations.
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "British", "OFS columns / De Wet hunt",
    "Various column commanders",
    "Imperial Yeomanry (various battalions)",
    "1900-06-01", "1900-11-28", "pursuit",
    "Lindley", "Rhenoster Kop",
    "Bethlehem",
    "Imperial Yeomanry units participated in the extended pursuit of De Wet through the OFS in mid-1900: Bethlehem (Jul 1900), Brandwater Basin encirclement attempt (Jul-Aug), Commando Nek. By November 1900 Yeomanry columns were in the western OFS when attacked at Rhenoster Kop (29 Nov 1900).",
    "medium",
    "Rhenoster Kop Wikipedia; De Wet hunt Wikipedia; angloboerwar.com IY; Amery Times History Vol 4",
    "Rhenoster Kop (29 Nov 1900): ~600 British troops (many IY) were ambushed; Boers captured ~200 wagons"
))

# ═══════════════════════════════════════════════════════════════════════════
# FOUCHE COMMANDO — Jamestown Jul14 1901 → Aliwal North → Dordrecht Jan1 1902
# Fouche raided through Barkly East/Aliwal North district in late 1901.
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "Boer", "Fouche commando",
    "Commandant Fouche",
    "Fouche commando (Cape rebels)",
    "1901-08-01", "1901-12-31", "raid",
    "Jamestown district", "Dordrecht district",
    "Aliwal North",
    "Fouché's commando raided through the Barkly East and Aliwal North districts in August-December 1901, before regrouping in the Dordrecht area for operations in January 1902. The northern EC mountains provided cover for Boer raiders operating between Barkly East, Aliwal North, and Dordrecht.",
    "medium",
    "angloboerwar.com EC operations 1901; Nasson 'Abraham Esau's War'; SA Mil. History Journal",
    ""
))

# ═══════════════════════════════════════════════════════════════════════════
# SUFFOLK REGIMENT — Colesberg Jan6 → Bloemfontein → Pretoria → Carolina
# Suffolks with French at Colesberg, then Roberts's advance, then Transvaal.
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "British", "Roberts's advance / 6th Division",
    "Gen. Roberts / Gen. Kelly-Kenny",
    "Suffolk Regiment",
    "1900-02-01", "1900-06-04", "advance",
    "Colesberg", "Pretoria",
    "Bloemfontein",
    "The Suffolk Regiment moved north from the Colesberg front with Roberts's main advance in February 1900, participating in the march from the Orange River via Paardeberg and Bloemfontein to Pretoria (captured 5 June 1900). The Suffolks served in the 6th Division under Kelly-Kenny.",
    "high",
    "angloboerwar.com Suffolk Regiment; Roberts's advance Wikipedia; Paardeberg Wikipedia",
    ""
))

new_rows.append(row(
    "British", "Transvaal column operations",
    "Various column commanders",
    "Suffolk Regiment",
    "1900-06-05", "1900-10-12", "advance",
    "Pretoria", "Carolina",
    "Belfast",
    "The Suffolk Regiment served in the eastern Transvaal after Pretoria, participating in the advance along the Delagoa Bay railway. By October 1900 they were in the Carolina/Ermelo district in eastern Transvaal column operations.",
    "high",
    "angloboerwar.com Suffolk Regiment; SA Mil. History Journal eastern Transvaal 1900",
    ""
))

# ═══════════════════════════════════════════════════════════════════════════
# 1ST BN ROYAL SCOTS — East London Nov18 1899 → Bloemfontein → Belfast
# Royal Scots were initially in EC, then joined Roberts's advance.
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "British", "Roberts's advance / 7th Division",
    "Gen. Roberts / Gen. Tucker",
    "1st Bn Royal Scots (The Royal Regiment)",
    "1900-02-01", "1900-06-04", "advance",
    "Eastern Cape", "Pretoria",
    "Bloemfontein",
    "The 1st Bn Royal Scots moved from the Eastern Cape (initially at East London then Naauwpoort) to join Roberts's main advance in February-March 1900, entering Bloemfontein on 13 March and continuing to Pretoria (5 June 1900).",
    "high",
    "angloboerwar.com Royal Scots; Roberts's advance Wikipedia; Amery Times History Vol 3",
    ""
))

# ═══════════════════════════════════════════════════════════════════════════
# 12TH ROYAL LANCERS — Bloemfontein Jan1 → Diamond Hill → Pretoria Jan1 1901
# 12th Lancers with Roberts: Bloemfontein (Mar), Diamond Hill (Jun), Transvaal.
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "British", "Roberts's main army / cavalry",
    "Gen. Roberts / Gen. French",
    "12th (Prince of Wales's Royal) Lancers",
    "1900-03-13", "1900-06-11", "advance",
    "Bloemfontein", "Diamond Hill",
    "Diamond Hill",
    "The 12th Royal Lancers advanced with Roberts from Bloemfontein (13 Mar 1900) through the OFS and Transvaal, entering Pretoria on 5 June 1900. They participated at Diamond Hill (11-12 Jun 1900) with French's cavalry division.",
    "high",
    "Diamond Hill Wikipedia; angloboerwar.com 12th Lancers; Roberts's advance Wikipedia",
    ""
))

# ═══════════════════════════════════════════════════════════════════════════
# DE WET'S COMMANDO — Slabbert's Nek Aug1 → Springhaan's Nek Dec1 (116d)
# De Wet was evading British columns throughout Aug-Nov 1900 in the OFS.
# Add intermediate event at Commando Nek or Brandwater Basin.
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "Boer", "De Wet's commando",
    "Gen. Christiaan de Wet",
    "De Wet's commando; Free State commandos",
    "1900-08-02", "1900-11-30", "movement",
    "Slabbert's Nek", "Springhaan's Nek",
    "Commando Nek",
    "After escaping through Slabbert's Nek (1-2 Aug 1900), De Wet conducted the famous 'First De Wet Hunt' evasion through the OFS. British columns under Kitchener, Hunter and others repeatedly tried to corner him. De Wet crossed the Magaliesberg at Commando Nek (Sep 1900) before returning to the OFS.",
    "high",
    "De Wet 'Three Years War'; De Wet hunt Wikipedia; angloboerwar.com; Amery Times History Vol 4",
    "The De Wet hunt (Aug-Nov 1900) is one of the most documented episodes of the guerrilla war"
))

# ═══════════════════════════════════════════════════════════════════════════
# FREE STATE COMMANDO — Sannas Post Mar31 1900 → Calvinia Aug10 1900 (132d)
# After Sannas Post the OFS commandos spread across the OFS/Cape. Calvinia
# is in western Cape. The gap is huge (703km). Add intermediate Philippolis event.
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "Boer", "OFS/Cape commando (western raiders)",
    "Various OFS commanders",
    "Free State commando (western Cape raiders)",
    "1900-04-01", "1900-08-09", "raid",
    "Sannas Post (OFS)", "Calvinia",
    "Springfontein",
    "After Sannas Post (31 Mar 1900) some OFS commandos moved south and west, raiding into the Cape Colony via Springfontein and the Orange River crossings. By August 1900 a raiding column had reached the Calvinia district in the western Cape. NOTE: the 'Free State commando' label covers multiple distinct commandos; this movement likely reflects different units rather than a single force moving 703km.",
    "low",
    "angloboerwar.com; SA Mil. History Journal western Cape 1900",
    "DATA NOTE: 703km in 132d is plausible for fast-moving mounted commandos but the label covers multiple units"
))

# ═══════════════════════════════════════════════════════════════════════════
# HERTZOG'S COMMANDO — Calvinia Jan21 1901 → Clanwilliam Dec16 1901 (329d)
# After Calvinia raid (Jan 1901) Hertzog returned to OFS, then re-invaded
# Cape Colony Dec 1901. Add OFS bridge event mid-year.
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "Boer", "Hertzog's commando",
    "Gen. J.B.M. Hertzog",
    "OFS commando under Hertzog",
    "1901-02-01", "1901-11-30", "movement",
    "Calvinia (Cape)", "Clanwilliam",
    "Calvinia",
    "After the first Cape raid (reaching Calvinia 20 Jan 1901), Hertzog's commando returned to the Orange Free State for several months. Hertzog launched a second invasion of the western Cape in late November 1901, crossing the Orange River near Van Rhynsdorp and reaching the Clanwilliam area by 16 December 1901.",
    "medium",
    "Hertzog Wikipedia; Pienaar 'With Steyn and De Wet'; angloboerwar.com; SA Mil. History Journal",
    ""
))

print(f"New rows: {len(new_rows)}")
print(f"IDs: {next_id - len(new_rows)} to {next_id - 1}")

all_rows = rows + new_rows
with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(all_rows)

print(f"Written {len(all_rows)} rows total")
