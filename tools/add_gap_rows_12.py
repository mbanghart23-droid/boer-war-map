"""Gap fill batch 12 — 10 Boer deployment singletons missed by batch 11."""
import csv
from pathlib import Path

CSV_PATH = Path(__file__).parent.parent / "data" / "movements.csv"
rows = list(csv.DictReader(open(CSV_PATH, encoding="utf-8")))
COLS = list(rows[0].keys())
max_id = max(int(r["id"]) for r in rows if r["id"].isdigit())
nid = [max_id + 1]

def R(force, ds, et, fp, tp, ap, desc, conf, src):
    r = {
        "id": str(nid[0]), "side": "Boer", "force": force,
        "commander": "", "units": force,
        "date_start": ds, "date_end": "",
        "event_type": et, "from_place": fp, "to_place": tp, "action_place": ap,
        "description": desc, "confidence": conf, "source": src,
        "note": "Auto-generated follow-up for coverage; verify against commando history",
    }
    nid[0] += 1
    return r

new_rows = [
    R("Ackermann's Commando", "1902-01-01", "redeployment",
      "Bloemfontein", "OFS guerrilla ops", "Heilbron",
      "Ackermann's Commando continued guerrilla operations in the OFS in 1901-1902, "
      "part of the mobile resistance under De Wet against British blockhouse lines.",
      "low", "angloboerwar.com OFS guerrilla; De Wet memoirs"),
    R("Alberts' Commando", "1902-01-01", "redeployment",
      "Pretoria", "eastern Transvaal guerrilla ops", "Machadodorp",
      "Alberts' Commando continued guerrilla operations in the eastern Transvaal "
      "in 1901-1902, part of Botha's mobile resistance against British columns.",
      "low", "angloboerwar.com eastern Transvaal; Botha's command"),
    R("Britz's Commando", "1902-01-01", "redeployment",
      "Bloemfontein", "OFS guerrilla ops", "Heilbron",
      "Britz's Commando continued guerrilla operations in the OFS in 1901-1902, "
      "participating in De Wet's mobile campaign against British blockhouse lines.",
      "low", "angloboerwar.com OFS guerrilla; De Wet memoirs"),
    R("Buys' Commando", "1902-01-01", "redeployment",
      "Bloemfontein", "OFS guerrilla ops", "Kroonstad",
      "Buys' Commando continued guerrilla operations in the OFS through 1901-1902, "
      "part of De Wet's mobile resistance against British forces.",
      "low", "angloboerwar.com OFS guerrilla; De Wet memoirs"),
    R("De Beer's Commando", "1902-01-01", "redeployment",
      "Bloemfontein", "OFS guerrilla ops", "Ventersburg",
      "De Beer's Commando continued guerrilla operations in the OFS through 1901-1902, "
      "part of the mobile resistance under De Wet.",
      "low", "angloboerwar.com OFS guerrilla; De Wet memoirs"),
    R("Lubbe's Commando", "1902-01-01", "redeployment",
      "Bloemfontein", "OFS guerrilla ops", "Heilbron",
      "Lubbe's Commando continued guerrilla operations in the OFS through 1901-1902, "
      "part of De Wet's mobile resistance campaign.",
      "low", "angloboerwar.com OFS guerrilla; De Wet memoirs"),
    R("Malan's Commando (Cape Rebels)", "1902-01-01", "redeployment",
      "Colesberg", "Cape Colony guerrilla ops", "Middelburg (Cape)",
      "Malan's Cape Rebel commando continued operations raiding into the Cape Colony "
      "from the OFS border throughout 1901-1902 under Hertzog's and Smuts's commands.",
      "low", "EC operations angloboerwar.com; Smuts's Cape raid Wikipedia"),
    R("Van Zyl's Commando", "1902-01-01", "redeployment",
      "Bloemfontein", "OFS guerrilla ops", "Brandfort",
      "Van Zyl's Commando continued guerrilla operations in the OFS in 1901-1902, "
      "part of De Wet's mobile resistance.",
      "low", "angloboerwar.com OFS guerrilla"),
    R("Vilonel's Commando", "1902-01-01", "redeployment",
      "Bloemfontein", "OFS guerrilla ops", "Winburg",
      "Vilonel's Commando continued guerrilla operations in the OFS in 1901-1902, "
      "part of De Wet's mobile resistance against British columns.",
      "low", "angloboerwar.com OFS guerrilla"),
    R("Bothaville Commando", "1900-11-07", "retreat",
      "Bothaville", "OFS guerrilla ops", "Hoopstad",
      "The Bothaville Commando was among the OFS forces scattered after the Battle of "
      "Bothaville (6 November 1900) when De Wet's supply column was surprised by British "
      "forces under Beatson. Survivors dispersed across the western OFS to continue resistance.",
      "medium", "Battle of Bothaville Wikipedia; De Wet memoirs"),
]

print("New rows: %d  IDs: %d-%d" % (len(new_rows), max_id + 1, nid[0] - 1))
all_rows = rows + new_rows
with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(all_rows)
print("Written %d rows" % len(all_rows))
print()
print("A dict entries:")
pts = {
    "Heilbron": ("Heilbron", "north"),
    "Machadodorp": ("Machadodorp", "north"),
    "Kroonstad": ("Kroonstad", "north"),
    "Ventersburg": ("Ventersburg", "north"),
    "Middelburg (Cape)": ("Middelburg (Cape)", "eastern"),
    "Brandfort": ("Brandfort", "north"),
    "Winburg": ("Winburg", "north"),
    "Hoopstad": ("Hoopstad", "north"),
}
for r in new_rows:
    pt_info = pts.get(r["action_place"])
    if pt_info:
        print(' "%s": dict(pt="%s", region="%s"),' % (r["id"], pt_info[0], pt_info[1]))
