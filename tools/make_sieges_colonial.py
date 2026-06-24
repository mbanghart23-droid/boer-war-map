import csv, json

FIELDS = ['id','side','force','commander','units','date_start','date_end',
          'event_type','from_place','to_place','action_place','description',
          'confidence','source','note']

rows = json.load(open('tools/research_sieges_colonial.json', encoding='utf-8'))
rows.sort(key=lambda r: r.get('date_start','') or '')
for i, r in enumerate(rows):
    r['id'] = str(320 + i)

out = 'data/_sieges_colonial_fragment.csv'
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    for r in rows:
        w.writerow({k: r.get(k,'') for k in FIELDS})

print(f'Written {len(rows)} rows, IDs {rows[0]["id"]}-{rows[-1]["id"]}')
print('\nA entries:')
for r in rows:
    region = r.get('_region', r.get('region', 'north'))
    pt = r['action_place']
    fr = r.get('from_place','')
    to = r.get('to_place','')
    if fr and to:
        print(f' "{r["id"]}": dict(pt="{pt}", line=("{fr}","{to}"), region="{region}"),')
    else:
        print(f' "{r["id"]}": dict(pt="{pt}", region="{region}"),')
