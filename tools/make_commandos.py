"""
Generate one mobilization row per Boer district commando (Oct 1899).
IDs start at 262.
"""
import csv, json

FIELDS = ['id','side','force','commander','units','date_start','date_end',
          'event_type','from_place','to_place','action_place','description',
          'confidence','source','note']

# (commando_name, home_town, theater, notes)
OFS = [
    ("Bethlehem Commando",    "Bethlehem",    "north", ""),
    ("Bethulie Commando",     "Bethulie",     "north", ""),
    ("Bloemfontein Commando", "Bloemfontein", "north", ""),
    ("Boshof Commando",       "Boshof",       "north", ""),
    ("Bothaville Commando",   "Bothaville",   "north", ""),
    ("Brandfort Commando",    "Brandfort",    "north", ""),
    ("Edenburg Commando",     "Edenburg",     "north", ""),
    ("Fauresmith Commando",   "Fauresmith",   "north", ""),
    ("Ficksburg Commando",    "Ficksburg",    "north", ""),
    ("Frankfort Commando",    "Frankfort",    "north", ""),
    ("Heilbron Commando",     "Heilbron",     "north", ""),
    ("Hoopstad Commando",     "Hoopstad",     "north", ""),
    ("Jacobsdal Commando",    "Jacobsdal",    "north", ""),
    ("Kroonstad Commando",    "Kroonstad",    "north", ""),
    ("Ladybrand Commando",    "Ladybrand",    "north", ""),
    ("Lindley Commando",      "Lindley",      "north", ""),
    ("Parys Commando",        "Parys",        "north", ""),
    ("Philippolis Commando",  "Philippolis",  "north", ""),
    ("Rouxville Commando",    "Rouxville",    "north", ""),
    ("Senekal Commando",      "Senekal",      "north", ""),
    ("Smithfield Commando",   "Smithfield OFS", "north", ""),
    ("Thaba Nchu Commando",   "Thaba Nchu",   "north", ""),
    ("Ventersburg Commando",  "Ventersburg",  "north", ""),
    ("Vrede Commando",        "Vrede",        "north", ""),
    ("Vredefort Commando",    "Vredefort",    "north", ""),
    ("Wepener Commando",      "Wepener",      "north", ""),
    ("Winburg Commando",      "Winburg",      "north", ""),
]

TVL = [
    ("Bethal Commando",        "Bethal",        "north", ""),
    ("Bloemhof Commando",      "Bloemhof",      "north", ""),
    ("Boksburg Commando",      "Boksburg",      "north", ""),
    ("Carolina Commando",      "Carolina",      "north", ""),
    ("Christiana Commando",    "Christiana",    "north", ""),
    ("Elandsrivier Commando",  "Elandsrivier",  "north", "Near Magaliesberg; site of famous Aug 1900 siege"),
    ("Ermelo Commando",        "Ermelo",        "north", ""),
    ("Fordsburg Commando",     "Johannesburg",  "north", "Fordsburg was a Johannesburg suburb"),
    ("Gatsrand Commando",      "Gatsrand",      "north", ""),
    ("Germiston Commando",     "Germiston",     "north", ""),
    ("Heidelberg Commando",    "Heidelberg (Tvl)", "north", ""),
    ("Jeppestown Commando",    "Johannesburg",  "north", "Jeppestown was a Johannesburg suburb"),
    ("Johannesburg Commando",  "Johannesburg",  "north", ""),
    ("Klerksdorp Commando",    "Klerksdorp",    "north", ""),
    ("Krugersdorp Commando",   "Krugersdorp",   "north", ""),
    ("Lichtenburg Commando",   "Lichtenburg",   "north", ""),
    ("Lydenburg Commando",     "Lydenburg",     "north", ""),
    ("Marico Commando",        "Zeerust",       "north", "Marico district centred near Zeerust"),
    ("Middelburg Commando",    "Middelburg (Tvl)", "north", ""),
    ("Piet Retief Commando",   "Piet Retief",   "north", ""),
    ("Potchefstroom Commando", "Potchefstroom", "north", ""),
    ("Pretoria Commando",      "Pretoria",      "north", ""),
    ("Rustenburg Commando",    "Rustenburg",    "north", ""),
    ("Standerton Commando",    "Standerton",    "north", ""),
    ("Swaziland Commando",     "Piet Retief",   "north", "Operated in Piet Retief/Utrecht district"),
    ("Utrecht Commando",       "Utrecht",       "north", ""),
    ("Vryheid Commando",       "Vryheid",       "north", ""),
    ("Wakkerstroom Commando",  "Wakkerstroom",  "north", ""),
    ("Waterberg Commando",     "Nylstroom",     "north", "Waterberg district, centred near Nylstroom"),
    ("Zoutpansberg Commando",  "Louis Trichardt", "north", "Northern Transvaal"),
    ("Zwartruggens Commando",  "Zwartruggens",  "north", ""),
]

all_commandos = OFS + TVL
rows = []
for i, (name, town, region, note) in enumerate(all_commandos):
    rows.append({
        'id': str(262 + i),
        'side': 'Boer',
        'force': name,
        'commander': '',
        'units': '',
        'date_start': '1899-10-11',
        'date_end': '',
        'event_type': 'deployment',
        'from_place': '',
        'to_place': '',
        'action_place': town,
        'description': f'{name} mobilised at {town} on declaration of war, October 1899, forming part of the Boer republican forces.',
        'confidence': 'high',
        'source': 'angloboerwar.com unit registry; Handbook of the Boer War',
        'note': note,
        '_region': region,
        '_town': town,
    })

# Write fragment
out = 'data/_commandos_fragment.csv'
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    for r in rows:
        w.writerow({k: r.get(k,'') for k in FIELDS})

print(f'Written {len(rows)} rows, IDs {rows[0]["id"]}-{rows[-1]["id"]}')

# Print towns not yet in TOWNS/OVERRIDES so we know what to add
existing_towns = {
    'bethlehem','bethulie','bloemfontein','boshof','bothaville','frankfort',
    'heilbron','jacobsdal','kroonstad','lindley','senekal','wepener','dewetsdorp',
    'reitz','harrismith','carolina','ermelo','heidelberg (tvl)','klerksdorp',
    'krugersdorp','lichtenburg','lydenburg','middelburg (tvl)','piet retief',
    'potchefstroom','pretoria','vryheid','wolmaranstad','zeerust','johannesburg',
    'bloemfontein','gatsrand','frankfort','heilbron',
}
new_towns = set()
for r in rows:
    t = r['_town'].lower()
    if t not in existing_towns:
        new_towns.add(r['_town'])

print('\nNew towns to add to TOWNS dict:')
for t in sorted(new_towns):
    print(f'  "{t}"')

# Print A entries
print('\nA entries:')
for r in rows:
    print(f' "{r["id"]}": dict(pt="{r["_town"]}", region="{r["_region"]}"),')
