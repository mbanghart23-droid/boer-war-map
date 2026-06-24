"""
Comprehensive audit of movements.csv — produces JSON for Excel export.
"""
import csv, json, re
from collections import defaultdict, Counter

rows = list(csv.DictReader(open('data/movements.csv', encoding='utf-8')))
ids = [r['id'] for r in rows]

# ── 1. ID gaps ──────────────────────────────────────────────────────────────
all_ids = sorted(int(i) for i in ids)
expected = set(range(all_ids[0], all_ids[-1]+1))
gaps_ids = sorted(expected - set(all_ids))

# ── 2. Event type distribution ───────────────────────────────────────────────
by_etype = Counter(r['event_type'] for r in rows)

# ── 3. Thin descriptions (<120 chars or generic "served in") ─────────────────
thin = []
generic_phrases = ['served in south africa','served in the transvaal','served in the ofs',
                   'served in the orange','served in column','served in roberts',
                   'served in buller','served in methuen','served in 1900','served in 1901']
for r in rows:
    d = r['description']
    is_thin = len(d) < 120
    is_generic = any(p in d.lower() for p in generic_phrases)
    if is_thin or is_generic:
        thin.append({'id':r['id'],'force':r['force'],'event_type':r['event_type'],
                     'action_place':r['action_place'],'description':d[:120],
                     'issue':'short (<120)' if is_thin else 'generic "served in"'})

# ── 4. Stacked points (>15 events at same place) ─────────────────────────────
place_counts = Counter(r['action_place'] for r in rows if r['event_type']!='deployment')
engagement_stacks = [(p,c) for p,c in place_counts.most_common(20) if c>3]

deployment_counts = Counter(r['action_place'] for r in rows if r['event_type']=='deployment')
deployment_stacks = [(p,c) for p,c in deployment_counts.most_common(20)]

# ── 5. Major battles audit (should have engagement rows) ────────────────────
MAJOR_BATTLES = [
    ("Talana Hill",         "1899-10-20","Natal — Penn Symons killed"),
    ("Elandslaagte",        "1899-10-21","Natal — Imperial Light Horse glory"),
    ("Lombard's Kop",       "1899-10-30","Natal — White repulsed"),
    ("Modder River",        "1899-11-28","Western — Methuen vs De la Rey"),
    ("Magersfontein",       "1899-12-11","Western — Highland Brigade disaster"),
    ("Stormberg",           "1899-12-10","Eastern Cape — Gatacre's disaster"),
    ("Colenso",             "1899-12-15","Natal — Black Week third defeat"),
    ("Spion Kop",           "1900-01-24","Natal — Tugela debacle"),
    ("Vaal Krantz",         "1900-02-05","Natal — third Tugela attempt"),
    ("Paardeberg",          "1900-02-18","OFS — Cronjé captured"),
    ("Hlangwane",           "1900-02-14","Natal — key to Tugela"),
    ("Dreifontein",         "1900-03-10","OFS — Roberts's advance"),
    ("Karee Siding",        "1900-03-29","OFS — Roberts's advance"),
    ("Sannaspos",           "1900-03-31","OFS — De Wet destroys convoy"),
    ("Wepener siege",       "1900-04-09","OFS — Olivier besieges town"),
    ("Mafeking relief",     "1900-05-17","Western — siege ended"),
    ("Diamond Hill",        "1900-06-11","Transvaal — last major OFS/Tvl battle"),
    ("Bergendal",           "1900-08-27","Transvaal — last conventional battle"),
    ("Nooitgedacht",        "1900-12-13","Transvaal — Clements ambushed"),
    ("Helvetia",            "1901-01-29","Transvaal — Boer night attack"),
    ("Moedwil",             "1901-09-30","Transvaal — De la Rey attacks"),
    ("Bakenlaagte",         "1901-10-30","Transvaal — Botha kills Benson"),
    ("Yzerspruit",          "1902-02-25","Transvaal — De la Rey ambush"),
    ("Tweebosch",           "1902-03-07","Transvaal — De la Rey captures Methuen"),
    ("Rooiwal",             "1902-04-11","Transvaal — last cavalry charge"),
    ("Colesburg operations","1899-12-01","Eastern Cape — French's holding action"),
    ("Elands River Poort",  "1901-09-17","Cape — Smuts ambushes 17th Lancers"),
    ("Okiep siege",         "1902-04-01","Cape — Smuts besieges copper mine"),
]

# Check which have engagement rows
engagement_places = set()
for r in rows:
    if r['event_type'] in ('engagement','battle'):
        engagement_places.add(r['action_place'].lower())
        engagement_places.add(r['force'].lower())
        engagement_places.add(r['description'].lower()[:60])

battle_audit = []
for place, date, note in MAJOR_BATTLES:
    # check if any engagement row mentions this place
    found = any(
        place.lower() in r['action_place'].lower() or
        place.lower() in r['description'].lower() or
        place.lower() in r['force'].lower()
        for r in rows if r['event_type'] in ('engagement','battle','movement')
    )
    battle_audit.append({'battle':place,'expected_date':date,'note':note,
                         'status':'✓ covered' if found else '✗ MISSING'})

# ── 6. Rows with no source ────────────────────────────────────────────────────
no_source = [{'id':r['id'],'force':r['force'],'event_type':r['event_type']}
             for r in rows if not r.get('source','').strip()]

# ── 7. Low-confidence rows ────────────────────────────────────────────────────
low_conf = [{'id':r['id'],'force':r['force'],'action_place':r['action_place'],
             'confidence':r['confidence'],'source':r.get('source','')}
            for r in rows if r.get('confidence','') == 'low']

# ── 8. Eastern Cape coverage check ───────────────────────────────────────────
eastern_places = ['cradock','queenstown','graaff-reinet','middelburg','aliwal north',
                  'stormberg','molteno','dordrecht','indwe','tarkastad','bedford',
                  'somerset east','pearston','murraysburg','richmond','steynsburg',
                  'barkly east','elliot','maclear','lady grey','burgersdorp',
                  'east london','king william','grahamstown','port elizabeth',
                  'uitenhage','hankey','patensie','willowmore','oudtshoorn',
                  'montagu','caledon','swellendam','worcester','tulbagh',
                  'calvinia','clanwilliam','okiep','springbok','namaqualand',
                  'upington','britstown','prieska','colesberg','naauwpoort',
                  'de aar','hanover road','orange river station']

eastern_rows = [r for r in rows if any(p in r['action_place'].lower() or
                p in r['description'].lower() for p in eastern_places)]
eastern_places_covered = Counter(r['action_place'] for r in eastern_rows)

eastern_missing = []
# Key eastern Cape events that should be represented
EASTERN_EVENTS = [
    ("Barkly East","1901","Smuts's commando passed through Barkly East during Cape raid"),
    ("Lady Grey","1901","Cape rebel activity / Smuts's raid route"),
    ("Elliot","1901","Smuts's commando operations eastern Cape"),
    ("Dordrecht","1901","Boer commando raids into Dordrecht district"),
    ("Indwe","1900","Coal mining district; Boer raids on colliery"),
    ("Maclear","1901","Remote eastern Cape town; commando activity"),
    ("Barkly East","1902","Smuts's commando winter quarters"),
    ("Steynsburg","1901","Cape rebel assembly point; Muller's commando"),
    ("Hanover Road","1899","Gatacre's advance base before Stormberg"),
    ("Molteno","1899","Gatacre's force retreated here after Stormberg"),
]
for place, date, note in EASTERN_EVENTS:
    found = any(place.lower() in r['action_place'].lower() or
                place.lower() in r['description'].lower() for r in rows)
    eastern_missing.append({'place':place,'date':date,'note':note,
                            'status':'✓ covered' if found else '✗ MISSING'})

# ── 9. Commander audit ────────────────────────────────────────────────────────
MAJOR_COMMANDERS = [
    ("Roberts, Lord","British","Commander-in-Chief from Jan 1900"),
    ("Kitchener, Lord","British","Chief of Staff then C-in-C from Nov 1900"),
    ("Buller, Sir Redvers","British","Natal Army commander"),
    ("Methuen, Lord","British","Western front, 1st Division"),
    ("French, General","British","Cavalry Division"),
    ("Hunter, General","British","OFS encirclement Jun-Jul 1900"),
    ("White, General","British","Ladysmith garrison"),
    ("Gatacre, General","British","Eastern Cape / 3rd Division"),
    ("Baden-Powell, Colonel","British","Mafeking garrison"),
    ("Botha, Louis","Boer","Transvaal Commandant-General"),
    ("De Wet, Christiaan","Boer","OFS guerrilla commander"),
    ("De la Rey, Koos","Boer","Western Transvaal guerrilla"),
    ("Smuts, Jan","Boer","Cape raid commander 1901-02"),
    ("Joubert, Piet","Boer","Natal invasion commander"),
    ("Prinsloo, Marthinus","Boer","OFS commandant; surrendered Brandwater"),
    ("Cronjé, Piet","Boer","Paardeberg commander; surrendered"),
    ("Hertzog, J.B.M.","Boer","Cape Colony invasion 1901"),
    ("Kritzinger, P.H.","Boer","Eastern Cape guerrilla commander"),
]
cmd_audit = []
for name, side, role in MAJOR_COMMANDERS:
    last = name.split(',')[0].lower()
    found = any(last in (r.get('commander','') or '').lower() or
                last in (r.get('force','') or '').lower() or
                last in (r.get('description','') or '').lower()
                for r in rows)
    cmd_audit.append({'commander':name,'side':side,'role':role,
                      'status':'✓ covered' if found else '✗ MISSING'})

# ── 10. Move lines missing endpoints ────────────────────────────────────────
move_rows = [r for r in rows if r['event_type']=='movement']
no_from = [{'id':r['id'],'force':r['force'],'action_place':r['action_place']}
           for r in move_rows if not r.get('from_place','').strip()]
no_to   = [{'id':r['id'],'force':r['force'],'action_place':r['action_place']}
           for r in move_rows if not r.get('to_place','').strip()]
move_no_line = [{'id':r['id'],'force':r['force'],'action_place':r['action_place']}
                for r in move_rows if not r.get('from_place','').strip() or not r.get('to_place','').strip()]

# ── Summary ──────────────────────────────────────────────────────────────────
summary = {
    'total_rows': len(rows),
    'id_range': f'{ids[0]}-{ids[-1]}',
    'id_gaps': gaps_ids,
    'event_types': dict(by_etype),
    'thin_descriptions': len(thin),
    'no_source': len(no_source),
    'low_confidence': len(low_conf),
    'battles_missing': sum(1 for b in battle_audit if 'MISSING' in b['status']),
    'eastern_events_missing': sum(1 for e in eastern_missing if 'MISSING' in e['status']),
    'commanders_missing': sum(1 for c in cmd_audit if 'MISSING' in c['status']),
    'movement_rows_no_line': len(move_no_line),
}

out = {
    'summary': summary,
    'battle_audit': battle_audit,
    'commander_audit': cmd_audit,
    'eastern_missing': eastern_missing,
    'thin_descriptions': thin[:80],
    'low_confidence': low_conf,
    'no_source': no_source,
    'deployment_stacks': [{'place':p,'count':c} for p,c in deployment_stacks],
    'movement_rows_no_line': move_no_line,
    'id_gaps': gaps_ids,
}
json.dump(out, open('data/audit.json','w',encoding='utf-8'), indent=1, ensure_ascii=False)

print(f"Total rows: {summary['total_rows']}")
print(f"ID gaps: {gaps_ids}")
print(f"Event types: {dict(by_etype)}")
print(f"Thin descriptions: {summary['thin_descriptions']}")
print(f"Battles missing: {summary['battles_missing']}/{len(battle_audit)}")
print(f"Commanders missing: {summary['commanders_missing']}/{len(MAJOR_COMMANDERS)}")
print(f"Eastern events missing: {summary['eastern_events_missing']}/{len(EASTERN_EVENTS)}")
print(f"Movement rows with no line: {summary['movement_rows_no_line']}")
print(f"Low confidence: {summary['low_confidence']}")
print(f"No source: {summary['no_source']}")
print("\nBattle audit:")
for b in battle_audit:
    print(f"  {b['status']}  {b['battle']} ({b['expected_date']})")
print("\nCommander audit:")
for c in cmd_audit:
    print(f"  {c['status']}  {c['commander']}")
