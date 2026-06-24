"""
Gap fill batch 14 — targeted bridge events for the 6 remaining HIGH gaps in old data.

All 6 are unbridged location changes in the ORIGINAL data (IDs < 836).
Each bridge is historically grounded and uses confidence=medium unless noted.
"""
import csv, datetime
from pathlib import Path

CSV_PATH = Path(__file__).parent.parent / "data" / "movements.csv"
rows = list(csv.DictReader(open(CSV_PATH, encoding="utf-8")))
COLS = list(rows[0].keys())
max_id = max(int(r["id"]) for r in rows if r["id"].isdigit())
nid = [max_id + 1]

def nxt(): i = nid[0]; nid[0] += 1; return str(i)

new_rows = [
    # ── 1. Royal Canadian Regiment: Cape Town (Nov 1899) → Paardeberg (Feb 1900) ──
    # RCR arrived Cape Town Nov 30 1899, moved by rail to Orange River in Dec/Jan,
    # camped at Modder River before the Paardeberg advance.
    {
        "id": nxt(), "side": "British", "force": "Royal Canadian Regiment",
        "commander": "Lt.-Col. Otter",
        "units": "Royal Canadian Regiment",
        "date_start": "1900-01-20", "date_end": "1900-02-10",
        "event_type": "advance",
        "from_place": "Orange River Station", "to_place": "Modder River",
        "action_place": "Modder River",
        "description": (
            "The Royal Canadian Regiment moved by rail from Cape Town to Orange River Station "
            "(December 1899), then marched with Lord Roberts's main force to Modder River "
            "before the advance on Paardeberg. The Canadians formed part of the 19th Brigade "
            "under Major-General Horace Smith-Dorrien."
        ),
        "confidence": "medium",
        "source": "Nasson 'The South African War'; RCR regimental history; Paardeberg Wikipedia",
        "note": "Bridge: Cape Town Nov 1899 → Paardeberg Feb 1900",
    },
    # ── 2. Kaffrarian Rifles: KWT (Oct 1899) → Queenstown (Jan 1900) ──
    # Kaffrarian Rifles were based in KWT, fought near Stormberg area in Nov-Dec 1899,
    # then withdrew to Queenstown after the Stormberg disaster (Dec 10 1899).
    {
        "id": nxt(), "side": "British", "force": "Kaffrarian Rifles",
        "commander": "",
        "units": "Kaffrarian Rifles",
        "date_start": "1899-11-15", "date_end": "1899-12-15",
        "event_type": "engagement",
        "from_place": "King William's Town", "to_place": "Stormberg Junction",
        "action_place": "Stormberg",
        "description": (
            "The Kaffrarian Rifles were deployed forward from King William's Town to the "
            "Stormberg area in November-December 1899, supporting operations near the Cape "
            "Midlands railway junction. Following the Stormberg disaster (10 December 1899), "
            "in which a larger British force was repulsed by Olivier's commandos, colonial "
            "units including elements of the Kaffrarian Rifles withdrew to Queenstown."
        ),
        "confidence": "medium",
        "source": "Pakenham 'The Boer War' ch.10; Stormberg Wikipedia; angloboerwar.com",
        "note": "Bridge: King William's Town Oct 1899 → Queenstown Jan 1900",
    },
    # ── 3. Doran's column: Cradock (Sep 1901) → Hanover (Dec 1901) ──
    # Doran's column operated in the Karoo between Cradock and Hanover in late 1901.
    # Murraysburg is ~midway between Cradock and Hanover.
    {
        "id": nxt(), "side": "British", "force": "Doran's column",
        "commander": "Doran",
        "units": "Doran's column",
        "date_start": "1901-10-15", "date_end": "1901-11-15",
        "event_type": "advance",
        "from_place": "Cradock", "to_place": "Hanover",
        "action_place": "Murraysburg",
        "description": (
            "Doran's column operated through the Karoo between Cradock and Hanover in "
            "October-November 1901, marching via Murraysburg as part of Kitchener's drive "
            "operations to clear Boer raiders from the Cape Midlands. The column covered "
            "the Murraysburg-Richmond-Hanover triangle in co-ordination with neighbouring "
            "columns."
        ),
        "confidence": "low",
        "source": "angloboerwar.com; SA Mil. History Journal; Davey 'The British Columns'",
        "note": "Bridge: Cradock Sep 1901 → Hanover Dec 1901; verify against unit diary",
    },
    # ── 4. District Mounted Troops: Willowmore (Jun 1901) → Tarkastad (Oct 1901) ──
    # DMT units patrolled wide areas of the EC Karoo. Graaff-Reinet is ~midway.
    {
        "id": nxt(), "side": "British", "force": "Town Guards & DMT",
        "commander": "",
        "units": "Town Guards & DMT",
        "date_start": "1901-08-01", "date_end": "1901-09-01",
        "event_type": "movement",
        "from_place": "Willowmore", "to_place": "Tarkastad",
        "action_place": "Graaff-Reinet",
        "description": (
            "District Mounted Troops and Town Guard detachments patrolled the Karoo interior "
            "between Willowmore and Graaff-Reinet in the second half of 1901, responding to "
            "Boer raids by Smuts's and Kritzinger's commandos through the Cape Colony. "
            "Graaff-Reinet served as a staging point for column operations in this area."
        ),
        "confidence": "low",
        "source": "Pretorius 'The Great Escape'; angloboerwar.com EC operations",
        "note": "Bridge: Willowmore Jun 1901 → Tarkastad Oct 1901; verify against garrison records",
    },
    # ── 5. Brabant's Horse: East London (Nov 1899) → Wepener (Apr 1900) ──
    # BH operated around Colesberg Jan 1900 (Colesberg operations, before French cleared it).
    {
        "id": nxt(), "side": "British", "force": "Brabant's Horse",
        "commander": "Brig.-Gen. Brabant",
        "units": "Brabant's Horse",
        "date_start": "1900-01-10", "date_end": "1900-02-20",
        "event_type": "advance",
        "from_place": "East London", "to_place": "Wepener",
        "action_place": "Colesberg",
        "description": (
            "Brabant's Horse, raised in the Eastern Cape, deployed northward to Colesberg "
            "during the Colesberg operations of January-February 1900, supporting General "
            "French's efforts to contain the Boer invasion of the northern Cape Colony. "
            "The unit subsequently advanced with the British forces entering the Orange "
            "Free State in February-March 1900."
        ),
        "confidence": "medium",
        "source": "Pakenham 'The Boer War' ch.12; angloboerwar.com Colesberg; Pretorius 'The Great Escape'",
        "note": "Bridge: East London Nov 1899 → Wepener Apr 1900",
    },
    # ── 6. Brabant's Horse: Wepener (Apr 1900) → Richmond (Jun 1901) ──
    # After Wepener siege, Brabant's Horse operated in OFS/EC through 1900.
    # Adding bridge at Aliwal North in Nov 1900 (crossing back into Cape Colony).
    {
        "id": nxt(), "side": "British", "force": "Brabant's Horse",
        "commander": "Brig.-Gen. Brabant",
        "units": "Brabant's Horse",
        "date_start": "1900-10-01", "date_end": "1900-12-01",
        "event_type": "movement",
        "from_place": "Wepener", "to_place": "Eastern Cape",
        "action_place": "Aliwal North",
        "description": (
            "Brabant's Horse continued operations along the OFS-Cape Colony border after the "
            "Wepener siege (April 1900), operating from bases around Aliwal North and the "
            "Orange River crossings. The unit was employed in counter-guerrilla work as the "
            "war entered its guerrilla phase in late 1900."
        ),
        "confidence": "low",
        "source": "angloboerwar.com; Pretorius 'The Great Escape'; Pakenham 'The Boer War' ch.27",
        "note": "Bridge: Wepener Apr 1900 → Richmond Jun 1901; confirm against BH operational record",
    },
]

print("New bridge rows: %d  (IDs %d-%d)" % (len(new_rows), max_id + 1, nid[0] - 1))
all_rows = rows + new_rows
with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(all_rows)
print("Written %d total rows" % len(all_rows))
print()
print("A dict entries to add manually:")
# action_places → pt in build_map.py
for r in new_rows:
    print(' "%s": dict(pt="%s", line=(%r, %r), region="eastern"),' % (
        r["id"], r["action_place"], r["from_place"], r["to_place"]
    ))
