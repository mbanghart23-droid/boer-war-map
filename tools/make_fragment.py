"""
Combine three research JSON files, assign sequential IDs starting at 191,
and write a CSV fragment ready to append to data/movements.csv.
"""
import csv, json, sys

FIELDNAMES = ['id','side','force','commander','units','date_start','date_end',
              'event_type','from_place','to_place','action_place','description',
              'confidence','source','note']

natal   = json.load(open('tools/research_natal.json',    encoding='utf-8'))
tvl     = json.load(open('tools/research_transvaal.json', encoding='utf-8'))
ofs     = json.load(open('tools/research_ofs.json',       encoding='utf-8'))

# Tag source front for reference
for r in natal: r['_front'] = 'natal'
for r in tvl:   r['_front'] = 'tvl'
for r in ofs:   r['_front'] = 'ofs'

all_rows = natal + tvl + ofs

# Sort by date so CSV reads chronologically
all_rows.sort(key=lambda r: r.get('date_start','') or '')

# Assign IDs 191+
for i, r in enumerate(all_rows):
    r['id'] = str(191 + i)

# Write fragment
out = 'data/_north_fragment.csv'
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=FIELDNAMES)
    for r in all_rows:
        w.writerow({k: r.get(k,'') for k in FIELDNAMES})

print(f'Written {len(all_rows)} rows to {out}')
print('IDs:', all_rows[0]['id'], '–', all_rows[-1]['id'])

# Print summary by front
from collections import Counter
fronts = Counter(r['_front'] for r in all_rows)
print('Natal:', fronts['natal'], '| TVL:', fronts['tvl'], '| OFS:', fronts['ofs'])
