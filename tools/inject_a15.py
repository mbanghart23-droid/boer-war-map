"""Inject A dict entries for batch 15 rows (1444-1963) into build_map.py."""
import csv, re

rows = {r['id']: r for r in csv.DictReader(open('data/movements.csv', encoding='utf-8'))}

REGION = {
    "Middelburg (Tvl)": "north", "Belfast": "north", "Carolina": "north",
    "Lydenburg": "north", "Ermelo": "north", "Standerton": "north",
    "Heidelberg (Tvl)": "north", "Johannesburg": "north", "Krugersdorp": "north",
    "Rustenburg": "north", "Lichtenburg": "north", "Mafeking": "north",
    "Klerksdorp": "north", "Potchefstroom": "north",
    "Bloemfontein": "north", "Kroonstad": "north", "Heilbron": "north",
    "Vrede": "north", "Harrismith": "north", "Bethlehem": "north",
    "Senekal": "north", "Ladybrand": "north", "Brandfort": "north",
    "Winburg": "north", "Ventersburg": "north", "Hoopstad": "north",
    "Lindley": "north", "Frankfort": "north", "Vredefort": "north",
    "Boshof": "north", "Parys": "north", "Pretoria": "north",
    "Machadodorp": "north", "Barberton": "north", "Nelspruit": "north",
    "Pietersburg": "north", "Nylstroom": "north", "Zeerust": "north",
    "Christiana": "north", "Bloemhof": "north", "Wolmaranstad": "north",
    "Edenburg": "north", "Fauresmith": "north", "Philippolis": "north",
    "Thaba Nchu": "north", "Ficksburg": "north", "Reitz": "north",
    "Bethulie": "north", "Rouxville": "north", "Wepener": "north",
    "Dewetsdorp": "north", "Sannaspos": "north", "Gatsrand": "north",
    "Elandsrivier": "north", "Magaliesberg": "north", "Boksburg": "north",
    "Germiston": "north", "Heidelberg": "north", "Bethal": "north",
    "Volksrust": "north", "Jacobsdal": "north", "Springfontein": "north",
    "Jakobsdal": "north", "Diamond Hill": "north", "Kimberley": "north",
    "Modder River": "north", "Paardeberg": "north", "Brandwater Basin": "north",
    "Ladysmith": "north", "Dundee": "north", "Newcastle": "north",
    "Laing's Nek": "north", "Pietermaritzburg": "north", "Vryheid": "north",
    "Utrecht": "north", "Wakkerstroom": "north", "Piet Retief": "north",
    "Melmoth": "north", "Estcourt": "north", "Chieveley": "north",
    "Colenso": "north", "Spion Kop": "north", "Talana Hill": "north",
    "Elandslaagte": "north", "Pieters Hill": "north", "Bakenlaagte": "north",
    # EC
    "De Aar": "eastern", "Hanover Road": "eastern", "Colesberg": "eastern",
    "Middelburg (Cape)": "eastern", "Graaff-Reinet": "eastern",
    "Cradock": "eastern", "Queenstown": "eastern", "Aliwal North": "eastern",
    "Grahamstown": "eastern", "Port Elizabeth": "eastern",
    "King William's Town": "eastern", "East London": "eastern",
    "Stormberg": "eastern", "Murraysburg": "eastern", "Hanover": "eastern",
    "Barkly East": "eastern", "Dordrecht": "eastern", "Tarkastad": "eastern",
    "Richmond": "eastern", "Willowmore": "eastern", "Steytlerville": "eastern",
    "Naauwpoort": "eastern", "Burghersdorp": "eastern", "Uitenhage": "eastern",
    "Sterkstroom": "eastern", "Molteno": "eastern", "Indwe": "eastern",
    "Maclear": "eastern", "Lady Grey": "eastern", "Steynsburg": "eastern",
    "Aberdeen": "eastern", "Pearston": "eastern", "Hofmeyr": "eastern",
    "Somerset East": "eastern", "Theebus": "eastern", "Belmont": "eastern",
    "Venterstad": "eastern", "New Bethesda": "eastern", "Klipplaat": "eastern",
    "Sheldon": "eastern", "Mortimer": "eastern", "Jansenville": "eastern",
    "Springbok": "eastern", "Calvinia": "eastern", "Carnarvon": "eastern",
    "Sutherland": "eastern", "Fraserburg": "eastern", "Ladismith": "eastern",
    "Ladismith (Cape)": "eastern", "Vanrhynsdorp": "eastern",
    "Clanwilliam": "eastern", "Lobatsi": "eastern", "Kokstad": "eastern",
    "Bulawayo": "north", "Zwartruggens": "north", "Melmoth": "north",
    "Heidelberg (Tvl)": "north",
}

lines = []
for rid in range(1444, 1964):
    r = rows.get(str(rid))
    if not r:
        continue
    ap = r.get('action_place', '').strip()
    region = REGION.get(ap, 'north')
    fp = r.get('from_place', '').strip()
    tp = r.get('to_place', '').strip()
    if fp and tp and fp != ap:
        lines.append(' "%s": dict(pt="%s", line=(%r, %r), region="%s"),' % (rid, ap, fp, tp, region))
    else:
        lines.append(' "%s": dict(pt="%s", region="%s"),' % (rid, ap, region))

print('A dict entries: %d' % len(lines))

bp = open('build_map.py', encoding='utf-8').read()
old_tail = '"1443": dict(pt="Cradock", line=(\'Aliwal North\', \'Richmond\'), region="eastern"),\n}'
new_tail = '"1443": dict(pt="Cradock", line=(\'Aliwal North\', \'Richmond\'), region="eastern"),\n' + '\n'.join(lines) + '\n}'
new_bp = bp.replace(old_tail, new_tail)
if new_bp == bp:
    print('ERROR: marker not found')
else:
    open('build_map.py', 'w', encoding='utf-8').write(new_bp)
    print('Injected OK')
