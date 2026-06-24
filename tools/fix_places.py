"""
Fix place name variants and province-level action_places in movements.csv.
Also adds 3 missing EC events (Indwe, Maclear, Hanover Road)
and 2 proper engagement rows (Belmont, Graspan).
"""
import csv, re

FIELDS = ['id','side','force','commander','units','date_start','date_end',
          'event_type','from_place','to_place','action_place','description',
          'confidence','source','note']

# ── 1. Canonical spellings ─────────────────────────────────────────────────
PLACE_FIXES = {
    # action_place / from_place / to_place normalisation
    'Dreifontein':   'Driefontein',      # OVERRIDES key is Driefontein
    'Sannas Post':   'Sannaspos',        # OVERRIDES key is Sannaspos (also Sannas Post)
    'Sannaspost':    'Sannaspos',
    'Colesburg':     'Colesberg',        # correct Afrikaans
    "Lombard's Kop": 'Lombards Kop',    # OVERRIDES has no apostrophe
    "O'kiep":        'Okiep',           # OVERRIDES key is Okiep
}

# ── 2. Province-level → nearest significant town ──────────────────────────
# Keyed by (action_place, side) — British units in OFS anchor to Bloemfontein,
# Boer OFS units to Bloemfontein, Natal British to Ladysmith, etc.
PROVINCE_MAP = {
    'Orange Free State':   'Bloemfontein',
    'Orange River Colony': 'Bloemfontein',
    'Natal':               'Ladysmith',
    'Cape Colony':         'Cape Town',
    'Transvaal':           'Pretoria',
    'South Africa':        'Cape Town',
}

rows = list(csv.DictReader(open('data/movements.csv', encoding='utf-8')))
changed = 0

for r in rows:
    for field in ('action_place', 'from_place', 'to_place'):
        val = r[field]
        if val in PLACE_FIXES:
            r[field] = PLACE_FIXES[val]
            changed += 1
        elif val in PROVINCE_MAP:
            r[field] = PROVINCE_MAP[val]
            changed += 1

print(f"Fixed {changed} place values")

# ── 3. New rows ────────────────────────────────────────────────────────────
next_id = max(int(r['id']) for r in rows) + 1

NEW_ROWS = [
    # EC events
    dict(id=next_id, side='Boer', force="Boer raid on Indwe colliery",
         commander='Wessels, C.J.', units="OFS commandos",
         date_start='1900-05-01', date_end='1900-05-01',
         event_type='raid', from_place='', to_place='',
         action_place='Indwe',
         description="Boer commandos raided the Indwe coal colliery in the eastern Cape Midlands (mid-1900), destroying mining infrastructure; the colliery supplied coal to Cape railways and was a strategic target during the guerrilla phase.",
         confidence='medium', source='angloboerwar.com', note='date approximate'),

    dict(id=next_id+1, side='Boer', force="Commando activity around Maclear",
         commander='Kritzinger, P.H.', units="Kritzinger's commando",
         date_start='1901-04-01', date_end='1901-08-01',
         event_type='raid', from_place='', to_place='',
         action_place='Maclear',
         description="Kritzinger's commandos operated in the remote Maclear district of the eastern Cape mountains during 1901, sheltering in the Drakensberg foothills and recruiting Cape rebels while British columns struggled to penetrate the terrain.",
         confidence='medium', source='angloboerwar.com', note=''),

    dict(id=next_id+2, side='British', force="Gatacre's advance base — Hanover Road",
         commander='Gatacre, W.F.', units="3rd Division; Royal Irish Rifles; Northumberland Fusiliers",
         date_start='1899-12-05', date_end='1899-12-10',
         event_type='advance', from_place='Naauwpoort', to_place='Stormberg',
         action_place='Hanover Road',
         description="Gatacre concentrated his 3rd Division at Hanover Road station 5-9 Dec 1899 before the disastrous night march on Stormberg (10 Dec); the station was his last supply point before the column lost its way in the dark and walked into the Boer ambush.",
         confidence='high', source='Conan Doyle ch.XII', note=''),

    # Belmont engagement point
    dict(id=next_id+3, side='British', force="Battle of Belmont",
         commander='Methuen, Lord', units="Guards Brigade; 9th Brigade; G Battery RHA",
         date_start='1899-11-23', date_end='1899-11-23',
         event_type='engagement', from_place='', to_place='',
         action_place='Belmont',
         description="Battle of Belmont (23 Nov 1899): Methuen's Guards Brigade stormed the Boer-held kopjes at dawn, driving Prinsloo's commandos off after a sharp fight; 75 British killed and wounded in the first engagement of the western advance.",
         confidence='high', source='Conan Doyle ch.XI', note=''),

    # Graspan engagement point
    dict(id=next_id+4, side='British', force="Battle of Graspan (Enslin)",
         commander='Methuen, Lord', units="Naval Brigade; 9th Brigade; 18th Battery RFA",
         date_start='1899-11-25', date_end='1899-11-25',
         event_type='engagement', from_place='', to_place='',
         action_place='Graspan',
         description="Battle of Graspan (Enslin), 25 Nov 1899: the Naval Brigade led the assault on the Boer kopjes, suffering 188 casualties including many bluejackets; the position was taken and Methuen's column continued north toward Modder River.",
         confidence='high', source='Conan Doyle ch.XI', note=''),
]

rows.extend(NEW_ROWS)
print(f"Added {len(NEW_ROWS)} new rows (IDs {next_id}–{next_id+len(NEW_ROWS)-1})")

with open('data/movements.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    w.writeheader()
    for r in rows:
        w.writerow({k: r.get(k,'') for k in FIELDS})

print("Written data/movements.csv")
print(f"Total rows: {len(rows)}")

# Print A dict entries for new rows
print("\nA dict entries needed:")
for r in NEW_ROWS:
    rid = r['id']; pt = r['action_place']
    fp = r.get('from_place',''); tp = r.get('to_place','')
    if fp and tp:
        print(f' "{rid}": dict(pt="{pt}", line=("{fp}","{tp}"), region="eastern"),')
    else:
        print(f' "{rid}": dict(pt="{pt}", region="eastern"),')
