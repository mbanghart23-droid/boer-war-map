"""
Add 20 units found on angloboerwar.com but absent from movements.csv:
Infantry: Cameron Highlanders, Cheshire, Leinster, Lincolnshire, Norfolk,
          Royal Berkshire, Royal Lancaster, South Staffordshire, South Wales Borderers
SA/Colonial: Buffalo Volunteer Rifles, Cape Mounted Police, Morley's Scouts,
             Natal Mounted Infantry, Natal Volunteer Medical Corps,
             Rhodesian Volunteers, Transkei Mounted Rifles
BSAC/Rhodesia: Afrikander Corps, Bulawayo Field Force, Pioneer Corps,
               Rhodesia Horse Volunteers

Sources: angloboerwar.com unit pages; Conan Doyle 'The Great Boer War';
         boer-war.com/Military/British/TroopArrivals
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

SRC = "angloboerwar.com; Conan Doyle 'The Great Boer War'; boer-war.com TroopArrivals"
NOTE = "Auto-generated from angloboerwar.com unit audit (add_missing_abw.py); verify against unit history"
LOW = "low"

new_rows = []
a_entries = []

def add(force, side, date_start, event_type, action_place, description,
        from_place="", to_place="", date_end="", commander=""):
    rid = nxt()
    tp = to_place or action_place
    new_rows.append({
        "id": rid, "side": side, "force": force,
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

# ── INFANTRY ───────────────────────────────────────────────────────────────────

# Cameron Highlanders — from Egypt, arrived ~23 Mar 1900; 21st Brigade (Bruce Hamilton)
# with 1st Sussex, 1st Derbyshire, CIV; Ian Hamilton's right-flank force;
# Vredefort Road Jun 1900; Spitz Kop Jul 1900 (~20 cas); Jan 1901 to Pretoria then Tvl columns
F = "1st Cameron Highlanders (Queen's Own)"
add(F, "British", "1900-03-23", "disembark", "Cape Town",
    "1st Cameron Highlanders (Queen's Own) arrived South Africa ~23 March 1900, having sailed from Egypt 3 March. Joined 21st Brigade (Maj Gen Bruce Hamilton) alongside 1st Sussex, 1st Derbyshire, and City Imperial Volunteers, under Lt Gen Ian Hamilton's right-flank column.",
    commander="")
add(F, "British", "1900-04-15", "redeployment", "Bloemfontein",
    "Camerons joined Roberts's main advance into the OFS as part of Ian Hamilton's right-flank force.",
    from_place="Cape Town")
add(F, "British", "1900-06-07", "engagement", "Bloemfontein",
    "Cameron Highlanders' mounted infantry company engaged near Vredefort Road, 7 June 1900, in the OFS operations.",
    from_place="Bloemfontein")
add(F, "British", "1900-07-21", "engagement", "Pretoria",
    "21st Brigade (incl. Camerons) captured strongly-held position at Spitz Kop / Spitz Ray, 21 July 1900, during Hunter's operations against Prinsloo in the OFS; ~20 casualties (3 fatal). Further fighting at Stephenusdrai, 29 July.",
    from_place="Bloemfontein")
add(F, "British", "1901-01-01", "redeployment", "Pretoria",
    "Camerons left Bruce Hamilton's command Jan 1901, transferred to Pretoria, then operated in various Transvaal columns throughout 1901-02. 13 officers and 19 NCOs/men mentioned in Roberts's final despatch.",
    from_place="Bloemfontein")

# Cheshire Regiment — 2nd Bn; 15th Brigade (Wavell) with SWB, 1st E Lancs, 2nd N Staffs;
# 7th Division (Tucker); Roberts's advance; arrived ~3 Feb 1900
F = "2nd Cheshire Regiment"
add(F, "British", "1900-02-03", "disembark", "Cape Town",
    "2nd Cheshire Regiment arrived Cape Colony ~3 February 1900 (sailed with South Wales Borderers on SS Bavarian, ~18 Jan 1900). Assigned to 15th Brigade (Maj Gen A G Wavell) alongside 2nd South Wales Borderers, 1st East Lancashire, and 2nd North Staffordshire, forming part of 7th Division under Lt Gen Tucker.",
    commander="")
add(F, "British", "1900-04-01", "redeployment", "Bloemfontein",
    "2nd Cheshire Regiment advanced into the OFS with Tucker's 7th Division as part of Roberts's main army.",
    from_place="Cape Town")
add(F, "British", "1900-06-01", "redeployment", "Pretoria",
    "2nd Cheshire Regiment continued north with Roberts's main advance to Pretoria and into the guerrilla phase.",
    from_place="Bloemfontein")

# Leinster Regiment — service in SA; multiple battalions
F = "Leinster Regiment (Prince of Wales's)"
add(F, "British", "1900-01-15", "disembark", "Cape Town",
    "Leinster Regiment (Prince of Wales's) deployed to South Africa in early 1900. Served in various garrison and column operations. Records at angloboerwar.com unit-information/imperial-units/569-leinster-regiment.",
    commander="")
add(F, "British", "1900-05-01", "redeployment", "Bloemfontein",
    "Leinster Regiment served in column and line-of-communication duties during the guerrilla phase in the OFS and Tvl.",
    from_place="Cape Town")

# Lincolnshire Regiment — 2nd Bn; sailed 4 Jan 1900 on Goorkha, arrived Cape ~25 Jan;
# 14th Brigade (Chermside) with 2nd Norfolk, 1st KOSB, 2nd Hampshire; 7th Division (Tucker)
F = "2nd Lincolnshire Regiment"
add(F, "British", "1900-01-25", "disembark", "Cape Town",
    "2nd Lincolnshire Regiment arrived Cape Colony ~25 January 1900, having sailed on SS Goorkha ~4 January. Assigned to 14th Brigade (Brig Gen Chermside) alongside 2nd Norfolk, 1st KOSB (King's Own Scottish Borderers), and 2nd Hampshire, forming part of 7th Division under Lt Gen Tucker.",
    commander="")
add(F, "British", "1900-04-01", "redeployment", "Bloemfontein",
    "2nd Lincolnshire Regiment advanced into the OFS with Tucker's 7th Division.",
    from_place="Cape Town")
add(F, "British", "1900-06-01", "redeployment", "Pretoria",
    "2nd Lincolnshire Regiment continued north with the main advance to Pretoria and into guerrilla-phase column work.",
    from_place="Bloemfontein")

# Norfolk Regiment — 2nd Bn; 14th Brigade (Chermside) with 2nd Lincolnshire, 1st KOSB, 2nd Hampshire
F = "2nd Norfolk Regiment"
add(F, "British", "1900-01-25", "disembark", "Cape Town",
    "2nd Norfolk Regiment arrived Cape Colony late January 1900. Assigned to 14th Brigade (Brig Gen Chermside) alongside 2nd Lincolnshire, 1st KOSB, and 2nd Hampshire — 7th Division (Tucker). Served in Roberts's advance and subsequent column operations.",
    commander="")
add(F, "British", "1900-04-01", "redeployment", "Bloemfontein",
    "2nd Norfolk Regiment advanced into the OFS with Tucker's 7th Division.",
    from_place="Cape Town")
add(F, "British", "1900-06-01", "redeployment", "Pretoria",
    "2nd Norfolk Regiment continued north to Pretoria and guerrilla-phase column duties.",
    from_place="Bloemfontein")

# Royal Berkshire Regiment — 2nd Bn; arrived later ~Jun 1900
F = "2nd Royal Berkshire Regiment (Princess Charlotte of Wales's)"
add(F, "British", "1900-06-01", "disembark", "Cape Town",
    "2nd Royal Berkshire Regiment (Princess Charlotte of Wales's) arrived South Africa June 1900 (Maj G de L Faunce commanding). Deployed during the guerrilla phase for garrison and column duties.",
    commander="Maj G de L Faunce")
add(F, "British", "1900-09-01", "redeployment", "Pretoria",
    "2nd Royal Berkshire Regiment deployed on column and garrison duties in the Tvl during the guerrilla phase.",
    from_place="Cape Town")

# Royal Lancaster Regiment (King's Own) — service in SA
F = "Royal Lancaster Regiment (King's Own)"
add(F, "British", "1900-01-01", "disembark", "Cape Town",
    "Royal Lancaster Regiment (King's Own) deployed to South Africa in early 1900. Served in column and garrison operations during Roberts's advance and the guerrilla phase.",
    commander="")
add(F, "British", "1900-06-01", "redeployment", "Pretoria",
    "Royal Lancaster Regiment (King's Own) serving in column duties in the Tvl and OFS during the guerrilla phase.",
    from_place="Cape Town")

# South Staffordshire Regiment — service in SA
F = "South Staffordshire Regiment"
add(F, "British", "1900-02-01", "disembark", "Cape Town",
    "South Staffordshire Regiment deployed to South Africa in early 1900. Served in garrison and mobile column operations during Roberts's advance and the guerrilla phase.",
    commander="")
add(F, "British", "1900-06-01", "redeployment", "Pretoria",
    "South Staffordshire Regiment serving in column and garrison duties in the Tvl during the guerrilla phase.",
    from_place="Cape Town")

# South Wales Borderers — 2nd Bn; sailed 18 Jan 1900 on Bavarian, arrived 3 Feb;
# 15th Brigade (Wavell) same as Cheshire; 7th Division (Tucker)
F = "2nd South Wales Borderers"
add(F, "British", "1900-02-03", "disembark", "Cape Town",
    "2nd South Wales Borderers arrived Cape Colony ~3 February 1900, having sailed on SS Bavarian ~18 January 1900. Assigned to 15th Brigade (Maj Gen A G Wavell) alongside 2nd Cheshire, 1st East Lancashire, and 2nd North Staffordshire — 7th Division (Tucker). Regiment of Rorke's Drift (1879) fame.",
    commander="")
add(F, "British", "1900-04-01", "redeployment", "Bloemfontein",
    "2nd South Wales Borderers advanced into the OFS with Tucker's 7th Division as part of Roberts's main army.",
    from_place="Cape Town")
add(F, "British", "1900-06-01", "redeployment", "Pretoria",
    "2nd South Wales Borderers continued north with Roberts's advance and served in guerrilla-phase column work.",
    from_place="Bloemfontein")

# ── SOUTH AFRICAN / COLONIAL ──────────────────────────────────────────────────

# Buffalo Volunteer Rifles — King William's Town / Buffalo River area, eastern Cape
F = "Buffalo Volunteer Rifles and Levy"
add(F, "British", "1899-10-12", "garrison", "King William's Town",
    "Buffalo Volunteer Rifles and Levy raised in the Buffalo River / King William's Town district for frontier defence of the eastern Cape Colony against Boer incursions and rebel activity.",
    commander="")
add(F, "British", "1902-05-31", "garrison", "King William's Town",
    "Buffalo Volunteer Rifles stood down following the Peace of Vereeniging.",
    commander="")

# Cape Mounted Police — distinct from Cape Police; frontier/rural policing
F = "Cape Mounted Police"
add(F, "British", "1899-10-12", "garrison", "Cape Town",
    "Cape Mounted Police mobilised at the outbreak of war. The force provided rural policing and frontier patrol throughout the Cape Colony, actively cooperating with British columns in the eastern and northern Cape during Boer raiding and the rebel phase.",
    commander="")
add(F, "British", "1901-06-01", "redeployment", "Graaff-Reinet",
    "Cape Mounted Police maintained district order and supported column operations in the eastern Cape during the guerrilla phase.",
    from_place="Cape Town")

# Morley's Scouts
F = "Morley's Scouts"
add(F, "British", "1901-01-01", "garrison", "Cape Town",
    "Morley's Scouts raised in the Cape Colony as a locally-recruited mounted scout and intelligence unit during the guerrilla phase. Records at angloboerwar.com south-african-units.",
    commander="")
add(F, "British", "1902-05-31", "garrison", "Cape Town",
    "Morley's Scouts stood down following the Peace of Vereeniging.")

# Natal Mounted Infantry
F = "Natal Mounted Infantry"
add(F, "British", "1899-10-12", "garrison", "Durban",
    "Natal Mounted Infantry mobilised at outbreak of war, forming part of the Natal Field Force. Served throughout the Natal campaign including Ladysmith operations, the advance to the Transvaal border, and subsequent column work in Natal and the southeastern Tvl.",
    commander="")
add(F, "British", "1900-06-01", "redeployment", "Durban",
    "Natal Mounted Infantry continued operations in Natal and the southeastern Transvaal during the guerrilla phase, cooperating with British columns.",
    from_place="Durban")

# Natal Volunteer Medical Corps
F = "Natal Volunteer Medical Corps"
add(F, "British", "1899-10-12", "garrison", "Durban",
    "Natal Volunteer Medical Corps mobilised at outbreak of war to provide medical support for the Natal Field Force. Served throughout the Natal campaign including the siege of Ladysmith.",
    commander="")

# Rhodesian Volunteers
F = "Rhodesian Volunteers"
add(F, "British", "1899-10-12", "garrison", "Bulawayo",
    "Rhodesian Volunteers raised in Rhodesia at the outbreak of war to defend against possible Boer incursion from the Transvaal and to contribute to operations in the northern Tvl. Associated with the British South Africa Company forces.",
    commander="")
add(F, "British", "1901-01-01", "redeployment", "Pietersburg",
    "Rhodesian Volunteers participated in operations in the northern Transvaal under Plumer's and Grenfell's columns.",
    from_place="Bulawayo")

# Transkei Mounted Rifles
F = "Transkei Mounted Rifles"
add(F, "British", "1901-01-01", "garrison", "King William's Town",
    "Transkei Mounted Rifles raised in the Transkei territories (eastern Cape / Pondoland border) to defend the loyalist population and support British operations against Boer raiding columns entering the Transkei region.",
    commander="")
add(F, "British", "1902-05-31", "garrison", "King William's Town",
    "Transkei Mounted Rifles stood down following the Peace of Vereeniging.")

# ── BSAC / RHODESIA ───────────────────────────────────────────────────────────

# Afrikander Corps — BSAC unit; Cape-Afrikaner loyalists or Rhodesian-based unit
F = "Afrikander Corps"
add(F, "British", "1900-01-01", "garrison", "Bulawayo",
    "Afrikander Corps raised by the British South Africa Company in Rhodesia/Bechuanaland area, recruited from Cape-Afrikaner settlers loyal to the Crown. Served in defensive and patrol roles during the northern Tvl campaign.",
    commander="")
add(F, "British", "1902-05-31", "garrison", "Bulawayo",
    "Afrikander Corps stood down following the Peace of Vereeniging.")

# Bulawayo Field Force — early-war Rhodesian defensive force
F = "Bulawayo Field Force"
add(F, "British", "1899-10-12", "garrison", "Bulawayo",
    "Bulawayo Field Force raised in Bulawayo, Rhodesia, at the outbreak of war to defend against possible Boer incursion from the northern Transvaal (Zoutpansberg/Swaziland direction). Comprised BSAC police, Rhodesian Volunteers, and local settlers.",
    commander="")
add(F, "British", "1900-03-01", "redeployment", "Bulawayo",
    "Bulawayo Field Force stood down as a distinct formation when the northern Tvl was occupied by British forces under Plumer/Grenfell and the defensive threat receded.")

# Pioneer Corps (BSAC/Rhodesia)
F = "Pioneer Corps (Rhodesia)"
add(F, "British", "1900-01-01", "garrison", "Bulawayo",
    "Pioneer Corps (Rhodesia) raised by the British South Africa Company for engineering, road-building, and pioneer duties in support of operations in Rhodesia and the northern Transvaal.",
    commander="")
add(F, "British", "1902-05-31", "garrison", "Bulawayo",
    "Pioneer Corps (Rhodesia) stood down following conclusion of the war.")

# Rhodesia Horse Volunteers
F = "Rhodesia Horse Volunteers"
add(F, "British", "1899-10-12", "garrison", "Bulawayo",
    "Rhodesia Horse Volunteers raised in Rhodesia as a cavalry/mounted volunteer force for British South Africa Company operations, providing mobile scouting and patrol capability in the Rhodesian-Transvaal border zone.",
    commander="")
add(F, "British", "1901-01-01", "redeployment", "Pietersburg",
    "Rhodesia Horse Volunteers participated in the northern Transvaal campaign under Plumer's column.",
    from_place="Bulawayo")
add(F, "British", "1902-05-31", "garrison", "Bulawayo",
    "Rhodesia Horse Volunteers stood down following the Peace of Vereeniging.")

# ── WRITE ─────────────────────────────────────────────────────────────────────
print("New rows: %d  (IDs %d-%d)" % (len(new_rows), max_id + 1, nid[0] - 1))
all_rows = rows + new_rows
with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(all_rows)
print("CSV written: %d rows, %d forces" % (
    len(all_rows), len(set(r["force"] for r in all_rows))))

bp = open(BUILD_MAP, encoding="utf-8").read()
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
    open(BUILD_MAP, "w", encoding="utf-8").write(
        before + '\n'.join(a_entries) + '\n}' + after)
    print("A dict entries injected: %d" % len(a_entries))
else:
    print("ERROR: no injection point")
