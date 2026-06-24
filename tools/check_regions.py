import csv

r = list(csv.DictReader(open('data/movements.csv', encoding='utf-8')))

cape_keywords = ['stormberg','colesberg','naauwpoort','burgersdorp','aliwal','tarkastad','cradock',
    'middelburg','graaff','de aar','port elizabeth','east london','uitenhage','steynsburg',
    'venterstad','queenstown','jamestown','hanover','richmond','murraysburg','aberdeen',
    'willowmore','oudtshoorn','uniondale','somerset','bedford','rosmead','molteno','dordrecht',
    'elliot','maclear','barkly','eastern cape','scheepers','kritzinger','lotter','malan',
    'fouche','fouch','gorringe','scobell','doran','brabant','french','town guard']

print('Non-Cape rows:')
for row in r:
    places = ' '.join([row['from_place'],row['to_place'],row['action_place'],
                       row['force'],row['units']]).lower()
    if not any(k in places for k in cape_keywords):
        print(f"  {row['id']:5s} {(row['date_start'][:7] if row['date_start'] else '?'):7s} "
              f"{row['side'][:3]} {row['force'][:38]:38s} {row['action_place'][:35]}")

print()
# Count by approximate front
fronts = {'Natal':0,'OFS/Kimberley':0,'Transvaal':0,'Cape':0,'Other':0}
natal_kw = ['ladysmith','natal','colenso','spion','tugela','dundee','talana','elandslaagte',
            'nicholson','lombard','vaal krantz']
ofs_kw = ['bloemfontein','kimberley','paardeberg','modder','magersfontein','belmont','abrahamskraal']
tvl_kw = ['pretoria','johannesburg','diamond hill','bergendal','komati','belfast','lydenburg']

for row in r:
    places = ' '.join([row['from_place'],row['to_place'],row['action_place']]).lower()
    if any(k in places for k in natal_kw):
        fronts['Natal'] += 1
    elif any(k in places for k in ofs_kw):
        fronts['OFS/Kimberley'] += 1
    elif any(k in places for k in tvl_kw):
        fronts['Transvaal'] += 1
    elif any(k in places for k in cape_keywords):
        fronts['Cape'] += 1
    else:
        fronts['Other'] += 1

print('Front coverage (approximate):')
for k,v in fronts.items():
    print(f'  {k:20s} {v}')
