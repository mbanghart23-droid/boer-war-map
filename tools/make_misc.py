"""
Miscellaneous remaining units: support, yeomanry, more cavalry, named commandos.
IDs start at 488.
"""
import csv

FIELDS = ['id','side','force','commander','units','date_start','date_end',
          'event_type','from_place','to_place','action_place','description',
          'confidence','source','note']

ROWS = [
    # --- SUPPORT (British) ---
    ("Army Chaplains Department","Army Chaplains Department","British",
     "1899-10-01","Cape Town",
     "Army Chaplains provided spiritual support to British forces across all theatres of the war from 1899-1902.",
     "medium","angloboerwar.com","north"),

    ("Army Pay Corps","Army Pay Corps","British",
     "1899-10-01","Cape Town",
     "The Army Pay Corps administered pay and financial records for British forces in South Africa throughout the war.",
     "medium","angloboerwar.com","north"),

    ("Army Post Office Corps","Army Post Office Corps","British",
     "1899-10-01","Cape Town",
     "The Army Post Office Corps maintained postal services for British forces across South Africa throughout the war.",
     "medium","angloboerwar.com","north"),

    ("Army Veterinary Corps","Army Veterinary Corps","British",
     "1899-10-01","Cape Town",
     "The Army Veterinary Corps cared for the enormous horse and mule populations essential to British mobility throughout the war.",
     "medium","angloboerwar.com","north"),

    ("Military Foot Police","Military Foot Police","British",
     "1899-10-01","Cape Town",
     "The Military Foot Police maintained order in base areas and lines of communication throughout South Africa.",
     "medium","angloboerwar.com","north"),

    ("Military Mounted Police","Military Mounted Police","British",
     "1899-10-01","Cape Town",
     "The Military Mounted Police provided mounted law enforcement and patrol duties across the theatre of operations.",
     "medium","angloboerwar.com","north"),

    ("New South Wales Ambulance","New South Wales Ambulance Corps","British",
     "1900-01-01","Bloemfontein",
     "The NSW Ambulance Corps provided medical evacuation and field hospital support to Australian and British forces in the OFS and Transvaal.",
     "medium","angloboerwar.com","north"),

    ("Railway Pioneers","Railway Pioneers","British",
     "1899-10-01","Cape Town",
     "Railway Pioneer units repaired and reconstructed the railway network destroyed by Boer demolition teams, essential to British logistics throughout the war.",
     "high","angloboerwar.com","north"),

    ("Militia","Militia (various)","British",
     "1900-01-01","Cape Town",
     "Militia battalions from various British regiments provided garrison and reserve duties in South Africa from 1900, freeing regular units for field service.",
     "medium","angloboerwar.com","north"),

    # --- IMPERIAL YEOMANRY (remaining) ---
    ("Derbyshire Yeomanry","Derbyshire Yeomanry","British",
     "1900-02-01","Pretoria",
     "The Derbyshire Yeomanry served as Imperial Yeomanry in South Africa during 1900-01 as part of the mounted column forces.",
     "high","angloboerwar.com","north"),

    ("Warwickshire Yeomanry","Warwickshire Yeomanry","British",
     "1900-02-01","Pretoria",
     "The Warwickshire Yeomanry served as Imperial Yeomanry in South Africa during 1900-01.",
     "high","angloboerwar.com","north"),

    ("Wiltshire Yeomanry","Wiltshire Yeomanry","British",
     "1900-02-01","Bloemfontein",
     "The Wiltshire Yeomanry served as Imperial Yeomanry in South Africa in 1900-01.",
     "high","angloboerwar.com","north"),

    # --- CAVALRY (remaining, not variant duplicates) ---
    ("Household Cavalry (Composite Regiment)","Household Cavalry","British",
     "1900-01-01","Pretoria",
     "The Composite Regiment of Household Cavalry (Life Guards, Horse Guards, Dragoon Guards) served in Roberts's army during the advance to Pretoria in 1900.",
     "high","Conan Doyle ch.14; angloboerwar.com","north"),

    ("11th (Prince Albert's Own) Hussars","11th Hussars","British",
     "1900-02-01","Bloemfontein",
     "The 11th Hussars served in the cavalry division during Roberts's advance from the Modder River to Pretoria in 1900.",
     "high","angloboerwar.com","north"),

    ("20th Hussars","20th Hussars","British",
     "1900-02-01","Pretoria",
     "The 20th Hussars served in the Transvaal during the advance and guerrilla phases of 1900-01.",
     "high","angloboerwar.com","north"),

    ("21st Lancers","21st Lancers","British",
     "1900-02-01","Pretoria",
     "The 21st Lancers (Empress of India's) served in the Transvaal during the advance and guerrilla phase of 1900-01.",
     "high","angloboerwar.com","north"),

    ("3rd (Prince of Wales's) Dragoon Guards","3rd Dragoon Guards","British",
     "1900-01-01","Pretoria",
     "The 3rd Dragoon Guards served in the Transvaal with Roberts's forces during the advance and guerrilla phase.",
     "high","angloboerwar.com","north"),

    ("6th (Inniskilling) Dragoons","6th Inniskilling Dragoons","British",
     "1900-01-01","Pretoria",
     "The 6th Inniskilling Dragoons served in the advance through the OFS and Transvaal in 1900.",
     "high","angloboerwar.com","north"),

    ("7th (Princess Royal's) Dragoon Guards","7th Dragoon Guards","British",
     "1900-01-01","Bloemfontein",
     "The 7th Dragoon Guards served in Roberts's cavalry during the advance from the Modder River to Pretoria in 1900.",
     "high","angloboerwar.com","north"),

    ("7th (Queen's Own) Hussars","7th Hussars","British",
     "1900-01-01","Pretoria",
     "The 7th Hussars served in the Transvaal during the advance and guerrilla phases of 1900-01.",
     "high","angloboerwar.com","north"),

    ("3rd Hussars","3rd Hussars","British",
     "1900-02-01","Pretoria",
     "The 3rd Hussars served in the Transvaal with Roberts's cavalry during 1900.",
     "high","angloboerwar.com","north"),

    ("4th (The Queen's Own) Hussars","4th Hussars","British",
     "1900-01-01","Bloemfontein",
     "The 4th Hussars served in the OFS and Transvaal during the advance of 1900.",
     "high","angloboerwar.com","north"),

    # --- REMAINING NAMED COMMANDOS (Boer) ---
    ("Prinsloo's Commando (Jacob Prinsloo)","Jacob Prinsloo","Boer",
     "1900-07-01","Brandwater Basin",
     "Major-General Jacob Prinsloo commanded a large OFS force that was surrounded and forced to surrender at Brandwater Basin on 30 July 1900, the largest Boer capitulation of the war (4,314 men).",
     "high","Conan Doyle ch.21; Handbook ch.XV","north"),

    ("Olivier's Commando","J.H. Olivier","Boer",
     "1900-03-01","Wepener",
     "General Olivier's commando besieged Wepener in April 1900 for 16 days before withdrawing as Roberts's flanking forces closed in; subsequently fought in the OFS guerrilla campaign.",
     "high","Conan Doyle ch.19","north"),

    ("Schalk Burger's Commando","Schalk Burger","Boer",
     "1900-08-01","Belfast",
     "Acting President Schalk Burger's commando operated in the eastern Transvaal during the guerrilla phase, retreating before Buller's advance through the Drakensberg.",
     "high","Conan Doyle ch.26","north"),

    ("Meyer's Commando","Lucas Meyer","Boer",
     "1899-10-20","Talana Hill",
     "General Lucas Meyer commanded the Boer forces at Talana Hill on 20 October 1899 and subsequently operated in the Natal and eastern Transvaal.",
     "high","Conan Doyle ch.6","north"),

    ("Sarel Eloff's Commando","Sarel Eloff","Boer",
     "1900-05-12","Mafeking",
     "Commandant Sarel Eloff led the final Boer assault on Mafeking on 12 May 1900, penetrating the defences but being captured along with 108 men as Baden-Powell counter-attacked.",
     "high","Conan Doyle ch.20","north"),

    ("Koch's Commando (ORC)","Koch","Boer",
     "1900-01-01","Harrismith",
     "Koch's commando operated in the northeastern OFS during the guerrilla phase, raiding supply lines and colonial borders.",
     "medium","angloboerwar.com","north"),

    ("Ferreira's Commando","Ferreira","Boer",
     "1900-06-01","Pretoria",
     "Ferreira's commando operated in the western Transvaal during the guerrilla phase from mid-1900.",
     "medium","angloboerwar.com","north"),

    ("Naauwpoort Commando","","Boer",
     "1899-11-01","Naauwpoort",
     "Cape rebel and Boer forces occupied and raided around Naauwpoort junction in November 1899 before being pushed out by French's cavalry operations.",
     "medium","Conan Doyle ch.9","eastern"),

    ("Roodepoort Commando","","Boer",
     "1900-05-01","Johannesburg",
     "The Roodepoort Commando, drawn from the Roodepoort/Krugersdorp mining district, served in the Witwatersrand defence and guerrilla operations.",
     "medium","angloboerwar.com","north"),

    # --- ARTILLERY (Boer / irregular) ---
    ("Boer Krupp Batteries","","Boer",
     "1899-10-11","Pretoria",
     "The Transvaal and OFS artilleries fielded Krupp field guns and howitzers throughout the war; the Krupp 75mm and Long Tom 155mm Creusot pieces were the backbone of Boer artillery.",
     "high","Conan Doyle ch.2; Handbook","north"),

    ("Free State Artillery","","Boer",
     "1899-10-11","Bloemfontein",
     "The Orange Free State Artillery, equipped with Krupp field guns, served on all fronts from the outbreak of war; it was disbanded after the fall of Bloemfontein in March 1900.",
     "high","angloboerwar.com; Handbook ch.IX","north"),

    ("Diamond Fields Artillery (Kimberley)","Diamond Fields Artillery","British",
     "1899-10-14","Kimberley",
     "The Diamond Fields Artillery, a colonial unit manned by De Beers employees and volunteers, provided artillery defence of Kimberley during the siege of October 1899 to February 1900; 'Long Cecil', a gun built in the De Beers workshops, was their improvised contribution.",
     "high","Conan Doyle ch.15","north"),

    ("Elswick Battery","Elswick Battery","British",
     "1900-02-01","Bloemfontein",
     "The Elswick Battery, equipped with Elswick Ordnance Company quick-firing guns, served in Roberts's main army during the advance through the OFS in 1900.",
     "high","angloboerwar.com","north"),

    ("Canadian Field Artillery","Canadian Field Artillery","British",
     "1900-01-01","Pretoria",
     "The Canadian Field Artillery battery served in the Transvaal during 1900, providing artillery support to Canadian and British column operations.",
     "high","angloboerwar.com","north"),
]

rows = []
START_ID = 488
for i, r in enumerate(ROWS):
    (force, units, side, date_start, action_place, description, confidence, source, region) = r
    rows.append({
        'id': str(START_ID + i),
        'side': side,
        'force': force,
        'commander': '',
        'units': units,
        'date_start': date_start,
        'date_end': '',
        'event_type': 'deployment',
        'from_place': '',
        'to_place': '',
        'action_place': action_place,
        'description': description,
        'confidence': confidence,
        'source': source,
        'note': '',
        '_region': region,
    })

out = 'data/_misc_fragment.csv'
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    for r in rows:
        w.writerow({k: r.get(k,'') for k in FIELDS})

print(f'Written {len(rows)} rows, IDs {rows[0]["id"]}-{rows[-1]["id"]}')
print('\nA entries:')
for r in rows:
    print(f' "{r["id"]}": dict(pt="{r["action_place"]}", region="{r["_region"]}"),')
