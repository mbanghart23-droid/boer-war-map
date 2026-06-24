"""
Cross-reference unit_roster.json against movements.csv units field.
Output: data/unit_gaps.json — units with zero map presence.
"""
import csv, json, re
from collections import defaultdict

roster = json.load(open('data/unit_roster.json', encoding='utf-8'))
rows = list(csv.DictReader(open('data/movements.csv', encoding='utf-8')))

# Build set of all unit tokens already in the CSV
# Units field is semicolon-separated; also check force/commander fields
covered_tokens = set()
for row in rows:
    for field in ['units', 'force', 'commander']:
        val = row.get(field, '')
        if val:
            for tok in re.split(r'[;,]', val):
                covered_tokens.add(tok.strip().lower())

def is_covered(unit_name):
    nm = unit_name.lower()
    # Direct match
    if nm in covered_tokens:
        return True
    # Substring match — if the unit name appears anywhere in the covered tokens
    for tok in covered_tokens:
        if nm in tok or tok in nm:
            if len(tok) > 4:  # avoid false positives on short words
                return True
    return False

gaps = []
covered = []
for u in roster:
    if is_covered(u['unit']):
        covered.append(u['unit'])
    else:
        gaps.append(u)

json.dump(gaps, open('data/unit_gaps.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

print(f'Total roster: {len(roster)}')
print(f'Already covered: {len(covered)}')
print(f'Gaps (no map presence): {len(gaps)}')
print()

# Group gaps by type
from collections import Counter
by_type = defaultdict(list)
for u in gaps:
    by_type[u.get('type','?')].append(u['unit'])

for t, units in sorted(by_type.items()):
    print(f'\n--- {t.upper()} ({len(units)}) ---')
    for u in sorted(units)[:20]:
        print(f'  {u}')
    if len(units) > 20:
        print(f'  ... and {len(units)-20} more')
