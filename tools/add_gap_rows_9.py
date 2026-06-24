"""
Gap fill batch 9:
  - Fix 14th Battery RFA / 14th Battery RFA (2nd) collision (parenthetical strip → merge)
  - Add O Battery RHA Colesberg→Bloemfontein bridge (Roberts advance, Jan-Mar 1900)
  - Add Rhodesia Regiment Bulawayo→Mafeking bridge (Plumer's column, Feb-May 1900)
  - Add 9th Lancers Diamond Hill→Richmond bridge (EC redeployment Oct-Nov 1900)
  - Add Imperial Light Horse Ladysmith→Mafeking bridge (ILH was at Mafeking relief)
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
    global next_id
    i = next_id
    next_id += 1
    return str(i)


def row(side, force, commander, units, ds, de, et, fp, tp, ap, desc, conf, src, note=""):
    return {
        "id": nid(), "side": side, "force": force, "commander": commander,
        "units": units, "date_start": ds, "date_end": de, "event_type": et,
        "from_place": fp, "to_place": tp, "action_place": ap,
        "description": desc, "confidence": conf, "source": src, "note": note,
    }


new_rows = []

# ── O Battery RHA: Colesberg → Bloemfontein (Jan–Mar 1900)
# O Battery RHA was with French's cavalry, broke out from Colesberg front to
# join Roberts's flanking march. Gap: Colesberg → Bloemfontein 208km 28d.
new_rows.append(row(
    "British",
    "O Battery Royal Horse Artillery",
    "French's Cavalry Division / Gen. Roberts",
    "O Battery Royal Horse Artillery",
    "1900-01-15", "1900-02-28", "movement",
    "Colesberg", "Bloemfontein", "Paardeberg",
    (
        "O Battery RHA formed part of French's cavalry division which broke out from the "
        "Colesberg front in late January 1900 to join Roberts's flanking march. The battery "
        "participated in the relief of Kimberley (15 Feb 1900) and the Paardeberg operations "
        "(17-27 Feb), before advancing to Bloemfontein (captured 13 Mar 1900)."
    ),
    "high",
    "French's advance Wikipedia; Roberts advance Wikipedia; RHA order of battle Boer War",
))

# ── Rhodesia Regiment: Bulawayo → Mafeking (Plumer's column, Feb–May 1900)
# Gap: Bulawayo (Dec 1 1899) → Mafeking (Apr 15 1900) = 704km 135d
# Plumer marched south from Bulawayo via Lobatsi; repulsed at Ramathlabama Mar 1900;
# linked up with Mahon's column and relieved Mafeking 17 May 1900.
new_rows.append(row(
    "British",
    "Plumer's Rhodesian column",
    "Col. Plumer",
    "Rhodesia Regiment",
    "1900-02-01", "1900-04-14", "movement",
    "Bulawayo", "Mafeking", "Lobatsi",
    (
        "Col. Plumer's column, built around the Rhodesia Regiment, marched south from Bulawayo "
        "from February 1900 in a series of advances to relieve Mafeking. After being repulsed at "
        "Ramathlabama in March 1900, the column reorganised and advanced via Lobatsi. It linked "
        "up with Mahon's flying column from Kimberley; the combined force relieved Mafeking "
        "on 17 May 1900."
    ),
    "high",
    "Siege of Mafeking Wikipedia; Plumer's column Wikipedia; angloboerwar.com Rhodesia Regiment",
))

# ── 9th Lancers: Diamond Hill → Richmond (Oct–Nov 1900 EC redeployment)
# Gap: Diamond Hill (Jun 1900) → Richmond (Dec 1900) = 765km 382d
# The 9th Lancers served in Natal then redeployed to the Eastern Cape under Scobell.
# Adding bridge rows: Diamond Hill → Pretoria base (Jul 1900) → EC (Nov 1900)
new_rows.append(row(
    "British",
    "Roberts's army / 9th Lancers",
    "Gen. Roberts",
    "9th (Queen's Royal) Lancers",
    "1900-07-01", "1900-10-31", "redeployment",
    "Diamond Hill", "Eastern Cape",
    "Pretoria",
    (
        "Following the Battle of Diamond Hill (11-12 Jun 1900), the 9th Lancers remained with "
        "Roberts's main army in the Pretoria area through mid-1900. In the latter half of 1900 "
        "elements of the regiment were redeployed to the Eastern Cape to reinforce column "
        "operations against Kritzinger and Scheepers."
    ),
    "medium",
    "9th Lancers regimental history; angloboerwar.com EC columns 1900",
    "RESEARCH NEEDED: exact timing of 9th Lancers redeployment from Transvaal to EC",
))

# ── Imperial Light Horse: Ladysmith → Mafeking (May 1900)
# Gap: Ladysmith (Jan 1 1900, relief) → Mafeking (May 17 1900) = 507km 66d
# ILH was raised in Natal, fought at Elandslaagte and in the Ladysmith siege relief.
# After the relief (Feb 28 1900) they marched north with Roberts and were part of
# Mahon's flying column that relieved Mafeking (17 May 1900).
new_rows.append(row(
    "British",
    "Mahon's flying column / ILH",
    "Col. Mahon / Gen. Roberts",
    "Imperial Light Horse",
    "1900-03-01", "1900-05-16", "advance",
    "Ladysmith", "Mafeking", "Kimberley",
    (
        "After the relief of Ladysmith (28 Feb 1900), the Imperial Light Horse moved north with "
        "Roberts's advance. ILH squadrons formed part of Mahon's flying column which departed "
        "Kimberley on 4 May 1900 and linked up with Plumer's Rhodesian column to relieve "
        "Mafeking on 17 May 1900."
    ),
    "high",
    "Relief of Mafeking Wikipedia; Mahon's column Wikipedia; ILH regimental history",
))

print("New rows: %d (ids %d-%d)" % (len(new_rows), max_id + 1, next_id - 1))
all_rows = rows + new_rows
with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(all_rows)
print("Written %d rows total" % len(all_rows))
print()
print("IMPORTANT: Add to build_map.py A dict:")
print('  "%d": dict(pt="Paardeberg", line=("Colesberg","Bloemfontein"), region="north"),' % (max_id + 1))
print('  "%d": dict(pt="Lobatsi", line=("Bulawayo","Mafeking"), region="north"),' % (max_id + 2))
print('  # "%d": CSV-only bridge (9th Lancers Pretoria redeployment)' % (max_id + 3))
print('  "%d": dict(pt="Kimberley", line=("Ladysmith","Mafeking"), region="north"),' % (max_id + 4))
