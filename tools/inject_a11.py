"""Inject A dict entries for batch 11 rows (ids 1082-1168) into build_map.py"""
import csv, re

rows = {r['id']:r for r in csv.DictReader(open('data/movements.csv', encoding='utf-8'))}

LOC_MAP = {
    'Bloemfontein': ('Kroonstad', ('Bloemfontein','Kroonstad'), 'north'),
    'Bethal': ('Ermelo', ('Bethal','Ermelo'), 'north'),
    'Bethlehem': ('Harrismith', ('Bethlehem','Harrismith'), 'north'),
    'Bethulie': ('Rouxville', ('Bethulie','Rouxville'), 'north'),
    'Bloemhof': ('Christiana', ('Bloemhof','Christiana'), 'north'),
    'Pretoria': ('Machadodorp', ('Pretoria','Machadodorp'), 'north'),
    'Johannesburg': ('Pretoria', ('Johannesburg','Pretoria'), 'north'),
    'Boshof': ('Hoopstad', ('Boshof','Hoopstad'), 'north'),
    'Bakenlaagte': ('Carolina', ('Bakenlaagte','Carolina'), 'north'),
    'Brandfort': ('Ventersburg', ('Brandfort','Ventersburg'), 'north'),
    'Burghersdorp': ('Aliwal North', ('Burghersdorp','Aliwal North'), 'eastern'),
    'Carolina': ('Lydenburg', ('Carolina','Lydenburg'), 'north'),
    'Christiana': ('Wolmaranstad', ('Christiana','Wolmaranstad'), 'north'),
    'Colesberg': ('Philippolis', ('Colesberg','Philippolis'), 'eastern'),
    'Edenburg': ('Fauresmith', ('Edenburg','Fauresmith'), 'north'),
    'Elandsrivier': ('Lichtenburg', ('Elandsrivier','Lichtenburg'), 'north'),
    'Ermelo': ('Wakkerstroom', ('Ermelo','Wakkerstroom'), 'north'),
    'Fauresmith': ('Philippolis', ('Fauresmith','Philippolis'), 'north'),
    'Ficksburg': ('Bethlehem', ('Ficksburg','Bethlehem'), 'north'),
    'Frankfort': ('Heilbron', ('Frankfort','Heilbron'), 'north'),
    'Gatsrand': ('Potchefstroom', ('Gatsrand','Potchefstroom'), 'north'),
    'Germiston': ('Pretoria', ('Johannesburg','Pretoria'), 'north'),
    'Boksburg': ('Pretoria', ('Johannesburg','Pretoria'), 'north'),
    'Krugersdorp': ('Pretoria', ('Johannesburg','Pretoria'), 'north'),
    'Heidelberg (Tvl)': ('Standerton', ('Heidelberg (Tvl)','Standerton'), 'north'),
    'Harrismith': ('Bethlehem', ('Harrismith','Bethlehem'), 'north'),
    'Heilbron': ('Frankfort', ('Heilbron','Frankfort'), 'north'),
    'Hoopstad': ('Heilbron', ('Hoopstad','Heilbron'), 'north'),
    'Jacobsdal': ('Bloemhof', ('Jacobsdal','Bloemhof'), 'north'),
    'Klerksdorp': ('Wolmaranstad', ('Klerksdorp','Wolmaranstad'), 'north'),
    'Kroonstad': ('Heilbron', ('Kroonstad','Heilbron'), 'north'),
    'Ladybrand': ('Thaba Nchu', ('Ladybrand','Thaba Nchu'), 'north'),
    'Ladysmith': ("Laing's Nek", ('Ladysmith','Volksrust'), 'north'),
    'Lichtenburg': ('Zeerust', ('Lichtenburg','Zeerust'), 'north'),
    'Lindley': ('Heilbron', ('Lindley','Heilbron'), 'north'),
    'Louis Trichardt': ('Nylstroom', ('Louis Trichardt','Nylstroom'), 'north'),
    'Lydenburg': ('Carolina', ('Lydenburg','Carolina'), 'north'),
    'Mafeking': ('Lichtenburg', ('Mafeking','Lichtenburg'), 'north'),
    'Magaliesberg': ('Rustenburg', ('Magaliesberg','Rustenburg'), 'north'),
    'Middelburg (Tvl)': ('Belfast', ('Middelburg (Tvl)','Belfast'), 'north'),
    'Naauwpoort': ('Colesberg', ('Naauwpoort','Colesberg'), 'eastern'),
    'Nylstroom': ('Pretoria', ('Nylstroom','Pretoria'), 'north'),
    'Parys': ('Heilbron', ('Parys','Heilbron'), 'north'),
    'Philippolis': ('Colesberg', ('Philippolis','Colesberg'), 'eastern'),
    'Piet Retief': ('Vryheid', ('Piet Retief','Vryheid'), 'north'),
    'Potchefstroom': ('Klerksdorp', ('Potchefstroom','Klerksdorp'), 'north'),
    'Belfast': ('Machadodorp', ('Belfast','Machadodorp'), 'north'),
    'Rouxville': ('Aliwal North', ('Rouxville','Aliwal North'), 'eastern'),
    'Rustenburg': ('Zeerust', ('Rustenburg','Zeerust'), 'north'),
    'Sannaspos': ('Thaba Nchu', ('Bloemfontein','Thaba Nchu'), 'north'),
    'Senekal': ('Bethlehem', ('Senekal','Bethlehem'), 'north'),
    'Smithfield OFS': ('Rouxville', ('Rouxville','Philippolis'), 'north'),
    'Standerton': ('Ermelo', ('Standerton','Ermelo'), 'north'),
    'Talana Hill': ('Ladysmith', ('Dundee','Ladysmith'), 'north'),
    'Thaba Nchu': ('Ladybrand', ('Thaba Nchu','Ladybrand'), 'north'),
    'Utrecht': ('Vryheid', ('Utrecht','Vryheid'), 'north'),
    'Ventersburg': ('Kroonstad', ('Ventersburg','Kroonstad'), 'north'),
    'Vrede': ('Harrismith', ('Vrede','Harrismith'), 'north'),
    'Vredefort': ('Parys', ('Vredefort','Parys'), 'north'),
    'Vryheid': ('Utrecht', ('Vryheid','Utrecht'), 'north'),
    'Wakkerstroom': ('Ermelo', ('Wakkerstroom','Ermelo'), 'north'),
    'Wepener': ('Ladybrand', ('Wepener','Ladybrand'), 'north'),
    'Winburg': ('Ventersburg', ('Winburg','Ventersburg'), 'north'),
    'Zeerust': ('Lichtenburg', ('Zeerust','Lichtenburg'), 'north'),
    'Zwartruggens': ('Rustenburg', ('Zwartruggens','Rustenburg'), 'north'),
    'Brandwater Basin': None,  # capture = CSV-only
}

lines = []
for rid in range(1082, 1169):
    r = rows.get(str(rid))
    if not r:
        continue
    fp = r.get('from_place','').strip()
    lm = LOC_MAP.get(fp)
    if lm is None:
        continue
    pt, line, region = lm
    if line:
        lines.append(' "%s": dict(pt="%s", line=(%r, %r), region="%s"),' % (rid, pt, line[0], line[1], region))
    else:
        lines.append(' "%s": dict(pt="%s", region="%s"),' % (rid, pt, region))

print('A dict entries to inject: %d' % len(lines))

bp = open('build_map.py', encoding='utf-8').read()
marker = '"1081": dict(pt="Pretoria", line=(\'Bloemfontein\', \'Pretoria\'), region="north"),\n}'
replacement = '"1081": dict(pt="Pretoria", line=(\'Bloemfontein\', \'Pretoria\'), region="north"),\n' + '\n'.join(lines) + '\n}'
new_bp = bp.replace(marker, replacement)
if new_bp == bp:
    print('ERROR: marker not found')
else:
    open('build_map.py','w',encoding='utf-8').write(new_bp)
    print('Injected OK')
