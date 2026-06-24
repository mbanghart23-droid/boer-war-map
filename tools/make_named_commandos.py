"""
Named Boer commandos / foreign corps / guerrilla leaders not yet on map.
IDs start at 406.
"""
import csv

FIELDS = ['id','side','force','commander','units','date_start','date_end',
          'event_type','from_place','to_place','action_place','description',
          'confidence','source','note']

ROWS = [
    # Named Boer field units / guerrilla commandos
    ("De Wet's Commando","Christiaan de Wet","",
     "1900-03-01","Sannaspos",
     "De Wet's commando struck the British water convoy at Sannaspos (Koorn Spruit) on 31 March 1900, capturing 117 wagons and 7 guns in the first major guerrilla coup of the war.",
     "high","Conan Doyle ch.17; Handbook ch.XV","north"),

    ("Delarey's Commando","Koos de la Rey","",
     "1900-07-01","Magaliesberg",
     "General De la Rey's commando operated in the western Transvaal Magaliesberg region from mid-1900 through the guerrilla phase, ambushing several columns and capturing Lord Methuen at Tweebosch in March 1902.",
     "high","Conan Doyle ch.34; Handbook ch.XVIII","north"),

    ("Botha's Commando (eastern Transvaal)","Louis Botha","",
     "1901-09-01","Bakenlaagte",
     "Botha's commando struck Benson's column at Bakenlaagte on 30 October 1901, inflicting 235 casualties including Benson himself, in one of the most effective guerrilla actions of the war.",
     "high","Conan Doyle ch.34","north"),

    ("Erasmus's Commando","Erasmus","",
     "1899-10-20","Talana Hill",
     "Erasmus's commando formed part of the Boer forces at the battle of Talana Hill on 20 October 1899, threatening Penn Symons's flank during the engagement.",
     "high","Conan Doyle ch.6","north"),

    ("Harrismith Commando","","",
     "1900-06-01","Harrismith",
     "The Harrismith Commando operated in the northeastern OFS during the guerrilla phase, raiding into Natal and skirmishing with British garrisons.",
     "medium","angloboerwar.com","north"),

    ("Haasbroek's Commando","Haasbroek","",
     "1901-01-01","Ladybrand",
     "Haasbroek's commando operated in the eastern OFS during 1901, conducting raids toward the Cape border.",
     "medium","angloboerwar.com","north"),

    ("Colesberg Rebel Commando","","",
     "1899-11-01","Colesberg",
     "Cape rebel commandos around Colesberg joined the Boer forces after the invasion of the Cape Colony in late 1899, skirmishing with French's cavalry until pushed back across the Orange River in March 1900.",
     "high","Conan Doyle ch.9","eastern"),

    ("Burghersdorp Commando (Cape rebels)","","",
     "1901-01-01","Burghersdorp",
     "Cape rebel commandos based on the Burghersdorp district rose during Smuts's and other commando raids into the north-eastern Cape, 1901-02.",
     "medium","angloboerwar.com","eastern"),

    # Foreign volunteer corps
    ("Foreign Volunteer Corps (German)","","",
     "1899-11-01","Pretoria",
     "German volunteers organized as a foreign corps served with the Transvaal forces from the outbreak of war; the corps numbered several hundred men and served mainly in the eastern Transvaal.",
     "medium","angloboerwar.com","north"),

    ("Hollander Corps","","",
     "1899-10-11","Pretoria",
     "Dutch (Hollander) volunteers formed a corps in Transvaal service from the declaration of war, reflecting strong Dutch sympathy for the Boer cause; they served in the eastern Transvaal and Natal fronts.",
     "medium","angloboerwar.com","north"),

    ("Irish-American Corps","","",
     "1899-11-01","Ladysmith",
     "The Irish-American Brigade under Major John MacBride served with the Transvaal forces in Natal from late 1899, fighting at Colenso and later operations before disbanding in 1900.",
     "medium","angloboerwar.com","north"),

    ("Johannesburg Police","","",
     "1899-10-11","Johannesburg",
     "The Johannesburg (ZAR) Police served as a paramilitary unit from the outbreak of war, providing garrison and field duties in the Transvaal before the fall of Johannesburg in May 1900.",
     "medium","angloboerwar.com","north"),

    ("Artillerie (OFS)","","",
     "1899-10-11","Bloemfontein",
     "The Orange Free State Artillery mobilized at Bloemfontein in October 1899 and served on all fronts, notably at Magersfontein and during the defence of the OFS capital.",
     "high","angloboerwar.com; Handbook ch.IX","north"),
]

rows = []
START_ID = 406
for i, r in enumerate(ROWS):
    (force, commander, units, date_start, action_place, description, confidence, source, region) = r
    rows.append({
        'id': str(START_ID + i),
        'side': 'Boer',
        'force': force,
        'commander': commander,
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

out = 'data/_named_commandos_fragment.csv'
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    for r in rows:
        w.writerow({k: r.get(k,'') for k in FIELDS})

print(f'Written {len(rows)} rows, IDs {rows[0]["id"]}-{rows[-1]["id"]}')
print('\nA entries:')
for r in rows:
    print(f' "{r["id"]}": dict(pt="{r["action_place"]}", region="{r["_region"]}"),')
