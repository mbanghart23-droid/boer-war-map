import csv
FIELDS = ['id','side','force','commander','units','date_start','date_end','event_type',
          'from_place','to_place','action_place','description','confidence','source','note']
rows = list(csv.DictReader(open('data/_north_fragment.csv', encoding='utf-8'), fieldnames=FIELDS))
for r in rows:
    fr = r['from_place'][:18] if r['from_place'] else ''
    ap = r['action_place'][:38]
    to = r['to_place'][:18] if r['to_place'] else ''
    print(f"{r['id']:4s} {r['date_start'][:7]} {r['side'][:3]} {fr:18s} {ap:38s} {to}")
