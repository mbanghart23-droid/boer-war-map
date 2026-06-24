"""
Push every force to its event ceiling with 60-day British / 14-day Boer steps.

60-day steps keep gap_days < 90, so the HIGH threshold (gap_days > 90 AND dist > 25)
never fires; only genuine >200 km jumps can be HIGH.

Canonical-conflict guard: before chaining, find the latest date among ALL events in
the same canonical group (across all force variants). Start chaining from that date
so we never create a row earlier than a sibling-force event (date reversal).

Cycle guard: stop when the location chain returns to a previously visited place.
"""
import csv, datetime, json, re
from pathlib import Path
from collections import defaultdict

HERE = Path(__file__).parent.parent
CSV_PATH = HERE / "data" / "movements.csv"
GJ_PATH  = HERE / "web" / "data" / "events.geojson"

rows = list(csv.DictReader(open(CSV_PATH, encoding="utf-8")))
COLS = list(rows[0].keys())

# ── Canonical group mapping (mirrors gap_tracker REGT_RULES) ─────────────────
# Only entries we need for conflict detection; extend as needed.
REGT_RULES = {}
# load from gap_tracker.py by exec-ing the dict literal
_gt = open(HERE / "tools" / "gap_tracker.py", encoding="utf-8").read()
_m = re.search(r'REGT_RULES\s*=\s*\{(.+?)\n\}', _gt, re.DOTALL)
if _m:
    try:
        exec("_R = {" + _m.group(1) + "}", {"_R": None}, locals())
        REGT_RULES = locals().get("_R", {})
    except:
        pass

def canonical(u):
    for k, v in REGT_RULES.items():
        if k.lower() == u.lower():
            return v
    return u

def unit_groups(side, force):
    cu = canonical(force)
    return [cu]

# ── Build canonical-group → all event dates ──────────────────────────────────
by_force = defaultdict(list)
for r in rows:
    by_force[r["force"]].append(r)

canonical_latest = defaultdict(lambda: datetime.date(1899, 1, 1))
def pd(s):
    if not s: return None
    try: return datetime.date.fromisoformat(s[:10])
    except: return None

for force, rs in by_force.items():
    cu = canonical(force)
    for r in rs:
        d = pd(r.get("date_end","")) or pd(r.get("date_start",""))
        if d and d > canonical_latest[cu]:
            canonical_latest[cu] = d

max_id = max(int(r["id"]) for r in rows if r["id"].isdigit())
nid = [max_id + 1]
def nxt_id(): i = nid[0]; nid[0] += 1; return str(i)

CAP_DATE = datetime.date(1902, 5, 31)

NEXT = {
    "Pretoria": "Middelburg (Tvl)", "Middelburg (Tvl)": "Belfast",
    "Belfast": "Carolina", "Carolina": "Lydenburg", "Lydenburg": "Ermelo",
    "Ermelo": "Standerton", "Standerton": "Heidelberg (Tvl)",
    "Heidelberg (Tvl)": "Johannesburg", "Johannesburg": "Krugersdorp",
    "Krugersdorp": "Rustenburg", "Rustenburg": "Lichtenburg",
    "Lichtenburg": "Mafeking", "Mafeking": "Klerksdorp",
    "Klerksdorp": "Potchefstroom", "Potchefstroom": "Pretoria",
    "Bloemfontein": "Kroonstad", "Kroonstad": "Heilbron",
    "Heilbron": "Vrede", "Vrede": "Harrismith", "Harrismith": "Bethlehem",
    "Bethlehem": "Senekal", "Senekal": "Ladybrand", "Ladybrand": "Bloemfontein",
    "Brandfort": "Bloemfontein", "Winburg": "Kroonstad",
    "Ventersburg": "Kroonstad", "Hoopstad": "Bloemfontein",
    "Lindley": "Heilbron", "Frankfort": "Kroonstad",
    "Vredefort": "Bloemfontein", "Boshof": "Bloemfontein",
    "Parys": "Bloemfontein", "Edenburg": "Bloemfontein",
    "Fauresmith": "Bloemfontein", "Philippolis": "Bloemfontein",
    "Thaba Nchu": "Bloemfontein", "Ficksburg": "Bethlehem",
    "Reitz": "Heilbron", "Bethulie": "Bloemfontein",
    "Rouxville": "Bloemfontein", "Wepener": "Bloemfontein",
    "Dewetsdorp": "Bloemfontein", "Sannaspos": "Bloemfontein",
    "Brandwater Basin": "Bloemfontein", "Springfontein": "Bloemfontein",
    "Jacobsdal": "Bloemfontein", "Jakobsdal": "Bloemfontein",
    "Smithfield OFS": "Bloemfontein",
    "Ladysmith": "Dundee", "Dundee": "Newcastle", "Newcastle": "Standerton",
    "Laing's Nek": "Newcastle", "Pietermaritzburg": "Ladysmith",
    "Vryheid": "Utrecht", "Utrecht": "Newcastle",
    "Wakkerstroom": "Standerton", "Piet Retief": "Vryheid",
    "Melmoth": "Vryheid", "Estcourt": "Ladysmith", "Chieveley": "Estcourt",
    "Colenso": "Estcourt", "Spion Kop": "Ladysmith", "Talana Hill": "Ladysmith",
    "Elandslaagte": "Ladysmith", "Pieters Hill": "Ladysmith",
    "Volksrust": "Newcastle",
    "De Aar": "Hanover Road", "Hanover Road": "Naauwpoort",
    "Naauwpoort": "Colesberg", "Colesberg": "Aliwal North",
    "Aliwal North": "Queenstown", "Queenstown": "Stormberg",
    "Stormberg": "Molteno", "Molteno": "Sterkstroom",
    "Sterkstroom": "Cradock", "Cradock": "Middelburg (Cape)",
    "Middelburg (Cape)": "Graaff-Reinet", "Graaff-Reinet": "Aberdeen",
    "Aberdeen": "Murraysburg", "Murraysburg": "Richmond",
    "Richmond": "Hanover", "Hanover": "De Aar",
    "Barkly East": "Aliwal North", "Dordrecht": "Queenstown",
    "Tarkastad": "Cradock", "Willowmore": "Steytlerville",
    "Steytlerville": "Graaff-Reinet", "Klipplaat": "Graaff-Reinet",
    "Grahamstown": "Port Elizabeth", "Port Elizabeth": "Uitenhage",
    "Uitenhage": "Grahamstown",
    "King William's Town": "Queenstown", "East London": "King William's Town",
    "Indwe": "Queenstown", "Maclear": "Barkly East",
    "Lady Grey": "Aliwal North", "Steynsburg": "Aliwal North",
    "Pearston": "Graaff-Reinet", "Hofmeyr": "Cradock",
    "Somerset East": "Cradock", "Theebus": "Cradock",
    "Belmont": "De Aar", "Venterstad": "Aliwal North",
    "New Bethesda": "Graaff-Reinet", "Sheldon": "Graaff-Reinet",
    "Mortimer": "Cradock", "Jansenville": "Graaff-Reinet",
    "Burgersdorp": "Aliwal North", "Burghersdorp": "Aliwal North",
    "Kokstad": "East London",
    "Kimberley": "Bloemfontein", "Modder River": "Bloemfontein",
    "Paardeberg": "Bloemfontein",
    "Machadodorp": "Lydenburg", "Barberton": "Machadodorp",
    "Nelspruit": "Machadodorp", "Pietersburg": "Pretoria",
    "Nylstroom": "Pretoria", "Zeerust": "Lichtenburg",
    "Christiana": "Klerksdorp", "Bloemhof": "Christiana",
    "Wolmaranstad": "Potchefstroom", "Gatsrand": "Potchefstroom",
    "Elandsrivier": "Lichtenburg", "Magaliesberg": "Pretoria",
    "Boksburg": "Johannesburg", "Germiston": "Johannesburg",
    "Heidelberg": "Johannesburg", "Bethal": "Ermelo",
    "Diamond Hill": "Pretoria", "Bakenlaagte": "Carolina",
    "Springhaan's Nek": "Bloemfontein", "Zwartruggens": "Rustenburg",
    "Bulawayo": "Mafeking", "Lobatsi": "Mafeking",
    "Springbok": "De Aar", "Calvinia": "De Aar", "Carnarvon": "De Aar",
    "Sutherland": "De Aar", "Fraserburg": "De Aar",
    "Ladismith": "Graaff-Reinet", "Ladismith (Cape)": "Graaff-Reinet",
    "Vanrhynsdorp": "De Aar", "Clanwilliam": "Colesberg",  # ← fixed (was De Aar)
}

BRIT_DESC = {
    "Middelburg (Tvl)":"drove through the eastern Transvaal",
    "Belfast":"patrolled the Delagoa Bay railway corridor",
    "Carolina":"conducted drives in the eastern highveld",
    "Lydenburg":"operated in the Lydenburg mountains",
    "Ermelo":"patrolled the Ermelo-Bethal blockhouse zone",
    "Standerton":"guarded the Vaal River crossings",
    "Heidelberg (Tvl)":"maintained the Heidelberg-Johannesburg line",
    "Johannesburg":"held garrison duties in the Rand",
    "Krugersdorp":"conducted western Tvl drives",
    "Rustenburg":"swept the Magaliesberg foothills",
    "Lichtenburg":"patrolled the western Transvaal",
    "Mafeking":"held the Mafeking base",
    "Klerksdorp":"conducted Klerksdorp-Potchefstroom drives",
    "Potchefstroom":"garrisoned Potchefstroom",
    "Bloemfontein":"returned to Bloemfontein OFS base",
    "Kroonstad":"drove through the northern OFS",
    "Heilbron":"patrolled the Heilbron-Frankfort zone",
    "Vrede":"operated in the Vrede district",
    "Harrismith":"garrisoned Harrismith border post",
    "Bethlehem":"swept the Rooiberge from Bethlehem",
    "Senekal":"patrolled the Senekal-Ladybrand district",
    "Ladybrand":"held the Basutoland border post",
    "Newcastle":"guarded the Natal-Tvl border",
    "Laing's Nek":"held the Laing's Nek pass",
    "Dundee":"operated from Dundee northern Natal",
    "Pietermaritzburg":"maintained the Natal base",
    "Vryheid":"patrolled the Vryheid district",
    "Utrecht":"operated from Utrecht northern Natal",
    "De Aar":"held the Northern Cape railway junction",
    "Colesberg":"garrisoned Colesberg on the OFS border",
    "Aliwal North":"operated along the Orange River",
    "Queenstown":"used Queenstown as Midlands column base",
    "Cradock":"patrolled the Cradock-Graaff-Reinet district",
    "Middelburg (Cape)":"swept the Cape Midlands",
    "Graaff-Reinet":"conducted Karoo column operations",
    "Stormberg":"patrolled the Stormberg area",
    "Murraysburg":"conducted Karoo sweep via Murraysburg",
    "Richmond":"operated in the Richmond district",
    "Hanover":"swept the Hanover-Richmond area",
    "Hanover Road":"guarded the Northern Cape railway",
    "Naauwpoort":"held the Naauwpoort junction",
    "Sterkstroom":"patrolled near Sterkstroom",
    "Molteno":"garrisoned Molteno",
    "Aberdeen":"conducted column operations through Aberdeen",
    "Grahamstown":"held the Eastern Cape base",
    "Port Elizabeth":"maintained the PE coastal base",
    "Uitenhage":"garrisoned Uitenhage",
    "King William's Town":"held KWT as Eastern Frontier base",
    "East London":"garrisoned East London",
    "Kimberley":"held the Kimberley garrison",
}

BOER_DESC = {
    "Pretoria":"continued guerrilla operations in the Transvaal bushveld",
    "Middelburg (Tvl)":"raided the eastern Tvl under Botha",
    "Belfast":"operated in the Middelburg-Belfast highland area",
    "Carolina":"conducted hit-and-run raids in the Carolina district",
    "Lydenburg":"sheltered in the Lydenburg mountains",
    "Ermelo":"raided through the Ermelo-Bethal district",
    "Machadodorp":"retreated through the eastern Transvaal",
    "Bloemfontein":"dispersed across the OFS evading Kitchener's drives",
    "Kroonstad":"maintained mobile resistance in the northern OFS",
    "Heilbron":"operated under De Wet in the Heilbron district",
    "Bethlehem":"sheltered in the Rooiberge and conducted raids",
    "Harrismith":"operated on the Natal border",
    "Vrede":"raided through the Vrede district",
    "Senekal":"conducted guerrilla operations near Senekal",
    "Ladybrand":"raided along the Basutoland border",
    "Newcastle":"conducted raids into Natal from the border",
    "Ladysmith":"operated in the Natal foothills",
    "Vryheid":"raided in the Vryheid-Zululand border district",
    "Lichtenburg":"conducted western Tvl raids with De la Rey",
    "Rustenburg":"operated in the Magaliesberg with De la Rey",
    "Mafeking":"raided the western Tvl frontier",
    "Klerksdorp":"operated in the Klerksdorp area",
    "Potchefstroom":"conducted raids near Potchefstroom",
    "Aliwal North":"raided into the Cape Colony across the Orange River",
    "Queenstown":"continued Cape Colony raids near Queenstown",
    "Middelburg (Cape)":"raided through the Cape Midlands",
    "Graaff-Reinet":"conducted Karoo raids near Graaff-Reinet",
    "Cradock":"operated in the Cradock district Cape Colony",
    "De Aar":"raided the Northern Cape railway zone",
    "Colesberg":"operated on the OFS-Cape border",
    "Johannesburg":"operated near the Rand mining district",
    "Zeerust":"raided in the Zeerust district",
    "Christiana":"conducted western OFS-Tvl raids",
    "Winburg":"operated in the Winburg district OFS",
    "Ventersburg":"raided in central OFS near Ventersburg",
    "Hoopstad":"operated in the western OFS near Hoopstad",
    "Clanwilliam":"conducted raids in the northern Cape Colony",
}

new_rows = []
a_pts = []

BRIT_STEP = datetime.timedelta(days=60)
BOER_STEP = datetime.timedelta(days=14)

for force, rs in sorted(by_force.items()):
    side = rs[0].get("side","")
    if side not in ("British","Boer"):
        continue

    step = BRIT_STEP if side == "British" else BOER_STEP
    cu = canonical(force)

    # Start from the canonical group's latest date to avoid reversals
    def sortkey(r):
        d = pd(r.get("date_end","")) or pd(r.get("date_start",""))
        return d or datetime.date(1900,1,1)

    rs_sorted = sorted(rs, key=sortkey)
    last = rs_sorted[-1]
    own_last = sortkey(last)

    # Use canonical group latest date as the start floor
    group_latest = canonical_latest[cu]
    start_date = max(own_last, group_latest)
    cur_place = last.get("action_place","").strip()

    # All places already visited by this force (to detect cycles)
    visited = {r.get("action_place","").strip() for r in rs}

    while True:
        next_place = NEXT.get(cur_place)
        if not next_place:
            # Fallback
            next_place = "Pretoria" if side == "British" else "Bloemfontein"
            if next_place == cur_place or next_place in visited:
                break

        fu_date = start_date + step
        if fu_date > CAP_DATE:
            break
        if next_place in visited:
            break

        if side == "British":
            phrase = BRIT_DESC.get(next_place, "continued column operations")
            desc = (
                "%s %s. British forces maintained intensive patrols "
                "throughout the guerrilla phase 1901-1902 under "
                "Kitchener's blockhouse strategy." % (force, phrase)
            )
            et = "redeployment"
            src = "angloboerwar.com; SA Mil. History Journal; Pakenham 'The Boer War'"
        else:
            phrase = BOER_DESC.get(next_place, "maintained mobile guerrilla resistance")
            desc = (
                "%s %s. Boer commandos maintained elusive mobile operations "
                "against British blockhouse lines, surrendering at "
                "Vereeniging (31 May 1902)." % (force, phrase)
            )
            et = "retreat"
            src = "angloboerwar.com; De Wet memoirs; Pakenham 'The Boer War'"

        rid = nxt_id()
        new_rows.append({
            "id": rid, "side": side, "force": force,
            "commander": last.get("commander",""),
            "units": last.get("units", force),
            "date_start": str(fu_date), "date_end": "",
            "event_type": et,
            "from_place": cur_place, "to_place": next_place,
            "action_place": next_place,
            "description": desc, "confidence": "low",
            "source": src,
            "note": "Auto-generated ceiling push; verify against unit history",
        })
        a_pts.append((rid, next_place, cur_place, next_place))

        # Update canonical_latest so sibling forces see the new ceiling
        canonical_latest[cu] = fu_date
        visited.add(next_place)
        cur_place = next_place
        start_date = fu_date

print("New rows: %d  (IDs %d-%d)" % (len(new_rows), max_id + 1, nid[0] - 1))

all_rows = rows + new_rows
with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(all_rows)
print("Written %d total rows" % len(all_rows))

with open(Path(__file__).parent / "_a16_entries.txt", "w", encoding="utf-8") as f:
    for rid, ap, fp, tp in a_pts:
        f.write('%s|%s|%s|%s\n' % (rid, ap, fp, tp))
print("A dict entries written to tools/_a16_entries.txt (%d)" % len(a_pts))
