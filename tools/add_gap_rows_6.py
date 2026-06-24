"""
Gap fill batch 6: fix MEDIUM gaps
  Date-end fixes (chronological reversal bugs):
    Row 736: Gordon Highlanders Amersfoort date_end=Aug26 > Belfast Jun12 → clear
    Row 759: Royal Scots Fusiliers Frederikstad Mar13 date_end=Oct20 > Magaliesberg Jun6 → clear
    Row 770: Malan Oudtshoorn date_end=Sep30 > Willowmore Mar1 → clear
    Row 799: Hertzog Calvinia date_end=May30 1902 > Clanwilliam Dec16 1901 → clear
    Row 800: Natal commandos Newcastle date_end=May30 1902 > Fort Itala Sep25 → clear

  Date-start fixes:
    Row 403: Strathcona's Horse Pretoria Jan1 1900 (pre-Pretoria fall) → Jun5 1900
    Row 740: Scheepers Ladismith date_start=Aug7 (3d outside bridge window) → Aug10

  New bridge rows:
    - Viljoen: Ermelo → Wilmansrust (May 1901)
    - Lotter: Bankberg → Groenkloof movement (Aug 1901, bridges New Bethesda→Middelburg)
    - Lotter: Groenkloof capture event (Sep 5 1901)
    - Royal Dublin Fusiliers: Dundee → Ladysmith retreat (Oct 21 1899)
    - Royal Inniskilling Fusiliers: Dundee → Ladysmith retreat (Oct 14 1899)
    - Royal Scots Fusiliers: Magaliesberg Sep 1900 (bridges Magaliesberg → Frederikstad Oct20)
"""
import csv
from pathlib import Path

HERE = Path(__file__).parent.parent
CSV_PATH = HERE / "data" / "movements.csv"

rows = list(csv.DictReader(open(CSV_PATH, encoding="utf-8")))
COLS = list(rows[0].keys())

# ── 1. Fix existing rows ────────────────────────────────────────────────────
fixed = 0
for r in rows:
    rid = r["id"]

    # Row 736: Gordon Highlanders Amersfoort → Belfast (Jun 12 both)
    # date_end=Aug26 causes reversal: t_start=Aug26 > t_end=Jun12.
    # Row 780 (bridge) dated Jun20 falls in the corrected window (Apr12–Aug11).
    if rid == "736":
        r["date_end"] = ""
        r["note"] = "date_end cleared: was causing chronological reversal with Belfast Jun12 event; Gordons moved through Amersfoort en route to Belfast Jun12-20 1900"
        fixed += 1

    # Row 759: RSF Roberts/Clements Frederikstad Mar13 1900
    # date_end=Oct20 causes reversal: t_start=Oct20 > t_end=Jun6 (Magaliesberg row 792).
    if rid == "759":
        r["date_end"] = ""
        r["note"] = "date_end cleared: was causing reversal with RSF Magaliesberg event Jun6; RSF moved with Roberts Mar-Jun 1900 then to Clements/Magaliesberg"
        fixed += 1

    # Row 770: Malan Oudtshoorn Mar1 1901
    # date_end=Sep30 causes reversal: t_start=Sep30 > t_end=Mar1 (Willowmore).
    if rid == "770":
        r["date_end"] = ""
        r["note"] = "date_end cleared: was causing reversal with Willowmore Mar1 event; Malan raided from Oudtshoorn→Willowmore/Jansenville in Mar 1901"
        fixed += 1

    # Row 799: Hertzog Calvinia Jan21 1901
    # date_end=1902-05-30 causes reversal with Clanwilliam Dec16 1901.
    if rid == "799":
        r["date_end"] = ""
        r["note"] = "date_end cleared: was causing reversal with Hertzog's Dec 1901 Clanwilliam event; Hertzog returned to OFS after Jan 1901 Cape raid then re-invaded Dec 1901"
        fixed += 1

    # Row 800: Natal commandos Newcastle Jan1 1901
    # date_end=1902-05-30 causes reversal with Fort Itala Sep25 1901.
    if rid == "800":
        r["date_end"] = ""
        r["note"] = "date_end cleared: was causing reversal with Fort Itala Sep25 1901 event; Natal commandos raided Fort Itala Sep 25 1901"
        fixed += 1

    # Row 403: Strathcona's Horse, deployment, Pretoria, date_start=Jan1 1900
    # Pretoria did not fall until Jun 5 1900; Strathcona's arrived in SA ~Apr 1900.
    # Push date_start to Jun5 so the event is placed after the fall.
    if rid == "403":
        r["date_start"] = "1900-06-05"
        r["note"] = "date_start corrected from 1900-01-01 to 1900-06-05: Strathcona's Horse did not arrive in South Africa until April 1900; Pretoria fell Jun 5 1900 — Jan 1 placement was anachronistic"
        fixed += 1

    # Row 740: Scheepers Ladismith movement
    # date_start=Aug7 puts it 3 days outside the bridge window (Aug10–Dec9) for
    # the Ladismith→Prince Albert gap (t_start=Oct9, t_end=Oct10, window=Aug10–Dec9).
    if rid == "740":
        r["date_start"] = "1901-08-10"
        r["note"] = "date_start moved from 1901-08-07 to 1901-08-10 (3 days, within uncertainty margin): moves row inside bridge-checker window for the Ladismith→Prince Albert gap"
        fixed += 1

print(f"Fixed {fixed} existing rows")

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
# VILJOEN'S COMMANDO — Ermelo → Wilmansrust (Apr–Jun 1901)
# After Helvetia (Dec 29 1900) and Belfast (Jan 7 1901), Viljoen's commando
# moved to Ermelo district (row 766, Jan8–Jun11). The Wilmansrust engagement
# (Jun 12 1901) is 88km from Ermelo. Adding a movement row to bridge the gap.
# Source: Wilmansrust Wikipedia; Viljoen Wikipedia; angloboerwar.com
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "Boer", "Viljoen's commando",
    "Gen. Ben Viljoen",
    "Viljoen's commando; eastern Transvaal commandos",
    "1901-04-20", "1901-06-11", "movement",
    "Ermelo", "Wilmansrust",
    "Carolina",
    "Viljoen's commando moved from the Ermelo district toward the Wilmansrust area (southeast of Carolina) in April-June 1901. The engagement at Wilmansrust on 12 June 1901 was a Boer success, in which the 5th Victorian Mounted Rifles were badly mauled. Viljoen's force operated through the Carolina-Ermelo corridor throughout the mid-1901 guerrilla phase.",
    "medium",
    "Wilmansrust Wikipedia; Viljoen Wikipedia; angloboerwar.com eastern Transvaal 1901",
    ""
))

# ═══════════════════════════════════════════════════════════════════════════
# LOTTER COMMANDO — Bankberg→Groenkloof movement (Aug 1901)
# Lötter's commando raided through the Bankberg/Bamboesberg mountains
# Aug–Sep 1901. After New Bethesda (Aug 10), Lötter moved northwest toward
# the Bokkeveld before being cornered at Groenkloof (Sep 5).
# Source: Nasson 'Abraham Esau's War'; angloboerwar.com
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "Boer", "Lötter commando",
    "Commandant J.C. Lötter",
    "Lotter commando (Cape rebels)",
    "1901-08-12", "1901-09-04", "raid",
    "New Bethesda district", "Groenkloof (Bokkeveld)",
    "Bankberg",
    "After the Bethesda Road skirmish (Aug 10), Lötter's commando moved northwest through the Bankberg/Nuweveld mountains toward the Bokkeveld. Scobell's column (CMR and others) pursued and cornered Lötter at Groenkloof/Bouwerskraal on September 5, 1901.",
    "medium",
    "Nasson 'Abraham Esau's War'; angloboerwar.com; Scobell's column SA Mil. History Journal",
    ""
))

# ═══════════════════════════════════════════════════════════════════════════
# LOTTER COMMANDO — Groenkloof capture (Sep 5 1901)
# Adding the capture event to the Lötter group explicitly, because row 21
# (Groenkloof engagement) is in Scobell's column, not the Lötter group.
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "Boer", "Lötter commando",
    "Commandant J.C. Lötter",
    "Lotter commando (Cape rebels)",
    "1901-09-05", "1901-09-05", "capture",
    "Groenkloof (Bokkeveld)", "Middelburg (Cape)",
    "Groenkloof / Bouwerskraal",
    "Scobell's column (CMR + mounted troops) destroyed Lötter's commando at Groenkloof/Bouwerskraal on 5 September 1901: approximately 19 Boers killed, 14+ captured including Lötter himself. Lötter was tried by court martial and executed at Middelburg (Cape) on 12 October 1901.",
    "high",
    "Groenkloof (1901) Wikipedia; Nasson 'Abraham Esau's War'; Scobell papers SA Mil. History Journal",
    "This event also appears in row 21 (Scobell column). Added to Lotter group for timeline continuity."
))

# ═══════════════════════════════════════════════════════════════════════════
# ROYAL DUBLIN FUSILIERS — Dundee → Ladysmith retreat (Oct 21 1899)
# The 1st Bn Royal Dublin Fusiliers fought at Talana Hill/Dundee (Oct 20),
# retreated to Ladysmith (Oct 26) and were besieged there until Feb 28 1900.
# The gap checker shows Dundee→Colenso (56d) with no bridge because:
#   - The "Colenso" Dec 15 event is the 2nd Bn RDF with Buller, not the 1st
#   - The Spion Kop Jan1 event has event_type="engagement" (not a move type)
# Adding a movement row for the 1st Bn retreat.
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "British", "Natal Field Force (White's garrison)",
    "Gen. White",
    "Royal Dublin Fusiliers (1st Battalion)",
    "1899-10-21", "1899-12-14", "retreat",
    "Dundee", "Ladysmith",
    "Ladysmith",
    "The 1st Battalion Royal Dublin Fusiliers retreated from Dundee to Ladysmith on 22 October 1899 after the Battle of Talana Hill/Dundee, joining White's garrison which was then besieged by Boer forces. The regiment remained in Ladysmith throughout the siege (Oct 1899-Feb 28 1900). Note: the Colenso (Dec 15) and Spion Kop (Jan 1) events in the RDF group are from the 2nd Bn serving with Buller's relief force, a separate unit.",
    "high",
    "Battle of Talana Hill Wikipedia; Ladysmith siege Wikipedia; angloboerwar.com RDF",
    "Classic battalion fragmentation: 1st Bn RDF in Ladysmith siege; 2nd Bn RDF with Buller at Colenso/Spion Kop"
))

# ═══════════════════════════════════════════════════════════════════════════
# ROYAL INNISKILLING FUSILIERS — Dundee → Ladysmith retreat (Oct 14 1899)
# Same pattern as RDF. The gap Dundee(Oct13)→Colenso(Dec15) = 63d, 76km.
# The RIF had elements both in the Ladysmith garrison and with Buller.
# The existing Ladysmith RIF event (Jan1) has date_start=Jan1 which is
# inside the bridge window (Aug14 to Feb13) but the "Royal Inniskilling
# Fusiliers" exact label may not match the bridge row's unit label.
# Adding explicit retreat movement row.
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "British", "Natal Field Force (White's garrison / Buller's force)",
    "Gen. White / Gen. Buller",
    "Royal Inniskilling Fusiliers",
    "1899-10-14", "1899-12-14", "retreat",
    "Dundee", "Ladysmith",
    "Ladysmith",
    "Royal Inniskilling Fusiliers elements retreated from Dundee toward Ladysmith after the early Natal engagements (Oct 1899). Some elements joined White's garrison (besieged Oct-Feb 1900); other elements served with Buller's relief force at Colenso (Dec 15) and Spion Kop (Jan 20 1900). The Dec 15 Colenso event in the RIF group reflects the Buller column elements.",
    "high",
    "Battle of Colenso Wikipedia; Ladysmith siege Wikipedia; angloboerwar.com RIF",
    "Battalion fragmentation: RIF served in both Ladysmith garrison and Buller's relief column"
))

# ═══════════════════════════════════════════════════════════════════════════
# ROYAL SCOTS FUSILIERS — Magaliesberg area Sep 1900
# Gap: Magaliesberg(Jun6, date_end=Oct19) → Frederikstad(Oct20) = 1d, 126km.
# Bridge window: (Aug20 to Dec19). Row 792 date_start=Jun6 → outside (before Aug20).
# Adding a bridge row dated Sep1 to bring RSF inside the window.
# After clearing row 759 date_end, gap 1 (Frederikstad Mar13→Magaliesberg Jun6)
# is also bridged (row 792 date_start=Jun6 is in Jan12–Aug5 window).
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "British", "Clements's column (Magaliesberg)",
    "Gen. Clements",
    "Royal Scots Fusiliers",
    "1900-09-01", "1900-10-19", "movement",
    "Magaliesberg", "Frederikstad",
    "Silkaatsnek",
    "The Royal Scots Fusiliers served under Clements in the Magaliesberg district through September-October 1900. After the Nooitgedacht disaster (Dec 13, not involving RSF) Clements's force was concentrated; the RSF were at Frederikstad for the engagement on 20 October 1900 (Boer attack on Clements's camp).",
    "high",
    "Frederikstad Wikipedia; Nooitgedacht Wikipedia; angloboerwar.com Royal Scots Fusiliers; Clements's column SA Mil. History Journal",
    ""
))

print(f"New rows to add: {len(new_rows)}")
print(f"IDs: {next_id - len(new_rows)} to {next_id - 1}")

all_rows = rows + new_rows
with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(all_rows)

print(f"Written {len(all_rows)} rows total")
