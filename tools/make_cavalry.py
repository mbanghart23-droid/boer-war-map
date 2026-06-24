"""
British cavalry regiments that served in the Boer War.
IDs start at 384.
"""
import csv

FIELDS = ['id','side','force','commander','units','date_start','date_end',
          'event_type','from_place','to_place','action_place','description',
          'confidence','source','note']

# (force, units, date_start, event_type, action_place, description, confidence, source, region)
ROWS = [
    # --- HOUSEHOLD / DRAGOONS ---
    ("1st (Royal) Dragoons","1st Royal Dragoons",
     "1900-02-01","deployment","Bloemfontein",
     "The 1st Royal Dragoons served in Roberts's main army during the advance from the Orange River to Pretoria in 1900, providing cavalry screen and pursuit roles.",
     "high","angloboerwar.com; Handbook ch.XII","north"),

    ("2nd Dragoon Guards (Queen's Bays)","2nd Dragoon Guards",
     "1900-01-01","deployment","Modder River",
     "The Queen's Bays (2nd Dragoon Guards) served in Methuen's and French's cavalry division on the western front, participating in the relief of Kimberley.",
     "high","Conan Doyle ch.14; angloboerwar.com","north"),

    ("5th (Princess Charlotte of Wales's) Dragoon Guards","5th Dragoon Guards",
     "1900-01-01","deployment","Pretoria",
     "The 5th Dragoon Guards served in the Transvaal during the advance phase and guerrilla period of 1900-01.",
     "high","angloboerwar.com","north"),

    ("6th (Carabiniers) Dragoon Guards","6th Dragoon Guards",
     "1900-01-01","deployment","Pretoria",
     "The 6th Dragoon Guards (Carabiniers) served in the Transvaal during the advance and guerrilla phases of 1900-01.",
     "high","angloboerwar.com","north"),

    # --- HUSSARS ---
    ("10th (Prince of Wales's Own) Hussars","10th Hussars",
     "1899-11-01","deployment","Ladysmith",
     "The 10th Hussars formed part of the cavalry attached to White's Natal force and were besieged in Ladysmith from November 1899 to February 1900.",
     "high","Handbook ch.V; angloboerwar.com","north"),

    ("13th Hussars","13th King's Hussars",
     "1900-02-01","deployment","Bloemfontein",
     "The 13th Hussars served in Roberts's cavalry force during the advance through the OFS and into the Transvaal in 1900.",
     "high","angloboerwar.com","north"),

    ("14th (King's) Hussars","14th King's Hussars",
     "1900-01-01","deployment","Pretoria",
     "The 14th King's Hussars served in the Transvaal during the advance and guerrilla phases of 1900-02.",
     "high","angloboerwar.com","north"),

    ("15th (The King's) Hussars","15th Hussars",
     "1900-02-01","deployment","Pretoria",
     "The 15th Hussars served with Roberts's cavalry in the advance from the Modder River to Pretoria in 1900.",
     "high","angloboerwar.com","north"),

    ("18th Hussars","18th King George's Own Hussars",
     "1899-10-01","deployment","Dundee",
     "The 18th Hussars served in Natal from the opening of the campaign and were engaged at Talana Hill on 20 October 1899, subsequently joining the Ladysmith garrison.",
     "high","Conan Doyle ch.6; Handbook ch.IV","north"),

    ("19th (Princess of Wales's Own) Hussars","19th Hussars",
     "1900-02-01","deployment","Bloemfontein",
     "The 19th Hussars served with Roberts's cavalry division during the advance through the OFS and Transvaal in 1900.",
     "high","angloboerwar.com","north"),

    # --- LANCERS ---
    ("5th (Royal Irish) Lancers","5th Royal Irish Lancers",
     "1899-10-01","deployment","Ladysmith",
     "The 5th Royal Irish Lancers served in Natal from the opening of the campaign and formed part of the Ladysmith cavalry during the siege of November 1899 - February 1900.",
     "high","Handbook ch.V; angloboerwar.com","north"),

    ("9th (Queen's Royal) Lancers","9th Lancers",
     "1899-11-01","deployment","Modder River",
     "The 9th Lancers served in French's cavalry under Methuen on the western front, participating in the advance to Kimberley; French's famous cavalry dash to relieve Kimberley in February 1900 included the regiment.",
     "high","Conan Doyle ch.14","north"),

    ("12th (Prince of Wales's Royal) Lancers","12th Royal Lancers",
     "1900-01-01","deployment","Bloemfontein",
     "The 12th Royal Lancers served in Roberts's main cavalry force during the advance from the Orange River to Pretoria in 1900.",
     "high","angloboerwar.com","north"),

    ("16th (Queen's) Lancers","16th Queen's Lancers",
     "1900-01-01","deployment","Pretoria",
     "The 16th Queen's Lancers served in the Transvaal during the advance and guerrilla phases of 1900-01.",
     "high","angloboerwar.com","north"),

    ("17th Duke of Cambridge's Own Lancers","17th Lancers",
     "1900-01-01","deployment","Pretoria",
     "The 17th Lancers served in Roberts's cavalry and in column drives during the guerrilla phase in the Transvaal.",
     "high","angloboerwar.com","north"),

    # --- DRAGOON LIGHT ---
    ("Imperial Light Horse","Imperial Light Horse",
     "1899-10-01","deployment","Ladysmith",
     "The Imperial Light Horse, raised in Natal from Uitlander refugees in 1899, served throughout the siege of Ladysmith and subsequently in the Natal advance, earning distinction at Elandslaagte on 21 October 1899.",
     "high","Conan Doyle ch.7; Handbook ch.IV","north"),

    ("Natal Carbineers","Natal Carbineers",
     "1899-10-01","deployment","Ladysmith",
     "The Natal Carbineers, an established colonial unit, served in the Ladysmith garrison throughout the siege and subsequently in the advance through Natal and the Transvaal.",
     "high","Handbook ch.V","north"),

    ("1st Canadian Mounted Rifles (Royal Canadian Dragoons)","Royal Canadian Dragoons",
     "1900-01-01","deployment","Pretoria",
     "The Royal Canadian Dragoons (1st Canadian Mounted Rifles) served in the Transvaal during 1900, earning distinction at Leliefontein on 7 November 1900 where three Victoria Crosses were won.",
     "high","angloboerwar.com; Conan Doyle ch.31","north"),

    ("2nd Canadian Mounted Rifles","2nd Canadian Mounted Rifles",
     "1900-01-01","deployment","Pretoria",
     "The 2nd Canadian Mounted Rifles served in the Transvaal in 1900 during the advance and early guerrilla phases.",
     "high","angloboerwar.com","north"),

    ("Strathcona's Horse","Strathcona's Horse",
     "1900-01-01","deployment","Pretoria",
     "Lord Strathcona's Horse, raised in Canada, served in the Transvaal during 1900, participating in column operations against the guerrilla commandos.",
     "high","angloboerwar.com","north"),

    ("New Zealand Mounted Rifles","New Zealand Mounted Rifles",
     "1900-01-01","deployment","Pretoria",
     "The New Zealand Mounted Rifles contingents (1st-5th) served in the Transvaal and ORC during 1900-01, noted for scouting and mobility in column operations.",
     "high","angloboerwar.com","north"),

    ("Australian Horse / 1st Australian Horse","1st Australian Horse",
     "1900-02-01","deployment","Bloemfontein",
     "Australian Horse contingents served in South Africa from early 1900, operating in the OFS and Transvaal during the advance and guerrilla phases.",
     "high","angloboerwar.com","north"),
]

rows = []
START_ID = 384
for i, r in enumerate(ROWS):
    (force, units, date_start, event_type, action_place, description, confidence, source, region) = r
    rows.append({
        'id': str(START_ID + i),
        'side': 'British',
        'force': force,
        'commander': '',
        'units': units,
        'date_start': date_start,
        'date_end': '',
        'event_type': event_type,
        'from_place': 'England',
        'to_place': '',
        'action_place': action_place,
        'description': description,
        'confidence': confidence,
        'source': source,
        'note': '',
        '_region': region,
    })

out = 'data/_cavalry_fragment.csv'
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    for r in rows:
        w.writerow({k: r.get(k,'') for k in FIELDS})

print(f'Written {len(rows)} rows, IDs {rows[0]["id"]}-{rows[-1]["id"]}')
print('\nA entries:')
for r in rows:
    print(f' "{r["id"]}": dict(pt="{r["action_place"]}", region="{r["_region"]}"),')
