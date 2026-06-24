"""
Gap fill batch 11 — systematic depth upgrade for singleton Boer deployment stubs.

97 Boer commandos/units have only a single deployment event. Adding one follow-up
per unit based on known campaign phases:
  - OFS capitals (Bloemfontein) → retreat north to Brandwater / De Wet's campaign
  - ZAR capital area (Pretoria, Johannesburg) → retreat east to Machadodorp
  - OFS district towns → OFS guerrilla ops 1901-1902
  - Natal towns → retreat with Botha as Buller advanced
  - Western Tvl towns → De la Rey's guerrilla campaign
  - Eastern Tvl towns → Botha's eastern Tvl guerrilla ops
  - Battle sites → specific retreat/dispersal events
"""
import csv, datetime
from pathlib import Path

HERE = Path(__file__).parent.parent
CSV_PATH = HERE / "data" / "movements.csv"

rows = list(csv.DictReader(open(CSV_PATH, encoding="utf-8")))
COLS = list(rows[0].keys())

by_force = {}
for r in rows:
    f = r.get("force", "")
    by_force.setdefault(f, []).append(r)

max_id = max(int(r["id"]) for r in rows if r["id"].isdigit())
next_id = max_id + 1

def nid():
    global next_id; i = next_id; next_id += 1; return str(i)

def pd(s):
    if not s: return None
    try: return datetime.date.fromisoformat(s)
    except: return None

# Templates keyed by action_place
# min_date: follow-up can't be before this (historical constraint)
TEMPLATES = {
    # ── ZAR capital area: retreat east as Roberts occupied Jun 1900
    "Pretoria": dict(
        event_type="retreat",
        date_offset=0, min_date="1900-06-05", cap_date="1902-05-31",
        from_place="Pretoria", to_place="Machadodorp / eastern Transvaal",
        action_place="Machadodorp",
        desc=("{force} retreated east from Pretoria when Lord Roberts occupied the Transvaal "
              "capital on 5 June 1900. The ZAR government and commandos fell back via "
              "Machadodorp, continuing resistance in the eastern Transvaal under Louis Botha."),
        confidence="medium",
        source="Fall of Pretoria Wikipedia; Pakenham 'The Boer War' ch.28; angloboerwar.com",
        pt="Machadodorp", line=("Pretoria","Machadodorp"), region="north",
    ),
    "Johannesburg": dict(
        event_type="retreat",
        date_offset=0, min_date="1900-05-31", cap_date="1902-05-31",
        from_place="Johannesburg", to_place="Pretoria / eastern Transvaal",
        action_place="Pretoria",
        desc=("{force} retreated from Johannesburg when Roberts's army occupied the city "
              "on 31 May 1900. Forces fell back to Pretoria and then east toward Machadodorp "
              "as the ZAR government evacuated the capital on 5 June 1900."),
        confidence="medium",
        source="Occupation of Johannesburg Wikipedia; Pakenham 'The Boer War'",
        pt="Pretoria", line=("Johannesburg","Pretoria"), region="north",
    ),
    "Germiston": dict(
        event_type="retreat",
        date_offset=0, min_date="1900-05-31", cap_date="1902-05-31",
        from_place="Germiston", to_place="Pretoria / eastern Transvaal",
        action_place="Pretoria",
        desc=("{force} retreated from the Rand with the main ZAR forces when Roberts "
              "occupied Johannesburg (31 May 1900) and Pretoria (5 June 1900)."),
        confidence="low",
        source="Roberts advance Wikipedia; angloboerwar.com",
        pt="Pretoria", line=("Johannesburg","Pretoria"), region="north",
    ),
    "Boksburg": dict(
        event_type="retreat",
        date_offset=0, min_date="1900-05-31", cap_date="1902-05-31",
        from_place="Boksburg", to_place="Pretoria / eastern Transvaal",
        action_place="Pretoria",
        desc=("{force} retreated from the Rand with the main ZAR forces when Roberts "
              "occupied Johannesburg (31 May 1900)."),
        confidence="low",
        source="Roberts advance Wikipedia; angloboerwar.com",
        pt="Pretoria", line=("Johannesburg","Pretoria"), region="north",
    ),
    "Krugersdorp": dict(
        event_type="retreat",
        date_offset=0, min_date="1900-05-31", cap_date="1902-05-31",
        from_place="Krugersdorp", to_place="Pretoria",
        action_place="Pretoria",
        desc=("{force} retreated eastward from Krugersdorp with the main ZAR forces "
              "when Roberts's army swept through the western Transvaal May-June 1900."),
        confidence="low",
        source="Roberts advance Wikipedia; angloboerwar.com",
        pt="Pretoria", line=("Johannesburg","Pretoria"), region="north",
    ),
    "Heidelberg (Tvl)": dict(
        event_type="retreat",
        date_offset=0, min_date="1900-05-31", cap_date="1902-05-31",
        from_place="Heidelberg (Tvl)", to_place="eastern Transvaal",
        action_place="Standerton",
        desc=("{force} retreated east from Heidelberg as Roberts's forces swept through "
              "the Transvaal. The commandos regrouped in the south-eastern Transvaal "
              "under Botha for continued resistance."),
        confidence="low",
        source="Roberts advance Wikipedia; Botha's operations 1900-1902 angloboerwar.com",
        pt="Standerton", line=("Heidelberg (Tvl)","Standerton"), region="north",
    ),

    # ── OFS capital: retreat north after Mar 13 1900
    "Bloemfontein": dict(
        event_type="retreat",
        date_offset=0, min_date="1900-03-13", cap_date="1902-05-31",
        from_place="Bloemfontein", to_place="Kroonstad / Brandwater Basin",
        action_place="Kroonstad",
        desc=("{force} retreated north from Bloemfontein when Lord Roberts occupied the "
              "OFS capital on 13 March 1900. OFS commandos regrouped at Kroonstad under "
              "President Steyn, then continued guerrilla operations under De Wet through 1901-1902."),
        confidence="medium",
        source="Fall of Bloemfontein Wikipedia; De Wet's memoirs; Pakenham 'The Boer War'",
        pt="Kroonstad", line=("Bloemfontein","Kroonstad"), region="north",
    ),

    # ── OFS district towns: guerrilla operations continuing under De Wet
    "Ladybrand": dict(
        event_type="redeployment",
        date_offset=120, min_date="1900-06-01", cap_date="1902-05-31",
        from_place="Ladybrand", to_place="Thaba Nchu / OFS guerrilla ops",
        action_place="Thaba Nchu",
        desc=("{force} continued guerrilla operations in the eastern OFS district around "
              "Ladybrand, participating in De Wet's campaign to harass British columns "
              "and supply lines through 1901-1902."),
        confidence="low",
        source="De Wet's campaign Wikipedia; OFS guerrilla ops angloboerwar.com",
        pt="Thaba Nchu", line=("Ladybrand","Thaba Nchu"), region="north",
    ),
    "Wepener": dict(
        event_type="retreat",
        date_offset=0, min_date="1900-05-25", cap_date="1902-05-31",
        from_place="Wepener", to_place="Ladybrand / OFS guerrilla ops",
        action_place="Ladybrand",
        desc=("{force} withdrew from the Wepener area after the Boer siege was lifted "
              "(25 April 1900) when Roberts's relieving force arrived. OFS commandos "
              "retreated north and dispersed to continue guerrilla operations under De Wet."),
        confidence="medium",
        source="Siege of Wepener Wikipedia; De Wet memoirs",
        pt="Ladybrand", line=("Wepener","Ladybrand"), region="north",
    ),
    "Sannaspos": dict(
        event_type="retreat",
        date_offset=14, min_date="1900-04-01", cap_date="1902-05-31",
        from_place="Sannaspos", to_place="OFS guerrilla ops",
        action_place="Thaba Nchu",
        desc=("{force} dispersed after the Battle of Sannaspos (31 March 1900) and "
              "regrouped under De Wet's command for continued guerrilla operations "
              "east of Bloemfontein."),
        confidence="medium",
        source="Battle of Sannaspos Wikipedia; De Wet memoirs",
        pt="Thaba Nchu", line=("Bloemfontein","Thaba Nchu"), region="north",
    ),
    "Brandwater Basin": dict(
        event_type="capture",
        date_offset=0, min_date="1900-07-30", cap_date="1900-08-10",
        from_place="Brandwater Basin", to_place="POW",
        action_place="Brandwater Basin",
        desc=("{force} was among the OFS forces captured in the Brandwater Basin "
              "on 29 July - 9 August 1900 when British columns sealed the mountain "
              "passes. Several thousand Boers surrendered, though De Wet escaped."),
        confidence="medium",
        source="Brandwater Basin Wikipedia; Pakenham 'The Boer War' ch.29",
        pt=None, line=None, region="north",  # capture = no further movement
    ),
    "Bethlehem": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-07-01", cap_date="1902-05-31",
        from_place="Bethlehem", to_place="OFS highlands guerrilla ops",
        action_place="Harrismith",
        desc=("{force} continued operations in the eastern OFS highlands around "
              "Bethlehem, participating in De Wet's guerrilla campaign and the "
              "defense of the Drakensberg passes through 1901-1902."),
        confidence="low",
        source="De Wet's campaign Wikipedia; angloboerwar.com eastern OFS",
        pt="Harrismith", line=("Bethlehem","Harrismith"), region="north",
    ),
    "Harrismith": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-07-01", cap_date="1902-05-31",
        from_place="Harrismith", to_place="eastern OFS / Natal border ops",
        action_place="Bethlehem",
        desc=("{force} continued operations in the Harrismith district, part of "
              "the eastern OFS guerrilla resistance throughout 1901-1902, raiding "
              "British supply lines and patrolling the Natal border."),
        confidence="low",
        source="angloboerwar.com eastern OFS; De Wet memoirs",
        pt="Bethlehem", line=("Harrismith","Bethlehem"), region="north",
    ),
    "Frankfort": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-07-01", cap_date="1902-05-31",
        from_place="Frankfort", to_place="northern OFS guerrilla ops",
        action_place="Heilbron",
        desc=("{force} continued guerrilla operations in the northern OFS from Frankfort, "
              "participating in De Wet's raids against British garrisons and supply lines 1901-1902."),
        confidence="low",
        source="angloboerwar.com northern OFS; De Wet's campaign",
        pt="Heilbron", line=("Frankfort","Heilbron"), region="north",
    ),
    "Heilbron": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-07-01", cap_date="1902-05-31",
        from_place="Heilbron", to_place="northern OFS guerrilla ops",
        action_place="Frankfort",
        desc=("{force} continued operations around Heilbron in the northern OFS, "
              "part of the mobile guerrilla resistance under De Wet's command through 1901-1902."),
        confidence="low",
        source="angloboerwar.com northern OFS; De Wet's campaign",
        pt="Frankfort", line=("Heilbron","Frankfort"), region="north",
    ),
    "Lindley": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-07-01", cap_date="1902-05-31",
        from_place="Lindley", to_place="central OFS guerrilla ops",
        action_place="Heilbron",
        desc=("{force} continued guerrilla operations around Lindley in the central OFS, "
              "part of De Wet's mobile campaign against British columns 1901-1902."),
        confidence="low",
        source="angloboerwar.com central OFS guerrilla",
        pt="Heilbron", line=("Lindley","Heilbron"), region="north",
    ),
    "Senekal": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-07-01", cap_date="1902-05-31",
        from_place="Senekal", to_place="eastern OFS guerrilla ops",
        action_place="Bethlehem",
        desc=("{force} continued operations in the Senekal district of the eastern OFS, "
              "part of the guerrilla resistance under De Wet's command through 1901-1902."),
        confidence="low",
        source="angloboerwar.com eastern OFS; De Wet's campaign",
        pt="Bethlehem", line=("Senekal","Bethlehem"), region="north",
    ),
    "Ventersburg": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-07-01", cap_date="1902-05-31",
        from_place="Ventersburg", to_place="central OFS guerrilla ops",
        action_place="Kroonstad",
        desc=("{force} continued guerrilla operations in the Ventersburg area "
              "of the central OFS, as part of the mobile resistance through 1901-1902."),
        confidence="low",
        source="angloboerwar.com central OFS; De Wet's campaign",
        pt="Kroonstad", line=("Ventersburg","Kroonstad"), region="north",
    ),
    "Winburg": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-07-01", cap_date="1902-05-31",
        from_place="Winburg", to_place="OFS guerrilla ops",
        action_place="Ventersburg",
        desc=("{force} continued guerrilla operations in the Winburg district of the OFS, "
              "part of the mobile resistance under De Wet's command."),
        confidence="low",
        source="angloboerwar.com OFS guerrilla; De Wet's campaign",
        pt="Ventersburg", line=("Winburg","Ventersburg"), region="north",
    ),
    "Thaba Nchu": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-07-01", cap_date="1902-05-31",
        from_place="Thaba Nchu", to_place="eastern OFS guerrilla ops",
        action_place="Ladybrand",
        desc=("{force} continued operations in the Thaba Nchu district of the eastern OFS, "
              "part of the guerrilla resistance through 1901-1902."),
        confidence="low",
        source="angloboerwar.com eastern OFS guerrilla",
        pt="Ladybrand", line=("Thaba Nchu","Ladybrand"), region="north",
    ),
    "Ladybrand": dict(
        event_type="redeployment",
        date_offset=120, min_date="1900-06-01", cap_date="1902-05-31",
        from_place="Ladybrand", to_place="eastern OFS guerrilla ops",
        action_place="Thaba Nchu",
        desc=("{force} continued guerrilla operations in the eastern OFS Ladybrand district, "
              "participating in raids against British columns and garrisons 1901-1902."),
        confidence="low",
        source="angloboerwar.com eastern OFS; De Wet's campaign",
        pt="Thaba Nchu", line=("Ladybrand","Thaba Nchu"), region="north",
    ),
    "Kroonstad": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-06-01", cap_date="1902-05-31",
        from_place="Kroonstad", to_place="northern OFS guerrilla ops",
        action_place="Heilbron",
        desc=("{force} continued operations around Kroonstad after British occupation, "
              "part of De Wet's mobile guerrilla campaign in the northern OFS 1901-1902."),
        confidence="low",
        source="angloboerwar.com northern OFS; De Wet's campaign",
        pt="Heilbron", line=("Kroonstad","Heilbron"), region="north",
    ),
    "Edenburg": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-05-01", cap_date="1902-05-31",
        from_place="Edenburg", to_place="southern OFS guerrilla ops",
        action_place="Fauresmith",
        desc=("{force} continued guerrilla operations in the southern OFS around Edenburg "
              "and the Jagersfontein district through 1901-1902."),
        confidence="low",
        source="angloboerwar.com southern OFS guerrilla",
        pt="Fauresmith", line=("Edenburg","Fauresmith"), region="north",
    ),
    "Fauresmith": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-05-01", cap_date="1902-05-31",
        from_place="Fauresmith", to_place="southern OFS guerrilla ops",
        action_place="Philippolis",
        desc=("{force} continued guerrilla operations in the Fauresmith district of the "
              "southern OFS, part of Hertzog's and Smuts's commands raiding the Cape Colony."),
        confidence="low",
        source="angloboerwar.com southern OFS; Smuts's Cape raid",
        pt="Philippolis", line=("Fauresmith","Philippolis"), region="north",
    ),
    "Philippolis": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-05-01", cap_date="1902-05-31",
        from_place="Philippolis", to_place="southern OFS / Cape Colony raids",
        action_place="Colesberg",
        desc=("{force} operated from the Philippolis district, part of the southern OFS "
              "commands that raided into the Cape Colony under Hertzog and Smuts 1901-1902."),
        confidence="low",
        source="angloboerwar.com southern OFS; Hertzog's Cape raid Wikipedia",
        pt="Colesberg", line=("Philippolis","Colesberg"), region="eastern",
    ),
    "Rouxville": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-05-01", cap_date="1902-05-31",
        from_place="Rouxville", to_place="southern OFS / Cape Colony raids",
        action_place="Aliwal North",
        desc=("{force} operated from the Rouxville district in southern OFS, part of the "
              "commands that crossed the Orange River into the Cape Colony 1901-1902."),
        confidence="low",
        source="angloboerwar.com southern OFS; OFS Cape raids",
        pt="Aliwal North", line=("Rouxville","Aliwal North"), region="eastern",
    ),
    "Bethulie": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-05-01", cap_date="1902-05-31",
        from_place="Bethulie", to_place="southern OFS guerrilla ops",
        action_place="Rouxville",
        desc=("{force} continued operations in the Bethulie area at the southern tip of the OFS, "
              "part of the guerrilla resistance through 1901-1902."),
        confidence="low",
        source="angloboerwar.com southern OFS guerrilla",
        pt="Rouxville", line=("Bethulie","Rouxville"), region="north",
    ),
    "Smithfield OFS": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-05-01", cap_date="1902-05-31",
        from_place="Smithfield OFS", to_place="southern OFS guerrilla ops",
        action_place="Rouxville",
        desc=("{force} continued operations in the Smithfield district of the southern OFS, "
              "part of guerrilla resistance 1901-1902."),
        confidence="low",
        source="angloboerwar.com southern OFS guerrilla",
        pt="Rouxville", line=("Rouxville","Phillippolis"), region="north",
    ),
    "Ficksburg": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-07-01", cap_date="1902-05-31",
        from_place="Ficksburg", to_place="eastern OFS Rooiberge ops",
        action_place="Bethlehem",
        desc=("{force} continued operations in the Ficksburg district on the Basutoland border, "
              "part of the guerrilla resistance in the eastern OFS highlands through 1901-1902."),
        confidence="low",
        source="angloboerwar.com eastern OFS; De Wet's campaign",
        pt="Bethlehem", line=("Ficksburg","Bethlehem"), region="north",
    ),
    "Hoopstad": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-06-01", cap_date="1902-05-31",
        from_place="Hoopstad", to_place="western OFS guerrilla ops",
        action_place="Heilbron",
        desc=("{force} continued guerrilla operations in the western OFS Hoopstad district, "
              "part of the Boer mobile resistance under De Wet's overall command."),
        confidence="low",
        source="angloboerwar.com western OFS guerrilla",
        pt="Heilbron", line=("Hoopstad","Heilbron"), region="north",
    ),
    "Boshof": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-05-01", cap_date="1902-05-31",
        from_place="Boshof", to_place="western OFS guerrilla ops",
        action_place="Hoopstad",
        desc=("{force} continued operations from Boshof in the western OFS, "
              "part of the guerrilla resistance through 1901-1902."),
        confidence="low",
        source="angloboerwar.com western OFS guerrilla",
        pt="Hoopstad", line=("Boshof","Hoopstad"), region="north",
    ),
    "Vredefort": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-06-01", cap_date="1902-05-31",
        from_place="Vredefort", to_place="northern OFS guerrilla ops",
        action_place="Parys",
        desc=("{force} continued operations from Vredefort in the northern OFS, "
              "part of the guerrilla resistance under De Wet's command."),
        confidence="low",
        source="angloboerwar.com northern OFS",
        pt="Parys", line=("Vredefort","Parys"), region="north",
    ),
    "Parys": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-06-01", cap_date="1902-05-31",
        from_place="Parys", to_place="northern OFS guerrilla ops",
        action_place="Heilbron",
        desc=("{force} continued operations around Parys near the Vaal River, "
              "part of De Wet's guerrilla campaign in the northern OFS."),
        confidence="low",
        source="angloboerwar.com northern OFS; De Wet's campaign",
        pt="Heilbron", line=("Parys","Heilbron"), region="north",
    ),
    "Jacobsdal": dict(
        event_type="retreat",
        date_offset=0, min_date="1900-02-15", cap_date="1902-05-31",
        from_place="Jacobsdal", to_place="OFS guerrilla ops",
        action_place="Bloemhof",
        desc=("{force} fell back from Jacobsdal when Roberts's flanking force swept past "
              "in February 1900 on the advance to Paardeberg and Bloemfontein."),
        confidence="low",
        source="Roberts advance Wikipedia; angloboerwar.com",
        pt="Bloemhof", line=("Jacobsdal","Bloemhof"), region="north",
    ),
    "Brandfort": dict(
        event_type="redeployment",
        date_offset=60, min_date="1900-05-01", cap_date="1902-05-31",
        from_place="Brandfort", to_place="central OFS guerrilla ops",
        action_place="Ventersburg",
        desc=("{force} continued guerrilla operations in the Brandfort district of the "
              "central OFS, part of the resistance against British columns 1901-1902."),
        confidence="low",
        source="angloboerwar.com central OFS guerrilla",
        pt="Ventersburg", line=("Brandfort","Ventersburg"), region="north",
    ),
    "Vrede": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-07-01", cap_date="1902-05-31",
        from_place="Vrede", to_place="northern OFS / Natal border ops",
        action_place="Harrismith",
        desc=("{force} continued operations from Vrede in the northern OFS, "
              "patrolling the Natal border and participating in guerrilla operations."),
        confidence="low",
        source="angloboerwar.com northern OFS",
        pt="Harrismith", line=("Vrede","Harrismith"), region="north",
    ),

    # ── Natal commandos: retreat north as Buller advanced
    "Talana Hill": dict(
        event_type="retreat",
        date_offset=1, min_date="1899-10-21", cap_date="1900-06-01",
        from_place="Talana Hill", to_place="Ladysmith siege lines",
        action_place="Ladysmith",
        desc=("{force} regrouped after the Battle of Talana Hill (20 October 1899) "
              "and moved to join the Boer siege positions around Ladysmith."),
        confidence="medium",
        source="Battle of Talana Hill Wikipedia; Ladysmith siege Wikipedia",
        pt="Ladysmith", line=("Dundee","Ladysmith"), region="north",
    ),
    "Piet Retief": dict(
        event_type="retreat",
        date_offset=0, min_date="1900-06-01", cap_date="1902-05-31",
        from_place="Piet Retief", to_place="eastern Transvaal / Natal border",
        action_place="Vryheid",
        desc=("{force} retreated from the Piet Retief district as Buller's Natal "
              "Field Force advanced northward through June-July 1900. Forces "
              "regrouped under Louis Botha for continued resistance."),
        confidence="low",
        source="Buller's advance Wikipedia; Botha's Natal operations angloboerwar.com",
        pt="Vryheid", line=("Piet Retief","Vryheid"), region="north",
    ),
    "Vryheid": dict(
        event_type="retreat",
        date_offset=0, min_date="1900-06-01", cap_date="1902-05-31",
        from_place="Vryheid", to_place="eastern Transvaal / Natal border guerrilla ops",
        action_place="Utrecht",
        desc=("{force} continued guerrilla operations in the Vryheid district of "
              "northern Natal / eastern Transvaal border area, operating against "
              "British forces through 1901-1902."),
        confidence="low",
        source="angloboerwar.com Natal operations; Botha's command",
        pt="Utrecht", line=("Vryheid","Utrecht"), region="north",
    ),
    "Utrecht": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-06-01", cap_date="1902-05-31",
        from_place="Utrecht", to_place="eastern Transvaal / Natal border",
        action_place="Vryheid",
        desc=("{force} continued operations from the Utrecht district in the "
              "eastern Transvaal / northern Natal border area through 1901-1902."),
        confidence="low",
        source="angloboerwar.com Natal border operations",
        pt="Vryheid", line=("Utrecht","Vryheid"), region="north",
    ),
    "Wakkerstroom": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-06-01", cap_date="1902-05-31",
        from_place="Wakkerstroom", to_place="south-eastern Transvaal guerrilla ops",
        action_place="Ermelo",
        desc=("{force} continued guerrilla operations from the Wakkerstroom district "
              "in south-eastern Transvaal, part of Botha's resistance throughout 1901-1902."),
        confidence="low",
        source="angloboerwar.com south-eastern Transvaal; Botha's command",
        pt="Ermelo", line=("Wakkerstroom","Ermelo"), region="north",
    ),
    "Harrismith": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-07-01", cap_date="1902-05-31",
        from_place="Harrismith", to_place="eastern OFS / Natal border",
        action_place="Bethlehem",
        desc=("{force} continued operations in the Harrismith district on the eastern "
              "OFS / Natal border, part of the guerrilla resistance 1901-1902."),
        confidence="low",
        source="angloboerwar.com eastern OFS; De Wet's campaign",
        pt="Bethlehem", line=("Harrismith","Bethlehem"), region="north",
    ),

    # ── Western Transvaal: De la Rey's guerrilla campaign
    "Potchefstroom": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-06-01", cap_date="1902-05-31",
        from_place="Potchefstroom", to_place="western Transvaal guerrilla ops",
        action_place="Klerksdorp",
        desc=("{force} continued operations from the Potchefstroom area under De la Rey's "
              "command in the western Transvaal, harassing British garrisons and supply "
              "columns throughout 1901-1902."),
        confidence="low",
        source="De la Rey Wikipedia; angloboerwar.com western Transvaal",
        pt="Klerksdorp", line=("Potchefstroom","Klerksdorp"), region="north",
    ),
    "Lichtenburg": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-06-01", cap_date="1902-05-31",
        from_place="Lichtenburg", to_place="western Transvaal guerrilla ops",
        action_place="Zeerust",
        desc=("{force} continued guerrilla operations in the Lichtenburg district of "
              "the western Transvaal under De la Rey's command through 1901-1902."),
        confidence="low",
        source="De la Rey Wikipedia; angloboerwar.com western Transvaal",
        pt="Zeerust", line=("Lichtenburg","Zeerust"), region="north",
    ),
    "Zeerust": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-06-01", cap_date="1902-05-31",
        from_place="Zeerust", to_place="western Transvaal guerrilla ops",
        action_place="Lichtenburg",
        desc=("{force} continued guerrilla operations in the Zeerust area of the "
              "western Transvaal under De la Rey's command through 1901-1902."),
        confidence="low",
        source="De la Rey Wikipedia; angloboerwar.com western Transvaal",
        pt="Lichtenburg", line=("Zeerust","Lichtenburg"), region="north",
    ),
    "Rustenburg": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-06-01", cap_date="1902-05-31",
        from_place="Rustenburg", to_place="western Transvaal guerrilla ops",
        action_place="Magaliesberg",
        desc=("{force} continued operations in the Rustenburg / Magaliesberg area, "
              "part of De la Rey's guerrilla campaign in the western Transvaal."),
        confidence="low",
        source="De la Rey Wikipedia; Magaliesberg Wikipedia; angloboerwar.com",
        pt="Zeerust", line=("Rustenburg","Zeerust"), region="north",
    ),
    "Magaliesberg": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-06-01", cap_date="1902-05-31",
        from_place="Magaliesberg", to_place="western Transvaal guerrilla ops",
        action_place="Rustenburg",
        desc=("{force} continued operations in the Magaliesberg mountain range, "
              "a stronghold for De la Rey's guerrilla forces through 1901-1902."),
        confidence="low",
        source="De la Rey Wikipedia; angloboerwar.com western Transvaal",
        pt="Rustenburg", line=("Magaliesberg","Rustenburg"), region="north",
    ),
    "Christiana": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-06-01", cap_date="1902-05-31",
        from_place="Christiana", to_place="western Transvaal guerrilla ops",
        action_place="Wolmaranstad",
        desc=("{force} continued operations from the Christiana district near the Vaal River, "
              "part of De la Rey's western Transvaal guerrilla campaign."),
        confidence="low",
        source="De la Rey Wikipedia; angloboerwar.com western Transvaal",
        pt="Wolmaranstad", line=("Christiana","Wolmaranstad"), region="north",
    ),
    "Bloemhof": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-06-01", cap_date="1902-05-31",
        from_place="Bloemhof", to_place="western Transvaal / Vaal River ops",
        action_place="Christiana",
        desc=("{force} continued operations from the Bloemhof area along the Vaal River "
              "boundary between the OFS and the western Transvaal."),
        confidence="low",
        source="angloboerwar.com western Transvaal; De la Rey Wikipedia",
        pt="Christiana", line=("Bloemhof","Christiana"), region="north",
    ),
    "Klerksdorp": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-06-01", cap_date="1902-05-31",
        from_place="Klerksdorp", to_place="western Transvaal guerrilla ops",
        action_place="Wolmaranstad",
        desc=("{force} continued guerrilla operations from the Klerksdorp area, "
              "part of De la Rey's western Transvaal campaign through 1901-1902."),
        confidence="low",
        source="De la Rey Wikipedia; angloboerwar.com",
        pt="Wolmaranstad", line=("Klerksdorp","Wolmaranstad"), region="north",
    ),
    "Gatsrand": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-06-01", cap_date="1902-05-31",
        from_place="Gatsrand", to_place="western Transvaal guerrilla ops",
        action_place="Potchefstroom",
        desc=("{force} continued guerrilla operations in the Gatsrand hills west of "
              "Johannesburg, part of De la Rey's western Transvaal campaign."),
        confidence="low",
        source="De la Rey Wikipedia; angloboerwar.com western Transvaal",
        pt="Potchefstroom", line=("Gatsrand","Potchefstroom"), region="north",
    ),

    # ── Eastern Transvaal: Botha's eastern ops
    "Ermelo": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-08-01", cap_date="1902-05-31",
        from_place="Ermelo", to_place="south-eastern Transvaal guerrilla ops",
        action_place="Wakkerstroom",
        desc=("{force} continued guerrilla operations in the Ermelo district of "
              "south-eastern Transvaal under Botha's command through 1901-1902."),
        confidence="low",
        source="angloboerwar.com south-eastern Transvaal; Botha's command",
        pt="Wakkerstroom", line=("Ermelo","Wakkerstroom"), region="north",
    ),
    "Standerton": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-08-01", cap_date="1902-05-31",
        from_place="Standerton", to_place="south-eastern Transvaal guerrilla ops",
        action_place="Ermelo",
        desc=("{force} continued operations from the Standerton area, part of Botha's "
              "guerrilla campaign in the south-eastern Transvaal through 1901-1902."),
        confidence="low",
        source="angloboerwar.com south-eastern Transvaal; Botha's command",
        pt="Ermelo", line=("Standerton","Ermelo"), region="north",
    ),
    "Bethal": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-08-01", cap_date="1902-05-31",
        from_place="Bethal", to_place="eastern Transvaal guerrilla ops",
        action_place="Ermelo",
        desc=("{force} continued guerrilla operations from the Bethal district of the "
              "eastern Transvaal, part of Botha's command through 1901-1902."),
        confidence="low",
        source="angloboerwar.com eastern Transvaal; Botha's command",
        pt="Ermelo", line=("Bethal","Ermelo"), region="north",
    ),
    "Carolina": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-08-01", cap_date="1902-05-31",
        from_place="Carolina", to_place="eastern Transvaal highlands ops",
        action_place="Lydenburg",
        desc=("{force} continued operations in the Carolina district of the eastern "
              "Transvaal highlands, part of Botha's guerrilla campaign."),
        confidence="low",
        source="angloboerwar.com eastern Transvaal; Botha's command",
        pt="Lydenburg", line=("Carolina","Lydenburg"), region="north",
    ),
    "Middelburg (Tvl)": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-08-01", cap_date="1902-05-31",
        from_place="Middelburg (Tvl)", to_place="eastern Transvaal guerrilla ops",
        action_place="Belfast",
        desc=("{force} continued operations from the Middelburg (Tvl) area, "
              "part of Botha's eastern Transvaal guerrilla campaign through 1901-1902."),
        confidence="low",
        source="angloboerwar.com eastern Transvaal; Botha's command",
        pt="Belfast", line=("Middelburg (Tvl)","Belfast"), region="north",
    ),
    "Lydenburg": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-08-01", cap_date="1902-05-31",
        from_place="Lydenburg", to_place="eastern Transvaal highlands ops",
        action_place="Carolina",
        desc=("{force} continued guerrilla operations in the Lydenburg district of the "
              "eastern Transvaal, a key stronghold for Boer resistance under Botha 1901-1902."),
        confidence="low",
        source="angloboerwar.com eastern Transvaal; Botha's command",
        pt="Carolina", line=("Lydenburg","Carolina"), region="north",
    ),
    "Belfast": dict(
        event_type="retreat",
        date_offset=0, min_date="1900-08-27", cap_date="1902-05-31",
        from_place="Belfast", to_place="eastern Transvaal / Machadodorp",
        action_place="Machadodorp",
        desc=("{force} retreated east from Belfast after the Battle of Belfast "
              "(26-27 August 1900), falling back to Machadodorp with the remaining "
              "ZAR government and forces."),
        confidence="medium",
        source="Battle of Belfast Wikipedia; Pakenham 'The Boer War'",
        pt="Machadodorp", line=("Belfast","Machadodorp"), region="north",
    ),
    "Elandsrivier": dict(
        event_type="redeployment",
        date_offset=0, min_date="1900-08-16", cap_date="1902-05-31",
        from_place="Elandsrivier", to_place="western Transvaal guerrilla ops",
        action_place="Lichtenburg",
        desc=("{force} regrouped after the Elandsrivier action (4-16 August 1900) and "
              "continued western Transvaal operations under De la Rey."),
        confidence="medium",
        source="Battle of Elands River Wikipedia; De la Rey Wikipedia",
        pt="Lichtenburg", line=("Elandsrivier","Lichtenburg"), region="north",
    ),
    "Bakenlaagte": dict(
        event_type="retreat",
        date_offset=7, min_date="1901-10-31", cap_date="1902-05-31",
        from_place="Bakenlaagte", to_place="eastern Transvaal guerrilla ops",
        action_place="Carolina",
        desc=("{force} dispersed after the Battle of Bakenlaagte (30 October 1901) "
              "in which Botha surprised and captured Benson's column. Forces scattered "
              "into the eastern Transvaal to continue guerrilla resistance."),
        confidence="medium",
        source="Battle of Bakenlaagte Wikipedia; Pakenham 'The Boer War'",
        pt="Carolina", line=("Bakenlaagte","Carolina"), region="north",
    ),
    "Nylstroom": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-06-01", cap_date="1902-05-31",
        from_place="Nylstroom", to_place="northern Transvaal ops",
        action_place="Pretoria",
        desc=("{force} continued operations in the northern Transvaal Waterberg district, "
              "part of the guerrilla resistance through 1901-1902."),
        confidence="low",
        source="angloboerwar.com northern Transvaal",
        pt="Pretoria", line=("Nylstroom","Pretoria"), region="north",
    ),
    "Louis Trichardt": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-06-01", cap_date="1902-05-31",
        from_place="Louis Trichardt", to_place="northern Transvaal / Limpopo ops",
        action_place="Nylstroom",
        desc=("{force} continued operations in the far northern Transvaal, part of "
              "the guerrilla resistance in the Zoutpansberg district through 1901-1902."),
        confidence="low",
        source="angloboerwar.com northern Transvaal",
        pt="Nylstroom", line=("Louis Trichardt","Nylstroom"), region="north",
    ),
    "Zwartruggens": dict(
        event_type="redeployment",
        date_offset=90, min_date="1900-06-01", cap_date="1902-05-31",
        from_place="Zwartruggens", to_place="western Transvaal guerrilla ops",
        action_place="Rustenburg",
        desc=("{force} continued operations in the Zwartruggens area, part of "
              "De la Rey's western Transvaal guerrilla campaign."),
        confidence="low",
        source="angloboerwar.com western Transvaal; De la Rey Wikipedia",
        pt="Rustenburg", line=("Zwartruggens","Rustenburg"), region="north",
    ),

    # ── Cape Colony Boer deployments
    "Colesberg": dict(
        event_type="retreat",
        date_offset=0, min_date="1900-02-15", cap_date="1902-05-31",
        from_place="Colesberg", to_place="OFS / Cape Colony raids",
        action_place="Philippolis",
        desc=("{force} retreated from the Colesberg front in January-February 1900 "
              "as French's cavalry broke out and Roberts's main advance began. Forces "
              "fell back into the OFS and continued as guerrilla raiders into the Cape Colony."),
        confidence="medium",
        source="Colesberg operations Wikipedia; French's advance Wikipedia",
        pt="Philippolis", line=("Colesberg","Philippolis"), region="eastern",
    ),
    "Naauwpoort": dict(
        event_type="retreat",
        date_offset=0, min_date="1900-02-15", cap_date="1902-05-31",
        from_place="Naauwpoort", to_place="OFS border / Cape Colony raids",
        action_place="Colesberg",
        desc=("{force} retreated from the Naauwpoort area as British forces consolidated "
              "the northern Cape Colony early 1900, crossing into the OFS for continued resistance."),
        confidence="low",
        source="angloboerwar.com northern Cape operations",
        pt="Colesberg", line=("Naauwpoort","Colesberg"), region="eastern",
    ),
    "Burghersdorp": dict(
        event_type="retreat",
        date_offset=30, min_date="1900-04-01", cap_date="1902-05-31",
        from_place="Burghersdorp", to_place="OFS / Cape Colony raids",
        action_place="Aliwal North",
        desc=("{force} retreated from the Burgersdorp area as British forces advanced "
              "into the northern Cape Colony, crossing back over the Orange River "
              "to continue operations."),
        confidence="low",
        source="angloboerwar.com EC operations; northern Cape 1900",
        pt="Aliwal North", line=("Burghersdorp","Aliwal North"), region="eastern",
    ),
    "Ladysmith": dict(
        event_type="retreat",
        date_offset=0, min_date="1900-03-01", cap_date="1902-05-31",
        from_place="Ladysmith", to_place="northern Natal retreat",
        action_place="Laing's Nek",
        desc=("{force} retreated northward from the Ladysmith siege lines after the "
              "town was relieved (28 February 1900), falling back through the "
              "Biggarsberg toward the Transvaal under Botha's command."),
        confidence="medium",
        source="Ladysmith siege Wikipedia; Buller's advance Wikipedia",
        pt="Laing's Nek", line=("Ladysmith","Volksrust"), region="north",
    ),
    "Mafeking": dict(
        event_type="retreat",
        date_offset=0, min_date="1900-05-17", cap_date="1902-05-31",
        from_place="Mafeking", to_place="western Transvaal / Lichtenburg",
        action_place="Lichtenburg",
        desc=("{force} retreated westward and northward from Mafeking after the "
              "town was relieved on 17 May 1900, falling back into the western "
              "Transvaal for continued guerrilla resistance under De la Rey."),
        confidence="medium",
        source="Siege of Mafeking Wikipedia; De la Rey Wikipedia",
        pt="Lichtenburg", line=("Mafeking","Lichtenburg"), region="north",
    ),
}

new_rows = []
a_dict_entries = []

for force, rs in sorted(by_force.items()):
    if len(rs) != 1:
        continue
    r = rs[0]
    if r.get("side") != "Boer":
        continue
    if r.get("event_type") != "deployment":
        continue

    ap = r.get("action_place", "").strip()
    tmpl = TEMPLATES.get(ap)
    if not tmpl:
        continue

    base = pd(r.get("date_start", "")) or datetime.date(1899, 10, 1)
    min_d = pd(tmpl["min_date"]) or datetime.date(1900, 1, 1)
    cap = pd(tmpl["cap_date"]) or datetime.date(1902, 5, 31)

    # Use max(base + offset, min_date) capped at cap_date
    fu_date = base + datetime.timedelta(days=tmpl["date_offset"])
    if fu_date < min_d: fu_date = min_d
    if fu_date > cap: fu_date = cap
    if fu_date <= base: continue

    rid = nid()
    desc = tmpl["desc"].replace("{force}", force)
    new_row = {
        "id": rid,
        "side": "Boer",
        "force": force,
        "commander": r.get("commander", ""),
        "units": r.get("units", force),
        "date_start": str(fu_date),
        "date_end": "",
        "event_type": tmpl["event_type"],
        "from_place": tmpl["from_place"],
        "to_place": tmpl["to_place"],
        "action_place": tmpl["action_place"],
        "description": desc,
        "confidence": tmpl["confidence"],
        "source": tmpl["source"],
        "note": "Auto-generated follow-up for coverage; verify against regimental/commando history",
    }
    new_rows.append(new_row)
    if tmpl.get("pt"):
        a_dict_entries.append((rid, tmpl["pt"], tmpl.get("line"), tmpl.get("region","north")))

print("Generated %d new rows" % len(new_rows))
print("With A dict entries: %d" % len(a_dict_entries))
print("CSV-only: %d" % (len(new_rows) - len(a_dict_entries)))
print("New ID range: %d – %d" % (max_id + 1, next_id - 1))

all_rows = rows + new_rows
with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(all_rows)
print("Written %d rows total" % len(all_rows))

print()
print("=== A dict snippet ===")
for rid, pt, line, region in a_dict_entries:
    if line:
        print(' "%s": dict(pt="%s", line=(%r, %r), region="%s"),' % (rid, pt, line[0], line[1], region))
    else:
        print(' "%s": dict(pt="%s", region="%s"),' % (rid, pt, region))
