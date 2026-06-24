"""
Royal Field Artillery / Royal Horse Artillery batteries.
IDs start at 458.
"""
import csv

FIELDS = ['id','side','force','commander','units','date_start','date_end',
          'event_type','from_place','to_place','action_place','description',
          'confidence','source','note']

# Each tuple: (battery_name, units_str, date_start, action_place, description, confidence, source, region)
ROWS = [
    # --- WESTERN FRONT (Methuen / French) ---
    ("14th Battery Royal Field Artillery","14th Battery RFA",
     "1899-11-01","Modder River",
     "The 14th Battery RFA supported Methuen's division in the advance along the western railway line, fighting at Belmont, Modder River, and Magersfontein in November-December 1899.",
     "high","Conan Doyle ch.13","north"),

    ("18th Battery Royal Field Artillery","18th Battery RFA",
     "1899-11-01","Modder River",
     "The 18th Battery RFA served with Methuen's 1st Division on the western front, supporting the advance to relieve Kimberley.",
     "high","Handbook ch.IX","north"),

    ("62nd Battery Royal Field Artillery","62nd Battery RFA",
     "1900-02-01","Modder River",
     "The 62nd Battery RFA formed part of the artillery attached to French's cavalry division during the relief of Kimberley in February 1900.",
     "high","Conan Doyle ch.14","north"),

    ("75th Battery Royal Field Artillery","75th Battery RFA",
     "1900-01-01","Bloemfontein",
     "The 75th Battery RFA served in Roberts's main army during the advance through the OFS to Bloemfontein and beyond in 1900.",
     "high","Handbook ch.XII","north"),

    ("76th Battery Royal Field Artillery","76th Battery RFA",
     "1900-01-01","Bloemfontein",
     "The 76th Battery RFA served in Roberts's forces during the OFS advance in early 1900.",
     "high","Handbook ch.XII","north"),

    # --- NATAL FRONT (Buller) ---
    ("4th Battery Royal Field Artillery","4th Battery RFA",
     "1899-11-01","Ladysmith",
     "The 4th Battery RFA was part of the Natal army's artillery, serving in the Ladysmith siege and subsequently in Buller's Tugela operations.",
     "high","Handbook ch.V","north"),

    ("13th Battery Royal Field Artillery","13th Battery RFA",
     "1899-12-01","Colenso",
     "The 13th Battery RFA served in Buller's Natal army and was engaged at Colenso on 15 December 1899, where several guns were temporarily lost.",
     "high","Conan Doyle ch.11","north"),

    ("14th Battery Royal Field Artillery (2nd)","14th Battery RFA (2nd deployment)",
     "1900-01-01","Ladysmith",
     "A second deployment of the 14th Battery RFA supported Buller's relief columns on the Tugela during January-February 1900.",
     "medium","Handbook ch.XI","north"),

    ("17th Battery Royal Field Artillery","17th Battery RFA",
     "1899-12-01","Colenso",
     "The 17th Battery RFA served at Colenso and the subsequent Tugela operations under Buller.",
     "high","Conan Doyle ch.11; Handbook ch.XI","north"),

    ("19th Battery Royal Field Artillery","19th Battery RFA",
     "1900-01-01","Spion Kop",
     "The 19th Battery RFA provided artillery support during the Spion Kop operations of January 1900.",
     "high","Conan Doyle ch.12","north"),

    ("28th Battery Royal Field Artillery","28th Battery RFA",
     "1900-01-01","Ladysmith",
     "The 28th Battery RFA served in the Natal army's artillery train during the Tugela campaign and relief of Ladysmith.",
     "high","Handbook ch.XI","north"),

    ("63rd Battery Royal Field Artillery","63rd Battery RFA",
     "1900-01-01","Ladysmith",
     "The 63rd Battery RFA formed part of Buller's field artillery during the Natal operations of 1900.",
     "medium","Handbook ch.XI","north"),

    ("64th Battery Royal Field Artillery","64th Battery RFA",
     "1900-01-01","Ladysmith",
     "The 64th Battery RFA served in the Natal artillery during the Tugela and relief operations of 1900.",
     "medium","Handbook ch.XI","north"),

    # --- ROBERTS'S MAIN ARMY (OFS / Tvl) ---
    ("20th Battery Royal Field Artillery","20th Battery RFA",
     "1900-02-01","Bloemfontein",
     "The 20th Battery RFA served with Roberts's main army in the advance from the Orange River to Bloemfontein and Pretoria in 1900.",
     "high","Handbook ch.XII","north"),

    ("21st Battery Royal Field Artillery","21st Battery RFA",
     "1900-02-01","Bloemfontein",
     "The 21st Battery RFA served in Roberts's OFS advance in early 1900.",
     "high","Handbook ch.XII","north"),

    ("38th Battery Royal Field Artillery","38th Battery RFA",
     "1900-02-01","Pretoria",
     "The 38th Battery RFA served in the Transvaal during the advance and guerrilla phases of 1900-01.",
     "high","angloboerwar.com","north"),

    ("42nd Battery Royal Field Artillery","42nd Battery RFA",
     "1900-02-01","Bloemfontein",
     "The 42nd Battery RFA formed part of Roberts's artillery during the OFS and Transvaal campaigns of 1900.",
     "high","Handbook ch.XII","north"),

    ("53rd Battery Royal Field Artillery","53rd Battery RFA",
     "1900-02-01","Pretoria",
     "The 53rd Battery RFA served in the Transvaal during 1900-01 as part of column artillery.",
     "medium","angloboerwar.com","north"),

    # --- HOWITZERS ---
    ("37th Howitzer Battery Royal Field Artillery","37th Howitzer Battery RFA",
     "1900-01-01","Ladysmith",
     "The 37th Howitzer Battery RFA served in the Natal campaign with 5-inch howitzers, providing high-angle fire over the kopjes during the Tugela operations.",
     "high","Handbook ch.XI","north"),

    ("61st Howitzer Battery Royal Field Artillery","61st Howitzer Battery RFA",
     "1900-02-01","Bloemfontein",
     "The 61st Howitzer Battery RFA served in Roberts's army during the OFS advance in 1900.",
     "high","Handbook ch.XII","north"),

    # --- MOUNTAIN BATTERIES ---
    ("4th Mountain Battery","4th Mountain Battery RGA",
     "1899-10-01","Ladysmith",
     "The 4th Mountain Battery Royal Garrison Artillery served with the Natal force from the outbreak of war, providing screw-gun support in the mountain terrain around Ladysmith.",
     "high","Handbook ch.V","north"),

    ("10th Mountain Battery","10th Mountain Battery RGA",
     "1900-02-01","Bloemfontein",
     "The 10th Mountain Battery Royal Garrison Artillery served in Roberts's army, providing artillery support in difficult terrain during the advance through the OFS.",
     "high","angloboerwar.com","north"),

    # --- ROYAL HORSE ARTILLERY ---
    ("J Battery Royal Horse Artillery","J Battery RHA",
     "1900-02-01","Modder River",
     "J Battery RHA served with French's cavalry division in the relief of Kimberley and subsequent advance through the OFS.",
     "high","Conan Doyle ch.14","north"),

    ("Q Battery Royal Horse Artillery","Q Battery RHA",
     "1899-12-01","Colenso",
     "Q Battery RHA served at Colenso and in the Natal operations; during the retreat at Sion Kop, Q Battery helped cover the British withdrawal.",
     "high","Conan Doyle ch.11","north"),

    ("U Battery Royal Horse Artillery","U Battery RHA",
     "1900-01-01","Bloemfontein",
     "U Battery RHA served with Roberts's cavalry in the OFS advance and Transvaal operations of 1900.",
     "high","angloboerwar.com","north"),

    # --- FIELD ARTILLERY ADDITIONAL ---
    ("18th Battery Royal Field Artillery (2nd)","18th Battery RFA (2nd)",
     "1900-06-01","Pretoria",
     "A second deployment or redeployment of the 18th Battery RFA served in the Transvaal during the guerrilla phase.",
     "medium","angloboerwar.com","north"),

    ("12th Battery Royal Field Artillery","12th Battery RFA",
     "1900-02-01","Bloemfontein",
     "The 12th Battery RFA served in Roberts's main army during the advance through the OFS in 1900.",
     "medium","angloboerwar.com","north"),

    ("73rd Battery Royal Field Artillery","73rd Battery RFA",
     "1900-02-01","Pretoria",
     "The 73rd Battery RFA served in the Transvaal during the advance and guerrilla phases of 1900-01.",
     "medium","angloboerwar.com","north"),

    ("82nd Battery Royal Field Artillery","82nd Battery RFA",
     "1900-02-01","Pretoria",
     "The 82nd Battery RFA served in Roberts's army during the advance through the OFS and Transvaal in 1900.",
     "medium","angloboerwar.com","north"),

    ("86th Battery Royal Field Artillery","86th Battery RFA",
     "1900-06-01","Pretoria",
     "The 86th Battery RFA served in the Transvaal during the guerrilla phase of 1900-02.",
     "medium","angloboerwar.com","north"),
]

rows = []
START_ID = 458
for i, r in enumerate(ROWS):
    (force, units, date_start, action_place, description, confidence, source, region) = r
    rows.append({
        'id': str(START_ID + i),
        'side': 'British',
        'force': force,
        'commander': '',
        'units': units,
        'date_start': date_start,
        'date_end': '',
        'event_type': 'deployment',
        'from_place': 'England',
        'to_place': '',
        'action_place': action_place,
        'description': description,
        'confidence': confidence,
        'source': source,
        'note': '',
        '_region': region,
    })

out = 'data/_artillery_fragment.csv'
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    for r in rows:
        w.writerow({k: r.get(k,'') for k in FIELDS})

print(f'Written {len(rows)} rows, IDs {rows[0]["id"]}-{rows[-1]["id"]}')
print('\nA entries:')
for r in rows:
    print(f' "{r["id"]}": dict(pt="{r["action_place"]}", region="{r["_region"]}"),')
