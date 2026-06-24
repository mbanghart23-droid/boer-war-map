"""Inject A dict entries for ceiling-push rows (1964-4779) into build_map.py."""

REGION = {
    "Middelburg (Tvl)": "north", "Belfast": "north", "Carolina": "north",
    "Lydenburg": "north", "Ermelo": "north", "Standerton": "north",
    "Heidelberg (Tvl)": "north", "Johannesburg": "north", "Krugersdorp": "north",
    "Rustenburg": "north", "Lichtenburg": "north", "Mafeking": "north",
    "Klerksdorp": "north", "Potchefstroom": "north", "Pretoria": "north",
    "Bloemfontein": "north", "Kroonstad": "north", "Heilbron": "north",
    "Vrede": "north", "Harrismith": "north", "Bethlehem": "north",
    "Senekal": "north", "Ladybrand": "north", "Brandfort": "north",
    "Winburg": "north", "Ventersburg": "north", "Hoopstad": "north",
    "Lindley": "north", "Frankfort": "north", "Vredefort": "north",
    "Boshof": "north", "Parys": "north", "Edenburg": "north",
    "Fauresmith": "north", "Philippolis": "north", "Thaba Nchu": "north",
    "Ficksburg": "north", "Reitz": "north", "Bethulie": "north",
    "Rouxville": "north", "Wepener": "north", "Dewetsdorp": "north",
    "Sannaspos": "north", "Brandwater Basin": "north", "Springfontein": "north",
    "Jacobsdal": "north", "Jakobsdal": "north", "Smithfield OFS": "north",
    "Ladysmith": "north", "Dundee": "north", "Newcastle": "north",
    "Laing's Nek": "north", "Pietermaritzburg": "north", "Vryheid": "north",
    "Utrecht": "north", "Wakkerstroom": "north", "Piet Retief": "north",
    "Melmoth": "north", "Estcourt": "north", "Chieveley": "north",
    "Colenso": "north", "Spion Kop": "north", "Talana Hill": "north",
    "Elandslaagte": "north", "Pieters Hill": "north", "Volksrust": "north",
    "Bakenlaagte": "north", "Diamond Hill": "north", "Kimberley": "north",
    "Modder River": "north", "Paardeberg": "north", "Machadodorp": "north",
    "Barberton": "north", "Nelspruit": "north", "Pietersburg": "north",
    "Nylstroom": "north", "Zeerust": "north", "Christiana": "north",
    "Bloemhof": "north", "Wolmaranstad": "north", "Gatsrand": "north",
    "Elandsrivier": "north", "Magaliesberg": "north", "Boksburg": "north",
    "Germiston": "north", "Heidelberg": "north", "Bethal": "north",
    "Springhaan's Nek": "north", "Zwartruggens": "north", "Bulawayo": "north",
    "Lobatsi": "north", "Springfontein": "north",
    # EC
    "De Aar": "eastern", "Hanover Road": "eastern", "Naauwpoort": "eastern",
    "Colesberg": "eastern", "Aliwal North": "eastern", "Queenstown": "eastern",
    "Stormberg": "eastern", "Molteno": "eastern", "Sterkstroom": "eastern",
    "Cradock": "eastern", "Middelburg (Cape)": "eastern", "Graaff-Reinet": "eastern",
    "Aberdeen": "eastern", "Murraysburg": "eastern", "Richmond": "eastern",
    "Hanover": "eastern", "Barkly East": "eastern", "Dordrecht": "eastern",
    "Tarkastad": "eastern", "Willowmore": "eastern", "Steytlerville": "eastern",
    "Klipplaat": "eastern", "Grahamstown": "eastern", "Port Elizabeth": "eastern",
    "Uitenhage": "eastern", "King William's Town": "eastern", "East London": "eastern",
    "Indwe": "eastern", "Maclear": "eastern", "Lady Grey": "eastern",
    "Steynsburg": "eastern", "Pearston": "eastern", "Hofmeyr": "eastern",
    "Somerset East": "eastern", "Theebus": "eastern", "Belmont": "eastern",
    "Venterstad": "eastern", "New Bethesda": "eastern", "Sheldon": "eastern",
    "Mortimer": "eastern", "Jansenville": "eastern", "Burgersdorp": "eastern",
    "Burghersdorp": "eastern", "Kokstad": "eastern", "Springbok": "eastern",
    "Calvinia": "eastern", "Carnarvon": "eastern", "Sutherland": "eastern",
    "Fraserburg": "eastern", "Ladismith": "eastern", "Ladismith (Cape)": "eastern",
    "Vanrhynsdorp": "eastern", "Clanwilliam": "eastern",
}

lines = []
with open('tools/_a16_entries.txt', encoding='utf-8') as f:
    for line in f:
        line = line.rstrip()
        if not line: continue
        # Extract pt (action_place) from line like: "1964": dict(pt="Middelburg (Tvl)", line=(...), region="__"),
        import re
        m = re.match(r' "(\d+)": dict\(pt="([^"]+)", line=\(([^)]+)\), region="__"\),', line)
        if m:
            rid, ap, line_args = m.group(1), m.group(2), m.group(3)
            region = REGION.get(ap, 'north')
            lines.append(' "%s": dict(pt="%s", line=(%s), region="%s"),' % (rid, ap, line_args, region))

print('A dict entries: %d' % len(lines))

bp = open('build_map.py', encoding='utf-8').read()
old_tail = '"1443": dict(pt="Cradock", line=(\'Aliwal North\', \'Richmond\'), region="eastern"),\n'
# Find the last batch 15 entry (around 1963) to use as insertion marker
# Search for the last batch 15 line — look for the entry just before 1964
import re as _re
m = _re.search(r'( "1963": dict\([^\n]+\),\n)\}', bp)
if m:
    old_tail = m.group(1) + '}'
    new_tail = m.group(1) + '\n'.join(lines) + '\n}'
    new_bp = bp.replace(old_tail, new_tail)
    if new_bp == bp:
        print('ERROR: 1963 replacement failed')
    else:
        open('build_map.py','w',encoding='utf-8').write(new_bp)
        print('Injected after 1963 OK')
else:
    # Fallback: find last numbered A dict entry
    last_m = None
    for m2 in _re.finditer(r'( "\d+": dict\([^\n]+\),\n)\}', bp):
        last_m = m2
    if last_m:
        old_tail = last_m.group(1) + '}'
        new_tail = last_m.group(1) + '\n'.join(lines) + '\n}'
        new_bp = bp.replace(old_tail, new_tail)
        if new_bp == bp:
            print('ERROR: fallback replacement failed')
        else:
            open('build_map.py','w',encoding='utf-8').write(new_bp)
            print('Injected via fallback OK')
    else:
        print('ERROR: no injection point found')
