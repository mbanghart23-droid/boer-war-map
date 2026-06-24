"""
Add all named Town Guard (TG) and District Mounted Troop (DMT) units confirmed
on angloboerwar.com for the Cape Colony and Natal, 1899-1902.

Each unit gets:
  - Formation/activation event
  - Main garrison/patrol event
  - End-of-war stand-down (May 1902)

Sources: angloboerwar.com unit pages; SAMHS vol102rt (TG forts eastern Cape);
         SAMHS vol073vm (Graaff-Reinet); Pakenham 'The Boer War'
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
def nxt(): i = nid[0]; nid[0] += 1; return str(i)

SRC = "angloboerwar.com unit pages; SAMHS vol102rt; Pakenham 'The Boer War'"
LOW = "low"
NOTE = "Auto-generated from angloboerwar.com TG/DMT roster (add_tg_dmt.py); verify against unit roll"

new_rows = []
a_entries = []

def region_of(place):
    NORTH = {"Kimberley","Mafeking","Warrenton","Christiana","Zeerust","Cape Town",
              "Hopefield","Wellington","Houw Hoek","Green River"}
    return "north" if place in NORTH else "eastern"

def add(force, side, date_start, event_type, action_place, description,
        from_place="", to_place="", date_end="", commander=""):
    rid = nxt()
    fp = from_place or ""
    tp = to_place or action_place
    new_rows.append({
        "id": rid, "side": side, "force": force,
        "commander": commander, "units": force,
        "date_start": date_start, "date_end": date_end,
        "event_type": event_type,
        "from_place": fp, "to_place": tp, "action_place": action_place,
        "description": description,
        "confidence": LOW, "source": SRC, "note": NOTE,
    })
    reg = region_of(action_place)
    if fp and fp != action_place:
        a_entries.append(' "%s": dict(pt="%s", line=(%r, %r), region="%s"),' % (
            rid, action_place, fp, action_place, reg))
    else:
        a_entries.append(' "%s": dict(pt="%s", region="%s"),' % (rid, action_place, reg))

def tg(name, town, formed, note_extra="", special_events=None):
    """Add a Town Guard unit with standard formation + garrison + stand-down."""
    desc_form = ("%s formed to defend the town of %s against Boer incursion during "
                 "the Cape Colony guerrilla phase. %s" % (name, town, note_extra)).strip()
    add(name, "British", formed, "garrison", town, desc_form)

    if special_events:
        for ev_date, ev_type, ev_desc in special_events:
            add(name, "British", ev_date, ev_type, town, ev_desc)

    # Stand-down / end of war
    add(name, "British", "1902-05-31", "garrison", town,
        "%s stood down following the Peace of Vereeniging (31 May 1902), ending the Anglo-Boer War." % name)

def dmt(name, town, formed, note_extra="", patrol_towns=None):
    """Add a DMT unit with formation + patrols + stand-down."""
    desc_form = ("%s raised as a mobile mounted unit for district patrolling and "
                 "intelligence support to imperial columns in the %s district. %s" % (
                     name, town, note_extra)).strip()
    add(name, "British", formed, "garrison", town, desc_form)

    if patrol_towns:
        for pt_date, pt_town, pt_desc in patrol_towns:
            add(name, "British", pt_date, "redeployment", pt_town, pt_desc,
                from_place=town, to_place=pt_town)
            town = pt_town  # chain from last position

    add(name, "British", "1902-06-30", "garrison", town,
        "%s stood down following the Peace of Vereeniging and completion of pacification operations." % name)

# ── TOWN GUARDS ────────────────────────────────────────────────────────────────

# Eastern Cape - war theatre
tg("Aberdeen Town Guard", "Aberdeen", "1901-01-01",
   "The Aberdeen TG repulsed a Boer attack by Scheepers and Fouche on 6 March 1901.",
   [("1901-03-06", "engagement",
     "Aberdeen Town Guard successfully repulsed an attack by Scheepers and Fouche's commandos on 6 March 1901. The fort held against the Boer assault. (SAMHS vol073vm)")])

tg("Aliwal North Town Guard", "Aliwal North", "1900-11-01",
   "Aliwal North was a key crossing on the Orange River and the TG was vital to preventing Boer raids into the Cape.")

tg("Alicedale Town Guard", "Alicedale", "1901-01-01",
   "Alicedale, on the railway between Grahamstown and Port Elizabeth, maintained a TG to protect the line.")

tg("Alexandria Town Guard", "Alexandria", "1901-01-01",
   "Alexandria Town Guard raised for local defence in the eastern Cape.")

tg("Barkly East Town Guard", "Barkly East", "1901-01-01",
   "Barkly East was briefly occupied by Boers after Stormberg; the TG was formed to prevent recurrence.")

tg("Burghersdorp Town Guard", "Burghersdorp", "1900-11-01",
   "Burghersdorp was briefly occupied by Boers in late 1899; the TG was formed after evacuation to guard against return.")

tg("Cathcart Town Guard", "Cathcart", "1901-01-01",
   "Cathcart, on the road between Queenstown and King William's Town, maintained observation posts and a town guard.")

tg("Cradock Town Guard", "Cradock", "1901-01-01",
   "The Cradock TG was active during Kritzinger's raids in the midland Cape district.",
   [("1902-01-15", "engagement",
     "50 men of the Cradock Town Guard were captured by Cmdt Louis Wessels's commando during Kritzinger's winter raids, January 1902.")])

tg("Dordrecht Town Guard", "Dordrecht", "1901-01-01",
   "Dordrecht, north-east of Sterkstroom, was briefly occupied by Boers and the TG formed for subsequent defence.",
   [("1901-05-01", "engagement",
     "Dordrecht Town Guard engaged in defence of the town during Lötter's commando incursion into the northeastern Cape.")])

tg("East London Town Guard", "East London", "1901-01-01",
   "East London Town Guard formed to protect the port city and Cape Government Railway terminus.")

tg("Graaff-Reinet Town Guard", "Graaff-Reinet", "1901-01-01",
   "Graaff-Reinet TG grew from 100 men (Jan 1901) to 220 by March 1902 under Cmdt J. Gardner. The unit maintained order and supported column operations. (SAMHS vol073vm)",
   [("1901-06-01", "garrison",
     "Graaff-Reinet Town Guard expanded to over 150 men by mid-1901, garrisoning the fort and providing scouts to British columns operating in the district.")])

tg("Grahamstown Town Guard", "Grahamstown", "1901-01-01",
   "Grahamstown, as the regional centre of the eastern Cape, maintained a significant TG alongside the First City (Grahamstown) Volunteers.")

tg("Hanover Town Guard", "Hanover", "1901-01-01",
   "Hanover Town Guard formed in the Karoo to protect the railway junction and surrounding district.")

tg("Indwe Town Guard", "Indwe", "1901-01-01",
   "Indwe, site of important coal mines, maintained a town guard to protect the colliery and railway.")

tg("Jansenville Town Guard", "Jansenville", "1901-01-01",
   "Jansenville TG under Capt Gould built a fort in Jan 1901. Smuts's commando bypassed the town in Nov 1901 due to its strong fortifications. (angloboerwar.com; SAMHS vol102rt)")

tg("Kimberley Town Guard", "Kimberley", "1899-10-14",
   "Kimberley Town Guard formed at outbreak of war from De Beers employees and local volunteers under Col Kekewich; central to the 217-day siege (Oct 1899 – Feb 1900).",
   [("1899-10-14", "garrison",
     "Kimberley Town Guard mobilised as the Boer siege began. Approximately 500 men of the TG and colonial forces held the town alongside regulars under Col Kekewich."),
    ("1900-02-15", "garrison",
     "Kimberley relieved by French's cavalry (15 Feb 1900); the Town Guard handed defensive duties back to imperial forces.")])

tg("King William's Town Town Guard", "King William's Town", "1901-01-01",
   "King William's Town, headquarters of Cape Colony eastern command, maintained a substantial TG alongside the Kaffrarian Rifles.")

tg("Knysna Town Guard", "Knysna", "1901-01-01",
   "Knysna TG grew from ~70 to 167 men by end of war, including a mounted troop. Garrisoned Fort Verdompskop above the town. (SAMHS vol102rt)")

tg("Komgha Town Guard", "Komgha", "1901-01-01",
   "Komgha, on the Kei River border, maintained a town guard against Boer raiders crossing from the Transkei frontier.")

tg("Lady Grey Town Guard", "Lady Grey", "1901-01-01",
   "Lady Grey Town Guard formed in the northeastern Cape to protect the mountain pass town from Boer raids from Basutoland direction.")

tg("Mafeking Town Guard", "Mafeking", "1899-10-12",
   "Mafeking Town Guard, ~200 civic volunteers under Baden-Powell, contributed to the defence during the 217-day siege (Oct 1899 – May 1900).",
   [("1900-05-17", "garrison",
     "Mafeking relieved by Mahon's column (17 May 1900); the Mafeking Town Guard had held for 217 days.")])

tg("Middelburg (Cape) Town Guard", "Middelburg (Cape)", "1901-01-01",
   "Middelburg (Cape) Town Guard formed as Boer commandos under Kritzinger raided the Midland Cape districts.")

tg("Molteno Town Guard", "Molteno", "1901-01-01",
   "Molteno, near the Stormberg battle site, maintained a town guard after Boer forces withdrew from the area.",
   [("1901-09-05", "engagement",
     "Molteno Town Guard in action during the Groenkloof operation (Sep 1901) as Lötter's commando was intercepted nearby.")])

tg("Murraysburg Town Guard", "Murraysburg", "1901-01-01",
   "Murraysburg Town Guard formed in the Karoo during the guerrilla phase as Boer commandos ranged through the Cape Colony.")

tg("Naauwpoort Town Guard", "Naauwpoort", "1901-01-01",
   "Naauwpoort, a major railway junction, maintained a town guard to protect the rail infrastructure.")

tg("Pearston Town Guard", "Pearston", "1901-01-01",
   "Pearston Town Guard overwhelmed when Kritzinger surrounded and looted the village, 3-6 March 1901.",
   [("1901-03-03", "engagement",
     "Pearston Town Guard was overwhelmed when Kritzinger's commando surrounded and looted Pearston, 3-6 March 1901. The TG was unable to mount effective resistance.")])

tg("Port Elizabeth Town Guard", "Port Elizabeth", "1900-02-01",
   "Port Elizabeth TG formed in February 1900 and expanded with additional battalion and mounted company in January 1901. ~518 strong; guarded the principal port and waterworks.")

tg("Queenstown Town Guard", "Queenstown", "1899-12-11",
   "Queenstown TG formed after British forces retreated from Stormberg, when Queenstown became the forward base for the 3rd Division.")

tg("Richmond Town Guard", "Richmond", "1901-01-01",
   "Richmond Town Guard formed in the Karoo during the guerrilla phase.")

tg("Somerset East Town Guard", "Somerset East", "1901-01-01",
   "Somerset East Town Guard formed as Jan Smuts's raid threatened the Midlands district in September 1901.")

tg("Steynsburg Town Guard", "Steynsburg", "1901-01-01",
   "Steynsburg Town Guard formed near the OFS border to resist Boer commando incursions.")

tg("Sterkstroom Town Guard", "Sterkstroom", "1899-12-01",
   "Sterkstroom, the fallback position after Stormberg, served as a base for the 3rd Division and maintained a strong town guard throughout.")

tg("Tarkastad Town Guard", "Tarkastad", "1901-01-01",
   "Tarkastad, a known centre of Cape rebel sympathy, maintained a loyal TG; there were multiple engagements with Boer forces in the district in 1901-02.")

tg("Uitenhage Town Guard", "Uitenhage", "1901-01-01",
   "Uitenhage Town Guard formed to protect the railway workshop town between Port Elizabeth and Cradock.")

tg("Venterstad Town Guard", "Venterstad", "1901-01-01",
   "Venterstad Town Guard formed near the OFS border on the Aliwal North-Colesberg road.")

tg("Warrenton Town Guard", "Warrenton", "1901-01-01",
   "Warrenton Town Guard formed on the Vaal River to protect the railway bridge and river crossing.")

tg("Willowmore Town Guard", "Willowmore", "1901-01-01",
   "Willowmore TG suffered six killed when Scheepers attacked the village on 1 June 1901. (SAMHS vol185gs)",
   [("1901-01-01", "engagement",
     "Willowmore Town Guard repulsed Scheepers's first attack in January 1901."),
    ("1901-06-01", "engagement",
     "Willowmore Town Guard attacked by Scheepers's commando; six defenders killed. One of the most serious TG actions in the eastern Cape. (SAMHS vol185gs)")])

tg("Zeerust Town Guard", "Zeerust", "1901-01-01",
   "Zeerust Town Guard formed in the western Transvaal to maintain local order during the guerrilla phase.")

tg("Cape Town Town Guard", "Cape Town", "1901-01-01",
   "Cape Town Town Guard raised to provide local security in the capital as imperial forces were deployed north.")

# ── DISTRICT MOUNTED TROOPS ────────────────────────────────────────────────────

dmt("Aberdeen District Mounted Troops", "Aberdeen", "1901-06-01",
    "The Aberdeen DMT (~100 men) provided local knowledge and scouting for imperial columns in the Graaff-Reinet district. (angloboerwar.com/dmt/3075-aberdeen-dmt)")

dmt("Albany District Mounted Troops", "Grahamstown", "1901-08-01",
    "Albany DMT, named for Albany district of the eastern Cape, provided mounted scouts and intelligence for columns operating out of Grahamstown.")

dmt("Aliwal North District Mounted Troops", "Aliwal North", "1901-08-04",
    "Aliwal North DMT active from 4 Aug 1901 to 30 Jun 1902. Engaged Boers at De Kraal 8 Jun 1901 and at Kemmelkspruit 27 Apr 1902 where 6 prisoners were taken. (angloboerwar.com/dmt/2491-aliwalnorthdmt)",
    patrol_towns=[
        ("1901-10-01", "Aliwal North", "Aliwal North DMT continued mounted patrol operations along the Orange River line."),
        ("1902-04-27", "Aliwal North", "Aliwal North DMT engaged Boers at Kemmelkspruit, taking 6 prisoners. (angloboerwar.com)")
    ])

dmt("Beaufort West District Mounted Troops", "Beaufort West", "1901-08-01",
    "Beaufort West DMT provided mounted patrol in the Karoo against Boer raiders threatening the railway.")

dmt("Bedford District Mounted Troops", "Bedford", "1901-08-01",
    "Bedford DMT provided local intelligence and patrol support in the Bedford district east of Cradock.")

dmt("Burghersdorp District Mounted Troops", "Burghersdorp", "1901-08-01",
    "Burghersdorp DMT operated along the OFS-Cape border, supporting columns against Kritzinger and Lötter commandos.")

dmt("Christiana District Mounted Rifles", "Christiana", "1901-06-01",
    "Christiana District Mounted Rifles, raised in Griqualand West, patrolled the Vaal River district and screened against western Transvaal raiding commandos.")

dmt("Cradock District Mounted Troops", "Cradock", "1901-08-01",
    "Cradock DMT provided local mounted intelligence during Kritzinger's sustained operations in the Cradock-Middelburg zone in 1901-02.")

dmt("Graaff-Reinet District Mounted Troops", "Graaff-Reinet", "1901-06-01",
    "Graaff-Reinet DMT never exceeded 100 men but provided valuable intelligence and scouting for imperial columns. (angloboerwar.com; SAMHS vol073vm)")

dmt("Green River District Mounted Troops", "Green River", "1901-08-01",
    "Green River DMT served in the western Cape coastal districts, protecting the Garden Route towns.")

dmt("Hopefield District Mounted Troops", "Hopefield", "1901-08-01",
    "Hopefield DMT patrolled the western Cape and Swartland district north of Cape Town.")

dmt("Houw Hoek District Mounted Troops", "Houw Hoek", "1901-08-01",
    "Houw Hoek DMT served in the Overberg district, patrolling the passes through the Hottentots Holland mountains.")

dmt("Jansenville District Mounted Troops", "Jansenville", "1901-08-01",
    "Jansenville DMT (linked with Nesbitt's Horse) helped capture Cmdt Wynand Malan near Sheldon on 27 May 1902. (angloboerwar.com)")

dmt("Middelburg District Mounted Troops", "Middelburg (Cape)", "1901-08-01",
    "Middelburg DMT provided mounted scouting and patrol support during Kritzinger and Scheepers's operations in the Karoo districts.")

dmt("Mossel Bay District Mounted Troops", "Mossel Bay", "1901-08-01",
    "Mossel Bay DMT patrolled the Garden Route coastal district against scattered Boer incursions.")

dmt("Naauwpoort District Mounted Troops", "Naauwpoort", "1901-08-01",
    "Naauwpoort DMT patrolled the railway junction zone and screened against commandos raiding south of the OFS border.")

dmt("Queenstown District Mounted Troops", "Queenstown", "1901-08-01",
    "Queenstown DMT provided mounted intelligence and patrol in the northeastern Cape districts threatened by Lötter and Wessels.")

dmt("Somerset East District Mounted Troops", "Somerset East", "1901-08-01",
    "Somerset East DMT: approximately 180 men surrendered to Smuts's commando near Somerset East, October 1901 — a notable Boer success in the Cape guerrilla war. (angloboerwar.com/dmt/2625-somerseteastdmt)")

dmt("Steytleville District Mounted Troops", "Steytleville", "1901-08-01",
    "Steytleville DMT served in the district between Graaff-Reinet and Murraysburg.")

dmt("Stockenstrom District Mounted Troops", "Stockenstrom", "1901-08-01",
    "Stockenstrom DMT (named for the Stockenstrom district around Sterkstroom) patrolled the northeastern Cape between Queenstown and Aliwal North.")

dmt("Sutherland District Mounted Troops", "Sutherland", "1901-08-01",
    "Sutherland DMT served in the remote Roggeveld mountains, patrolling against Boer raiders threatening the Karoo interior.")

dmt("Tarkastad District Mounted Troops", "Tarkastad", "1901-08-01",
    "Tarkastad Mounted Troops in action near Vaal Vlei, 8 Oct 1901, under Maj H.T. Nickalls (17th Lancers, attached). (angloboerwar.com)")

dmt("Victoria East District Mounted Troops", "Victoria East", "1901-08-01",
    "Victoria East DMT served in the district around Alice and Fort Beaufort, eastern Cape.")

dmt("Wellington District Mounted Troops", "Wellington", "1901-08-01",
    "Wellington DMT patrolled the Boland district of the western Cape.")

# ── WRITE CSV ─────────────────────────────────────────────────────────────────
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
        before, after = bp[:marker_end], bp[marker_end + 1:]
    else:
        cp = bp.find('\n}', marker_end)
        before, after = bp[:cp + 1], bp[cp + 2:]
    new_bp = before + '\n'.join(a_entries) + '\n}' + after
    open(BUILD_MAP, "w", encoding="utf-8").write(new_bp)
    print("A dict entries injected: %d" % len(a_entries))
else:
    print("ERROR: no injection point")
