"""
Add 22 missing colonial-raised and irregular scout units identified from:
  - TNA Kew WO126/145-163 nominal rolls
  - angloboerwar.com south-african-units pages
  - bowlerhat.com.au/saforce/ roster

Sources: angloboerwar.com; Conan Doyle 'The Great Boer War'; Pakenham 'The Boer War';
         TNA WO126 nominal rolls; SAMHS journal
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

SRC = "angloboerwar.com; TNA WO126; Conan Doyle 'The Great Boer War'; Pakenham 'The Boer War'"
NOTE = "Auto-generated from TNA/angloboerwar.com colonial unit roster (add_colonial_irregular.py); verify against unit roll"

new_rows = []
a_entries = []

REGION_MAP = {
    "Cape Town":"north","Kimberley":"north","Mafeking":"north","Johannesburg":"north",
    "Pretoria":"north","Durban":"north","Bloemfontein":"north","Pietersburg":"north",
    "Upington":"north","Clanwilliam":"north","Fraserburg":"eastern","Loxton":"eastern",
    "Graaff-Reinet":"eastern","Colesberg":"eastern","Aliwal North":"eastern",
    "De Aar":"eastern","Queenstown":"eastern","Sterkstroom":"eastern","Molteno":"eastern",
    "Kokstad":"north","Vryheid":"north","Zululand":"north","Herschel":"eastern",
}

def add(force, side, date_start, event_type, action_place, description,
        from_place="", to_place="", commander=""):
    rid = nxt()
    tp = to_place or action_place
    new_rows.append({
        "id": rid, "side": side, "force": force,
        "commander": commander, "units": force,
        "date_start": date_start, "date_end": "",
        "event_type": event_type,
        "from_place": from_place or "", "to_place": tp, "action_place": action_place,
        "description": description,
        "confidence": "low", "source": SRC, "note": NOTE,
    })
    reg = REGION_MAP.get(action_place, "north")
    fp = from_place or ""
    if fp and fp != action_place:
        a_entries.append(' "%s": dict(pt="%s", line=(%r, %r), region="%s"),' % (
            rid, action_place, fp, action_place, reg))
    else:
        a_entries.append(' "%s": dict(pt="%s", region="%s"),' % (rid, action_place, reg))

def unit(force, side, events):
    """events: list of (date, event_type, place, description, from_place, commander)"""
    for e in events:
        date, et, place = e[0], e[1], e[2]
        desc = e[3]
        fp = e[4] if len(e) > 4 else ""
        co = e[5] if len(e) > 5 else ""
        add(force, side, date, et, place, desc, from_place=fp, commander=co)

# ── MOUNTED CORPS & LIGHT HORSE ───────────────────────────────────────────────

unit("Bechuanaland Rifles", "British", [
    ("1899-10-12", "garrison", "Mafeking",
     "Bechuanaland Rifles mobilised at outbreak of war. A substantial portion of the regiment was caught in the Mafeking siege, serving alongside the Protectorate Regiment and Mafeking Town Guard under Baden-Powell.",
     "", "Lt Col Hore"),
    ("1900-05-17", "redeployment", "Mafeking",
     "Bechuanaland Rifles stood down siege duties following the relief of Mafeking by Mahon's column, 17 May 1900.",
     "", ""),
])

unit("Bushmanland Borderers", "British", [
    ("1901-06-01", "garrison", "Upington",
     "Bushmanland Borderers raised in Namaqualand/Bushmanland to defend the remote northern Cape from Boer incursions and to control the Upington-Namaqualand borders.",
     "", ""),
    ("1902-05-31", "garrison", "Upington",
     "Bushmanland Borderers stood down following the Peace of Vereeniging.",
     "", ""),
])

unit("Clanwilliam Convoy Guard", "British", [
    ("1901-03-01", "garrison", "Clanwilliam",
     "Clanwilliam Convoy Guard raised in the Clanwilliam district of the western Cape to protect supply convoys against Boer raiding columns. Hertzog's commando raided the area in early 1902.",
     "", ""),
    ("1902-01-10", "engagement", "Clanwilliam",
     "Clanwilliam Convoy Guard on alert as Hertzog's commando raided through the western Cape reaching Clanwilliam district, January 1902.",
     "", ""),
])

unit("Griqualand East Light Horse", "British", [
    ("1901-03-01", "garrison", "Kokstad",
     "Griqualand East Light Horse (also recorded as Griqualand Light Horse) formed in East Griqualand early 1901, recruited in the Mount Currie, Kokstad, and Matatiele districts, with extension into Harding district of Natal. Raised to defend the borders of East Griqualand against Boer raiding and rebel activity. (angloboerwar.com/unit-information/south-african-units/3320-griqualand-light-horse)",
     "", ""),
    ("1902-05-31", "garrison", "Kokstad",
     "Griqualand East Light Horse stood down on conclusion of the peace.",
     "", ""),
])

unit("Hannay's Scouts", "British", [
    ("1900-01-01", "garrison", "De Aar",
     "Hannay's Scouts raised in the Cape Colony, named for Colonel Hannay who led mounted forces in the northern Cape and the Roberts advance. Hannay was killed at Paardeberg, 18 Feb 1900, and the scouts were subsequently absorbed into other mounted units.",
     "", "Col Hannay"),
    ("1900-02-18", "engagement", "Bloemfontein",
     "Hannay's Scouts active at Paardeberg operations; Col Hannay was killed leading the charge on 18 Feb 1900. The unit subsequently served under Kitchener's column reorganisation.",
     "", ""),
])

unit("Herbert Mounted Rifles", "British", [
    ("1901-06-01", "garrison", "Kimberley",
     "Herbert Mounted Rifles raised in the Herbert district (Griqualand West / northern Cape) for local defence and mounted patrol duties along the Vaal River valley.",
     "", ""),
    ("1902-05-31", "garrison", "Kimberley",
     "Herbert Mounted Rifles stood down following the Peace of Vereeniging.",
     "", ""),
])

unit("Johannesburg Mounted Rifles", "British", [
    ("1900-06-15", "garrison", "Johannesburg",
     "Johannesburg Mounted Rifles raised following the British occupation of Johannesburg (31 May 1900), recruited mainly from English refugees and Rand mine employees for garrison and police duties in the district.",
     "", ""),
    ("1901-01-01", "redeployment", "Johannesburg",
     "Johannesburg Mounted Rifles continued garrison and mounted patrol duties around the Rand mining district during the guerrilla phase.",
     "", ""),
    ("1902-05-31", "garrison", "Johannesburg",
     "Johannesburg Mounted Rifles stood down following the Peace of Vereeniging.",
     "", ""),
])

unit("Kimberley Mounted Corps", "British", [
    ("1899-10-14", "garrison", "Kimberley",
     "Kimberley Mounted Corps formed at the outbreak of war, distinct from the Kimberley Light Horse, raised from the Kimberley civilian population for mounted patrol and scouting duties during and after the siege.",
     "", ""),
    ("1900-02-15", "redeployment", "Kimberley",
     "Kimberley Mounted Corps resumed mounted patrol duties following the relief of Kimberley by French's cavalry, 15 February 1900.",
     "", ""),
])

unit("Loxton's Horse", "British", [
    ("1901-06-01", "garrison", "Graaff-Reinet",
     "Loxton's Horse raised in the Karoo/Loxton district of the northern Cape as a locally-organised mounted corps for column support and district patrol during the guerrilla phase.",
     "", ""),
    ("1902-05-31", "garrison", "Graaff-Reinet",
     "Loxton's Horse stood down following the Peace of Vereeniging.",
     "", ""),
])

unit("Marshall's Horse", "British", [
    ("1900-01-15", "disembark", "Cape Town",
     "Marshall's Horse raised in South Africa and formed part of Roberts's advance column from Modder River to Bloemfontein, February-March 1900.",
     "", ""),
    ("1900-02-01", "redeployment", "Bloemfontein",
     "Marshall's Horse participated in Roberts's advance from Modder River to Bloemfontein, February-March 1900, serving on the flanks of the main column.",
     "Cape Town", "Bloemfontein", ""),
    ("1900-06-01", "redeployment", "Pretoria",
     "Marshall's Horse continued north with Roberts's main force, advancing to Pretoria.",
     "Bloemfontein", "Pretoria", ""),
])

unit("Menne's Scouts", "British", [
    ("1900-06-01", "garrison", "Durban",
     "Menne's Scouts raised in Natal by Major T. Menne, with the nucleus drawn from his own 'G' Squadron of the Colonial Scouts (which disbanded April 1900). Operated as a mounted scout and intelligence corps in the Natal-Transvaal border zone.",
     "", "Maj T. Menne"),
    ("1901-01-01", "redeployment", "Durban",
     "Menne's Scouts continued mounted intelligence and patrol operations along the Natal-Transvaal border during the guerrilla phase.",
     "", "Maj T. Menne"),
])

unit("Montmorency's Scouts", "British", [
    ("1899-12-01", "garrison", "Cape Town",
     "Montmorency's Scouts raised by Captain the Honourable R. de Montmorency VC (21st Lancers) in December 1899, strength ~100. The corps operated in the eastern Cape and was among the first troops to enter Pretoria.",
     "", "Capt Hon. R. de Montmorency VC"),
    ("1900-02-23", "engagement", "Stormberg",
     "Captain de Montmorency killed in a skirmish near Stormberg, 23 February 1900. Command passed to Capt McNeill of the Seaforth Highlanders (formerly ADC to Gen Gatacre). The scouts remained effective under new leadership.",
     "", "Capt McNeill"),
    ("1900-06-05", "redeployment", "Pretoria",
     "Montmorency's Scouts were among the first troops to gallop into Pretoria, 5 June 1900. After occupation the unit was split up and disbanded.",
     "", "Capt McNeill"),
])

unit("Namaqualand Border Scouts", "British", [
    ("1901-06-01", "garrison", "Upington",
     "Namaqualand Border Scouts raised to patrol the remote Namaqualand-Orange River border against Boer incursions from German South-West Africa direction. Records held in TNA WO126.",
     "", ""),
    ("1902-05-31", "garrison", "Upington",
     "Namaqualand Border Scouts stood down following the Peace of Vereeniging.",
     "", ""),
])

unit("Pietersburg Light Horse", "British", [
    ("1901-03-01", "garrison", "Pietersburg",
     "Pietersburg Light Horse raised in the northern Transvaal (Pietersburg / Polokwane area) following its occupation in April 1901. Associated with but distinct from the Bush Veldt Carbineers; both served in the northern Tvl counter-insurgency.",
     "", ""),
    ("1902-05-31", "garrison", "Pietersburg",
     "Pietersburg Light Horse stood down following the Peace of Vereeniging.",
     "", ""),
])

unit("Warren's Mounted Infantry", "British", [
    ("1900-01-01", "garrison", "Durban",
     "Warren's Mounted Infantry raised under General Sir Charles Warren for operations in Natal and Griqualand. Served during the Spion Kop operations and the subsequent Natal campaign.",
     "", "Gen Sir Charles Warren"),
    ("1900-01-24", "engagement", "Durban",
     "Warren's Mounted Infantry served during the Spion Kop operations (Jan 1900) as part of Warren's 5th Division force.",
     "", "Gen Sir Charles Warren"),
])

unit("Warwick's Horse", "British", [
    ("1901-06-01", "garrison", "Cape Town",
     "Warwick's Horse raised in the Cape Colony as part of the locally-recruited mounted forces during the guerrilla phase. Records held at TNA WO126 (nominal roll).",
     "", ""),
    ("1902-05-31", "garrison", "Cape Town",
     "Warwick's Horse stood down following the Peace of Vereeniging.",
     "", ""),
])

# ── SCOUT UNITS ────────────────────────────────────────────────────────────────

unit("Erroll's Scouts", "British", [
    ("1901-06-01", "garrison", "Cape Town",
     "Erroll's Scouts raised in the Cape Colony as a locally-recruited scout and intelligence unit during the guerrilla phase. TNA WO126 nominal roll.",
     "", ""),
    ("1902-05-31", "garrison", "Cape Town",
     "Erroll's Scouts stood down following the Peace of Vereeniging.",
     "", ""),
])

unit("Fraserburg Scouts", "British", [
    ("1901-06-01", "garrison", "Fraserburg",
     "Fraserburg Scouts raised in Fraserburg, Karoo district of the Cape Colony. The Duke of Edinburgh's Own Volunteer Rifles had 98 men stationed at Fraserburg early in the war; the Fraserburg Scouts were a locally-raised continuation/successor for district patrol during the guerrilla phase.",
     "", ""),
    ("1902-05-31", "garrison", "Fraserburg",
     "Fraserburg Scouts stood down following the Peace of Vereeniging.",
     "", ""),
])

unit("Geoghegan's Scouts", "British", [
    ("1901-06-01", "garrison", "Cape Town",
     "Geoghegan's Scouts raised in the Cape Colony as a mounted scout and intelligence unit. Records held at TNA WO126 (nominal roll).",
     "", ""),
    ("1902-05-31", "garrison", "Cape Town",
     "Geoghegan's Scouts stood down following the Peace of Vereeniging.",
     "", ""),
])

# ── OTHER LOCAL UNITS ──────────────────────────────────────────────────────────

unit("Herschel Native Police", "British", [
    ("1901-01-01", "garrison", "Herschel",
     "Herschel Native Police raised in the Herschel district (northeastern Cape Colony, bordering Basutoland) to maintain order, prevent rebel recruitment, and protect loyalist civilians from Boer raiding columns. TNA WO126 nominal roll.",
     "", ""),
    ("1902-05-31", "garrison", "Herschel",
     "Herschel Native Police stood down following the Peace of Vereeniging.",
     "", ""),
])

unit("Protectorate Regiment", "British", [
    ("1899-10-12", "garrison", "Mafeking",
     "Protectorate Regiment (also Bechuanaland Protectorate Regiment) raised from settlers in the Bechuanaland Protectorate. Formed the core professional force at Mafeking alongside the Bechuanaland Rifles and Mafeking Town Guard during the 217-day siege under Baden-Powell.",
     "", "Lt Col Hore"),
    ("1900-05-17", "redeployment", "Mafeking",
     "Protectorate Regiment stood down siege duties following relief of Mafeking, 17 May 1900. Many men subsequently joined other colonial corps.",
     "", ""),
])

unit("Zululand Scouts", "British", [
    ("1901-03-01", "garrison", "Vryheid",
     "Zululand Scouts raised in Zululand/northern Natal for mounted patrol and intelligence in the border zone between Natal and the southern Transvaal. TNA WO126 nominal roll.",
     "", ""),
    ("1902-05-31", "garrison", "Vryheid",
     "Zululand Scouts stood down following the Peace of Vereeniging.",
     "", ""),
])

# ── WRITE ─────────────────────────────────────────────────────────────────────
print("New rows: %d  (IDs %d-%d)" % (len(new_rows), max_id + 1, nid[0] - 1))
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
        before, after = bp[:marker_end], bp[marker_end + 1:]
    else:
        cp = bp.find('\n}', marker_end)
        before, after = bp[:cp + 1], bp[cp + 2:]
    new_bp = before + '\n'.join(a_entries) + '\n}' + after
    open(BUILD_MAP, "w", encoding="utf-8").write(new_bp)
    print("A dict entries injected: %d" % len(a_entries))
else:
    print("ERROR: no injection point")
