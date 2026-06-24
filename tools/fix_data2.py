"""
fix_data2.py  –  apply data fixes to data/movements.csv
Run from the boer-war-eastern-cape directory:
    python tools/fix_data2.py
"""

import csv
import re
import pathlib

CSV_PATH = pathlib.Path("data/movements.csv")

FIELDS = [
    "id", "side", "force", "commander", "units",
    "date_start", "date_end", "event_type",
    "from_place", "to_place", "action_place",
    "description", "confidence", "source", "note",
]

# ── helpers ─────────────────────────────────────────────────────────────────

def fix_double_period(s):
    """Remove trailing double-period e.g. 'R.H..' → 'R.H.'"""
    return re.sub(r'\.\.+', '.', s)

def reformat_commander(name):
    """
    Normalise a commander name to 'Lastname, Title? Initials/Firstname' format.
    Rules
    -----
    1. Already in 'Lastname, ...' form → just fix double-periods and return.
    2. 'J.D.P. French'  (initials then surname) → 'French, J.D.P.'
    3. 'Louis Botha'    (two capitalised words) → 'Botha, Louis'
    4. Anything else → return as-is after period fix.
    """
    if not name or not name.strip():
        return name
    name = name.strip()
    name = fix_double_period(name)

    # already in Lastname, ... form
    if ',' in name:
        return name

    # pattern: one or more dot-separated initial groups followed by a capitalised surname
    # e.g. "J.D.P. French" or "Sir R.H. Buller"
    m = re.match(
        r'^((?:[A-Z][a-z]*\.?\s+)*)'    # optional prefix words (Sir, Gen, etc.) – greedy
        r'((?:[A-Z]\.)+)\s+'            # initials block  e.g. "J.D.P. "
        r'([A-Z][a-zA-Z\'\-]+)$',       # surname
        name
    )
    if m:
        prefix = m.group(1).strip()
        initials = m.group(2).rstrip('.')  # keep dots between, strip trailing
        surname = m.group(3)
        if prefix:
            return f"{surname}, {prefix} {initials}."
        return f"{surname}, {initials}."

    # pattern: "Firstname Lastname" – exactly two capitalised words, no dots
    m = re.match(r'^([A-Z][a-záéíóúàèìòùäëïöü\'\-]+)\s+([A-Z][a-záéíóúàèìòùäëïöü\'\-]+)$', name)
    if m:
        first, last = m.group(1), m.group(2)
        return f"{last}, {first}"

    return name


# ── FIX 2 – inferred commanders for blank fields ─────────────────────────────

# Map (force_fragment, event_type) → inferred commander
# Only covers the most obvious gaps visible in the data.
INFERRED_COMMANDERS = {
    # commando-mobilisation rows (id 262-412 range) – generic
}

BLANK_CMD_LOOKUP = [
    # (force_fragment_lower, event_types, commander)
    ("natal field force", {"engagement", "defeat"}, "Penn Symons, Sir William"),
    ("ladysmith field force", {"engagement", "defeat", "siege"}, "White, Sir George"),
    ("estcourt", {"engagement"}, "Kitchener, Maj-Gen Walter"),
    ("kritzinger and scheepers", {"move"}, "Kritzinger, P.H.; Scheepers, G."),
    ("ermelo commando", {"engagement", "deployment"}, ""),
    ("harrismith commando", {"deployment"}, ""),
    ("haasbroek", {"deployment"}, "Haasbroek"),
    ("colesberg rebel", {"deployment"}, ""),
    ("prinsloo's commando", {"deployment", "surrender"}, "Prinsloo, Jacob"),
    ("olivier's commando", {"deployment"}, "Olivier, J.H."),
]

ACTIVE_EVENT_TYPES = {
    "engagement", "defeat", "raid", "advance", "capture",
    "siege", "skirmish", "drive", "pursuit", "surrender",
}


def infer_commander(row):
    """Return an inferred commander string or '' if nothing suitable found."""
    force = row["force"].lower()
    et = row["event_type"].lower()
    if et not in ACTIVE_EVENT_TYPES:
        return ""
    for fragment, types, cmd in BLANK_CMD_LOOKUP:
        if fragment in force and et in types:
            return cmd
    return ""


# ── FIX 3 – enriched descriptions ────────────────────────────────────────────

# Each entry: (match_function, new_description)
# match_function receives a row dict and returns True if this is the target row.

ENRICHED_DESCRIPTIONS = [
    # ---- Ladysmith siege ----
    (
        lambda r: (
            "ladysmith" in r["action_place"].lower() or "ladysmith" in r["to_place"].lower()
        ) and r["event_type"] == "siege" and r["side"] == "Boer",
        "Boer forces under Joubert invested Ladysmith 2 Nov 1899, trapping White's 12,000-man garrison. "
        "118-day siege ended 28 Feb 1900 when Buller's Tugela breakthrough opened the relief road. "
        "Pivotal Natal campaign action."
    ),
    # ---- Mafeking siege / Baden-Powell ----
    (
        lambda r: (
            "mafeking" in r["action_place"].lower()
        ) and r["event_type"] == "siege" and r["side"] == "British",
        "Baden-Powell's ~1,200-man garrison withstood 217 days of Boer siege at Mafeking, "
        "13 Oct 1899 – 17 May 1900. Garrison used innovative tactics and sorties; relief by Mahon "
        "and Plumer triggered Empire-wide celebrations."
    ),
    # ---- Kimberley siege ----
    (
        lambda r: (
            "kimberley" in r["action_place"].lower()
        ) and r["event_type"] == "siege" and r["side"] == "British",
        "Kekewich's ~4,000-strong garrison (incl. 2,000 armed civilians) held Kimberley "
        "15 Oct 1899 – 15 Feb 1900. Cecil Rhodes's pressure on the commander complicated "
        "defence; French's cavalry dash finally broke the siege."
    ),
    # ---- Spion Kop ----
    (
        lambda r: (
            "spion kop" in r["action_place"].lower() or "spion kop" in r["description"].lower()
        ) and r["event_type"] in ("defeat", "engagement"),
        "Buller and Warren seized Spion Kop summit 23-24 Jan 1900 but the crest was "
        "dominated by Boer fire from surrounding heights. Thorneycroft held through the night "
        "then abandoned the summit. British ~1,700 casualties; a defining Black Week failure."
    ),
    # ---- Paardeberg (British side) ----
    (
        lambda r: (
            "paardeberg" in r["action_place"].lower() or "paardeberg" in r["to_place"].lower()
        ) and r["event_type"] == "engagement" and r["side"] == "British",
        "Roberts encircled Cronje's 4,000-man laager on the Modder River 18 Feb 1900. "
        "After Kitchener's costly frontal assault on 18 Feb (Paardeberg Drift), the Boers "
        "were starved into surrender on 27 Feb – Majuba Day – opening the road to Bloemfontein."
    ),
    # ---- Paardeberg (Boer surrender) ----
    (
        lambda r: (
            "paardeberg" in r["action_place"].lower()
        ) and r["event_type"] == "surrender",
        "Piet Cronje surrendered ~4,000 burghers to Roberts at Paardeberg on 27 Feb 1900 – "
        "deliberately chosen as the anniversary of Majuba Hill. Largest Boer capitulation to "
        "that date; decisive blow to the conventional Boer war effort."
    ),
    # ---- Elandslaagte ----
    (
        lambda r: "elandslaagte" in r["action_place"].lower()
        and r["event_type"] == "engagement"
        and r["side"] == "British",
        "French and Hamilton routed Kock's commando at Elandslaagte 21 Oct 1899. "
        "Gordon Highlanders and Imperial Light Horse broke the Boer position; "
        "5th Lancers pursued. One of few clear British set-piece victories early in the war; "
        "General Kock mortally wounded."
    ),
    # ---- Talana Hill ----
    (
        lambda r: "talana" in r["action_place"].lower()
        and r["event_type"] == "engagement",
        "Penn Symons's brigade stormed Boer-held Talana Hill at Dundee 20 Oct 1899. "
        "Costly British infantry attack drove the Boers off the summit; Penn Symons was "
        "mortally wounded during the advance. First pitched battle of the war on Natal soil."
    ),
    # ---- Nooitgedacht ----
    (
        lambda r: "nooitgedacht" in r["action_place"].lower()
        and r["event_type"] == "engagement",
        "De la Rey and Beyers surprised Clements's isolated brigade at the foot of the "
        "Magaliesberg 13 Dec 1900. Boers descended the cliffs at dawn; British lost ~600 men "
        "killed, wounded or captured plus all camp stores. Clements extricated a remnant; "
        "a serious reverse in the guerrilla phase."
    ),
    # ---- Tweebosch ----
    (
        lambda r: "tweebosch" in r["action_place"].lower()
        and r["event_type"] == "engagement",
        "De la Rey routed Lord Methuen's column at Tweebosch (Harts River) 7 Mar 1902. "
        "Mounted Boers stampeded Methuen's horses then charged; Methuen was wounded and "
        "captured. Last major Boer field success; Methuen later released on parole."
    ),
    # ---- Rooiwal ----
    (
        lambda r: "rooiwal" in r["action_place"].lower()
        and r["event_type"] == "engagement",
        "Kemp led a 2,000-strong mounted Boer charge at Rooiwal (near Klerksdorp) 11 Apr 1902. "
        "Entrenched British infantry and artillery shattered the attack; ~200 Boers killed. "
        "The last massed offensive action of the war, ending Boer hope of a decisive battlefield reversal."
    ),
    # ---- Diamond Hill ----
    (
        lambda r: "diamond hill" in r["action_place"].lower()
        and r["event_type"] == "engagement",
        "Roberts attacked Botha's line east of Pretoria at Diamond Hill (Donkerhoek) "
        "11-12 Jun 1900. After a day's fighting the Boers withdrew overnight; British "
        "occupied the position. Last major engagement before Botha dispersed into guerrilla warfare."
    ),
    # ---- Bergendal ----
    (
        lambda r: "bergendal" in r["action_place"].lower()
        and r["event_type"] == "engagement",
        "Buller broke the last Boer conventional defensive line at Bergendal kopje near "
        "Belfast 27 Aug 1900. A Zarps (ZARP police) detachment held the kopje until "
        "overwhelmed; Botha's line collapsed. Final set-piece battle of the conventional war."
    ),
    # ---- De Wet's escape / Brandwater Basin / OFS encirclement ----
    (
        lambda r: (
            "slabbert" in r["description"].lower()
            or ("brandwater" in r["action_place"].lower() and r["event_type"] == "move")
        ),
        "De Wet with Steyn and ~2,600 burghers broke out through unguarded Slabbert's Nek "
        "night of 15 Jul 1900, escaping Hunter's encirclement in the Brandwater Basin. "
        "~4,300 men under Prinsloo were left behind and surrendered 30 Jul; De Wet's escape "
        "kept the OFS resistance alive."
    ),
    # ---- Smuts's Cape raid (main row) ----
    (
        lambda r: (
            "smuts" in r["force"].lower()
            and "cape" in r["force"].lower()
            and r["event_type"] in ("raid", "march", "advance")
            and r["id"] in ("24", "188", "189")
        ),
        "Smuts led ~300 burghers from the Orange River into the western Cape Sep 1901, "
        "routing C Squadron 17th Lancers at Modderfontein, raiding as far as Springbok and "
        "Namaqualand. Besieged Okiep Apr-May 1902. The most daring Boer commando operation "
        "in the Cape Colony."
    ),
    # ---- Smuts's Cape raid (general Smuts commando rows) ----
    (
        lambda r: (
            r["force"].strip().lower() in ("smuts commando", "smuts' cape commando",
                                            "smuts/van deventer commando")
            and r["event_type"] in ("raid", "march", "advance", "siege")
            and "namaqualand" in (r["action_place"] + r["to_place"] + r["description"]).lower()
        ),
        "Smuts led ~300 burghers from the Orange River into the western Cape Sep 1901, "
        "routing C Squadron 17th Lancers at Modderfontein, raiding as far as Springbok and "
        "Namaqualand. Besieged Okiep Apr-May 1902. The most daring Boer commando operation "
        "in the Cape Colony."
    ),
    # ---- Botha at Bakenlaagte ----
    (
        lambda r: "bakenlaagte" in r["action_place"].lower()
        and r["event_type"] == "engagement",
        "Botha with Grobler and Oppermann attacked Benson's column rearguard at Bakenlaagte "
        "30 Oct 1901 in rain and mist. A mounted Boer charge overwhelmed the guns (29 of 32 "
        "gunners fell); Benson mortally wounded. British ~235 casualties; 2 guns lost."
    ),
]


def enrich_description(row):
    """Return a new description if the row matches a high-priority target, else ''."""
    for match_fn, new_desc in ENRICHED_DESCRIPTIONS:
        try:
            if match_fn(row):
                return new_desc.strip()
        except Exception:
            pass
    return ""


# ── NEW ROWS (FIX 4) ─────────────────────────────────────────────────────────

NEW_ROWS = [
    {
        "id": "726",
        "side": "Boer",
        "force": "Prinsloo's OFS force",
        "commander": "Prinsloo, Marthinus",
        "units": "OFS commandos (~4,000 men)",
        "date_start": "1900-07-15",
        "date_end": "1900-07-30",
        "event_type": "surrender",
        "from_place": "Brandwater Basin",
        "to_place": "",
        "action_place": "Brandwater Basin",
        "description": (
            "Hunter's nine-column operation encircled Prinsloo's ~4,314-man OFS force "
            "in the Brandwater Basin. After De Wet escaped through Slabbert's Nek "
            "(15 Jul), the trapped Boers surrendered 30 Jul 1900 – the largest single "
            "Boer capitulation of the war. QSA clasp: WITTEBERGEN."
        ),
        "confidence": "high",
        "source": "Handbook ch.XV; Conan Doyle ch.21; SAMHS vol113hk",
        "note": "QSA clasp WITTEBERGEN; De Wet escaped earlier via Slabbert's Nek",
    },
    {
        "id": "727",
        "side": "British",
        "force": "Natal Army",
        "commander": "Buller, Sir Redvers",
        "units": "IInd Division; Clery; Dundonald cavalry",
        "date_start": "1900-06-09",
        "date_end": "1900-06-12",
        "event_type": "advance",
        "from_place": "Alleman's Nek",
        "to_place": "Laing's Nek",
        "action_place": "Laing's Nek",
        "description": (
            "After storming Alleman's Nek (11 Jun), Clery closed up from Ingogo and "
            "found the historic Majuba–Laing's Nek–Pougwana position abandoned; "
            "Laing's Nek occupied 12 Jun 1900 without opposition, completing Buller's "
            "crossing into the Transvaal. QSA clasp: LAING'S NEK."
        ),
        "confidence": "high",
        "source": "Handbook ch.XIII p.268; Conan Doyle ch. on Natal advance",
        "note": "QSA clasp LAING'S NEK; Volksrust entered 13 Jun concluding the Natal campaign",
    },
]


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    rows = []
    with CSV_PATH.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for r in reader:
            rows.append(r)

    changes = {
        "fix1_place": 0,
        "fix2_commander_format": 0,
        "fix2_commander_infer": 0,
        "fix3_description": 0,
        "fix4_new_rows": 0,
    }

    for row in rows:
        rid = row["id"].strip()

        # ── FIX 1 – Petersburg geocoding ──────────────────────────────────
        if rid == "18":
            old = row["to_place"]
            if "Petersburg" in old or old != "Groenkloof":
                row["to_place"] = "Groenkloof"
                print(f"  FIX1 row 18 to_place: {old!r} → 'Groenkloof'")
                changes["fix1_place"] += 1

        if rid == "21":
            old = row["from_place"]
            if old != "Groenkloof":
                row["from_place"] = "Groenkloof"
                print(f"  FIX1 row 21 from_place: {old!r} → 'Groenkloof'")
                changes["fix1_place"] += 1

        # ── FIX 2 – Commander name format ─────────────────────────────────
        cmd = row["commander"].strip()

        if not cmd:
            # try to infer
            inferred = infer_commander(row)
            if inferred:
                row["commander"] = inferred
                print(f"  FIX2 row {rid} commander inferred: '' → {inferred!r}")
                changes["fix2_commander_infer"] += 1
        else:
            # reformat existing name
            # Handle semicolon-separated lists (multiple commanders)
            parts = cmd.split(";")
            new_parts = [reformat_commander(p.strip()) for p in parts]
            new_cmd = "; ".join(new_parts)
            # Also strip trailing period duplicates at the joined level
            new_cmd = fix_double_period(new_cmd)
            if new_cmd != cmd:
                print(f"  FIX2 row {rid} commander: {cmd!r} → {new_cmd!r}")
                row["commander"] = new_cmd
                changes["fix2_commander_format"] += 1

        # ── FIX 3 – Enrich descriptions ───────────────────────────────────
        new_desc = enrich_description(row)
        if new_desc and new_desc != row["description"].strip():
            old_desc = row["description"][:60]
            row["description"] = new_desc
            print(f"  FIX3 row {rid} description enriched (was: {old_desc!r}...)")
            changes["fix3_description"] += 1

    # ── FIX 4 – Add new QSA clasp rows ────────────────────────────────────
    existing_ids = {r["id"].strip() for r in rows}
    for nr in NEW_ROWS:
        if nr["id"] not in existing_ids:
            rows.append(nr)
            print(f"  FIX4 added row id={nr['id']} ({nr['action_place']})")
            changes["fix4_new_rows"] += 1
        else:
            print(f"  FIX4 SKIP row id={nr['id']} already exists")

    # ── Write back ────────────────────────────────────────────────────────
    with CSV_PATH.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print()
    print("=== Summary ===")
    for k, v in changes.items():
        print(f"  {k}: {v} change(s)")
    total = sum(changes.values())
    print(f"  TOTAL: {total} change(s) applied")
    print(f"  Written to: {CSV_PATH.resolve()}")


if __name__ == "__main__":
    main()
