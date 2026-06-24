"""Inject A dict entries for ceiling-push rows from _a16_entries.txt (pipe-delimited)."""
import re

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
    "Lobatsi": "north",
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
    for raw in f:
        parts = raw.strip().split('|')
        if len(parts) != 4:
            continue
        rid, ap, fp, tp = parts
        region = REGION.get(ap, 'north')
        if fp and tp and fp != ap:
            lines.append(' "%s": dict(pt="%s", line=(%r, %r), region="%s"),' % (rid, ap, fp, tp, region))
        else:
            lines.append(' "%s": dict(pt="%s", region="%s"),' % (rid, ap, region))

print('Entries to inject: %d' % len(lines))

bp = open('build_map.py', encoding='utf-8').read()
m = re.search(r'( "1963": dict\([^\n]+\),\n)', bp)
if not m:
    print('ERROR: 1963 marker not found')
else:
    marker_end = m.end()
    close_pos = bp.find('\n}', marker_end)
    if close_pos == -1:
        print('ERROR: closing } not found')
    else:
        before = bp[:marker_end]
        after = bp[close_pos + 2:]
        new_bp = before + '\n'.join(lines) + '\n}' + after
        open('build_map.py', 'w', encoding='utf-8').write(new_bp)
        print('Injected OK')
