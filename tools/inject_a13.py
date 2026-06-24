"""Inject A dict entries for batch 13 rows (1179-1360)."""
import csv

rows = {r['id']: r for r in csv.DictReader(open('data/movements.csv', encoding='utf-8'))}

REGION = {
    "Cradock": "eastern", "Middelburg (Cape)": "eastern", "Graaff-Reinet": "eastern",
    "Aliwal North": "eastern", "Colesberg": "eastern", "De Aar": "eastern",
    "Port Elizabeth": "eastern", "Grahamstown": "eastern", "Queenstown": "eastern",
    "King William's Town": "eastern", "East London": "eastern",
    "Pretoria": "north", "Bloemfontein": "north", "Kimberley": "north",
    "Ladysmith": "north", "Newcastle": "north", "Ermelo": "north",
    "Standerton": "north", "Belfast": "north", "Middelburg (Tvl)": "north",
    "Lydenburg": "north", "Carolina": "north", "Bethal": "north",
    "Harrismith": "north", "Kroonstad": "north", "Vryheid": "north",
    "Mafeking": "north", "Johannesburg": "north", "Ventersburg": "north",
    "Heilbron": "north", "Frankfort": "north", "Brandfort": "north",
    "Winburg": "north", "Hoopstad": "north", "Potchefstroom": "north",
    "Klerksdorp": "north", "Lichtenburg": "north", "Zeerust": "north",
    "Rustenburg": "north", "Machadodorp": "north",
}

lines = []
for rid in range(1179, 1361):
    r = rows.get(str(rid))
    if not r:
        continue
    ap = r.get('action_place', '').strip()
    region = REGION.get(ap, 'north')
    lines.append(' "%s": dict(pt="%s", region="%s"),' % (rid, ap, region))

print('A dict entries: %d' % len(lines))

bp = open('build_map.py', encoding='utf-8').read()
old_tail = '"1178": dict(pt="Hoopstad", region="north"),\n}'
new_tail = '"1178": dict(pt="Hoopstad", region="north"),\n' + '\n'.join(lines) + '\n}'
new_bp = bp.replace(old_tail, new_tail)
if new_bp == bp:
    print('ERROR: marker not found')
else:
    open('build_map.py', 'w', encoding='utf-8').write(new_bp)
    print('Injected OK')
