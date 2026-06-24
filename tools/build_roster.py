"""
Build master unit roster from angloboerwar.com scrape + source-mined JSON.
Outputs data/unit_roster.json — the authoritative unit list for gap analysis.
"""
import json

# ── BRITISH IMPERIAL UNITS (from angloboerwar.com) ──────────────────────────
imperial = [
    # Cavalry
    {"unit":"10th (Prince of Wales's Own Royal) Hussars","side":"British","type":"cavalry","theater":"All"},
    {"unit":"11th (Prince Albert's Own) Hussars","side":"British","type":"cavalry","theater":"All"},
    {"unit":"12th (Prince of Wales's Royal) Lancers","side":"British","type":"cavalry","theater":"All"},
    {"unit":"13th Hussars","side":"British","type":"cavalry","theater":"All"},
    {"unit":"14th (King's) Hussars","side":"British","type":"cavalry","theater":"All"},
    {"unit":"15th (The King's) Hussars","side":"British","type":"cavalry","theater":"All"},
    {"unit":"16th (Queen's) Lancers","side":"British","type":"cavalry","theater":"All"},
    {"unit":"17th (Duke of Cambridge's Own) Lancers","side":"British","type":"cavalry","theater":"Cape/Transvaal"},
    {"unit":"18th Hussars","side":"British","type":"cavalry","theater":"All"},
    {"unit":"19th (Princess of Wales's Own) Hussars","side":"British","type":"cavalry","theater":"All"},
    {"unit":"1st (King's) Dragoon Guards","side":"British","type":"cavalry","theater":"All"},
    {"unit":"1st (Royal) Dragoons","side":"British","type":"cavalry","theater":"All"},
    {"unit":"20th Hussars","side":"British","type":"cavalry","theater":"All"},
    {"unit":"21st Lancers","side":"British","type":"cavalry","theater":"All"},
    {"unit":"2nd (Queen's Bays) Dragoon Guards","side":"British","type":"cavalry","theater":"All"},
    {"unit":"2nd (Royal Scots Greys) Dragoons","side":"British","type":"cavalry","theater":"All"},
    {"unit":"3rd (Prince of Wales's) Dragoon Guards","side":"British","type":"cavalry","theater":"All"},
    {"unit":"3rd Hussars","side":"British","type":"cavalry","theater":"All"},
    {"unit":"4th (Royal Irish) Dragoon Guards","side":"British","type":"cavalry","theater":"All"},
    {"unit":"4th (The Queen's Own) Hussars","side":"British","type":"cavalry","theater":"All"},
    {"unit":"5th (Princess Charlotte of Wales's) Dragoon Guards","side":"British","type":"cavalry","theater":"All"},
    {"unit":"5th (Royal Irish) Lancers","side":"British","type":"cavalry","theater":"Natal"},
    {"unit":"6th (Inniskilling) Dragoons","side":"British","type":"cavalry","theater":"All"},
    {"unit":"6th Dragoon Guards","side":"British","type":"cavalry","theater":"All"},
    {"unit":"7th (Princess Royal's) Dragoon Guards","side":"British","type":"cavalry","theater":"All"},
    {"unit":"7th (Queen's Own) Hussars","side":"British","type":"cavalry","theater":"All"},
    {"unit":"8th (King's Royal Irish) Hussars","side":"British","type":"cavalry","theater":"All"},
    {"unit":"9th (Queen's Royal) Lancers","side":"British","type":"cavalry","theater":"Cape/OFS"},
    {"unit":"Life Guards","side":"British","type":"cavalry","theater":"All"},
    {"unit":"Royal Horse Guards","side":"British","type":"cavalry","theater":"All"},
    # Infantry
    {"unit":"Argyll and Sutherland Highlanders","side":"British","type":"infantry","theater":"All"},
    {"unit":"Bedfordshire Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"Black Watch","side":"British","type":"infantry","theater":"OFS"},
    {"unit":"Border Regiment","side":"British","type":"infantry","theater":"Transvaal"},
    {"unit":"Cameron Highlanders","side":"British","type":"infantry","theater":"All"},
    {"unit":"Cameronians (Scottish Rifles)","side":"British","type":"infantry","theater":"All"},
    {"unit":"Cheshire Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"City Imperial Volunteers","side":"British","type":"infantry","theater":"OFS/Transvaal"},
    {"unit":"Coldstream Guards","side":"British","type":"infantry","theater":"Cape/OFS"},
    {"unit":"Connaught Rangers","side":"British","type":"infantry","theater":"All"},
    {"unit":"Derbyshire Regiment (Sherwood Foresters)","side":"British","type":"infantry","theater":"All"},
    {"unit":"Devonshire Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"Dorsetshire Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"Duke of Cornwall's Light Infantry","side":"British","type":"infantry","theater":"All"},
    {"unit":"Durham Light Infantry","side":"British","type":"infantry","theater":"All"},
    {"unit":"East Kent Regiment (Buffs)","side":"British","type":"infantry","theater":"All"},
    {"unit":"East Lancashire Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"East Surrey Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"East Yorkshire Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"Essex Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"Gloucestershire Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"Gordon Highlanders","side":"British","type":"infantry","theater":"All"},
    {"unit":"Grenadier Guards","side":"British","type":"infantry","theater":"Cape/OFS"},
    {"unit":"Hampshire Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"Highland Light Infantry","side":"British","type":"infantry","theater":"All"},
    {"unit":"Irish Guards","side":"British","type":"infantry","theater":"All"},
    {"unit":"King's Own Scottish Borderers","side":"British","type":"infantry","theater":"All"},
    {"unit":"King's Royal Rifle Corps","side":"British","type":"infantry","theater":"All"},
    {"unit":"Lancashire Fusiliers","side":"British","type":"infantry","theater":"All"},
    {"unit":"Leicestershire Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"Leinster Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"Lincolnshire Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"Liverpool Regiment (King's)","side":"British","type":"infantry","theater":"All"},
    {"unit":"Loyal North Lancashire Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"Manchester Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"Middlesex Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"Norfolk Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"North Staffordshire Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"Northamptonshire Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"Northumberland Fusiliers","side":"British","type":"infantry","theater":"Transvaal"},
    {"unit":"Oxford Light Infantry","side":"British","type":"infantry","theater":"All"},
    {"unit":"Rifle Brigade","side":"British","type":"infantry","theater":"All"},
    {"unit":"Royal Berkshire Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"Royal Dublin Fusiliers","side":"British","type":"infantry","theater":"All"},
    {"unit":"Royal Fusiliers","side":"British","type":"infantry","theater":"All"},
    {"unit":"Royal Inniskilling Fusiliers","side":"British","type":"infantry","theater":"All"},
    {"unit":"Royal Irish Fusiliers","side":"British","type":"infantry","theater":"All"},
    {"unit":"Royal Irish Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"Royal Irish Rifles","side":"British","type":"infantry","theater":"All"},
    {"unit":"Royal Lancaster Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"Royal Munster Fusiliers","side":"British","type":"infantry","theater":"All"},
    {"unit":"Royal Scots","side":"British","type":"infantry","theater":"Transvaal"},
    {"unit":"Royal Scots Fusiliers","side":"British","type":"infantry","theater":"Transvaal"},
    {"unit":"Royal Sussex Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"Royal Warwickshire Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"Royal Welsh Fusiliers","side":"British","type":"infantry","theater":"Transvaal"},
    {"unit":"Royal West Kent Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"Royal West Surrey Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"Scots Guards","side":"British","type":"infantry","theater":"Cape/OFS"},
    {"unit":"Seaforth Highlanders","side":"British","type":"infantry","theater":"All"},
    {"unit":"Shropshire Light Infantry","side":"British","type":"infantry","theater":"All"},
    {"unit":"Somerset Light Infantry","side":"British","type":"infantry","theater":"All"},
    {"unit":"South Lancashire Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"South Staffordshire Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"South Wales Borderers","side":"British","type":"infantry","theater":"All"},
    {"unit":"Suffolk Regiment","side":"British","type":"infantry","theater":"Transvaal"},
    {"unit":"Welsh Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"West Riding Regiment","side":"British","type":"infantry","theater":"Transvaal"},
    {"unit":"West Yorkshire Regiment","side":"British","type":"infantry","theater":"Transvaal"},
    {"unit":"Wiltshire Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"Worcestershire Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"York and Lancaster Regiment","side":"British","type":"infantry","theater":"All"},
    {"unit":"Yorkshire Light Infantry","side":"British","type":"infantry","theater":"All"},
    {"unit":"Yorkshire Regiment","side":"British","type":"infantry","theater":"All"},
    # Guards
    # Support
    {"unit":"Army Chaplains Department","side":"British","type":"support","theater":"All"},
    {"unit":"Army Ordnance Department","side":"British","type":"support","theater":"All"},
    {"unit":"Army Pay Corps","side":"British","type":"support","theater":"All"},
    {"unit":"Army Post Office Corps","side":"British","type":"support","theater":"All"},
    {"unit":"Army Service Corps","side":"British","type":"support","theater":"All"},
    {"unit":"Army Veterinary Corps","side":"British","type":"support","theater":"All"},
    {"unit":"Royal Army Medical Corps","side":"British","type":"support","theater":"All"},
    {"unit":"Military Foot Police","side":"British","type":"support","theater":"All"},
    {"unit":"Military Mounted Police","side":"British","type":"support","theater":"All"},
    {"unit":"Militia","side":"British","type":"garrison","theater":"All"},
    {"unit":"Lovat's Scouts","side":"British","type":"mounted_infantry","theater":"Cape"},
    {"unit":"Scottish Cyclist Company","side":"British","type":"infantry","theater":"All"},
    {"unit":"Elswick Battery","side":"British","type":"artillery","theater":"Natal"},
    {"unit":"Royal Garrison Artillery","side":"British","type":"artillery","theater":"All"},
    {"unit":"Royal Regiment of Artillery","side":"British","type":"artillery","theater":"All"},
    # Royal Engineers sub-units are in subcategory (54 entries) — roll up
    {"unit":"Royal Engineers","side":"British","type":"engineers","theater":"All"},
    {"unit":"Royal Field Artillery","side":"British","type":"artillery","theater":"All"},
    {"unit":"Royal Horse Artillery","side":"British","type":"artillery","theater":"All"},
]

# ── IMPERIAL YEOMANRY (battalion level) ─────────────────────────────────────
yeomanry_btns = [
    "1st Btn Imperial Yeomanry","2nd Btn Imperial Yeomanry","3rd Btn Imperial Yeomanry",
    "4th Btn Imperial Yeomanry","5th Btn Imperial Yeomanry","6th Btn Imperial Yeomanry",
    "7th Btn Imperial Yeomanry","8th Btn Imperial Yeomanry","9th Btn Imperial Yeomanry",
    "10th Btn Imperial Yeomanry","11th Btn Imperial Yeomanry","12th Btn Imperial Yeomanry",
    "13th Btn Imperial Yeomanry","15th Btn Imperial Yeomanry","17th Btn Imperial Yeomanry",
    "18th Btn Imperial Yeomanry","19th Btn Imperial Yeomanry","20th Btn Imperial Yeomanry",
    "21st Btn Imperial Yeomanry","22nd Btn Imperial Yeomanry","23rd Btn Imperial Yeomanry",
    "24th Btn Imperial Yeomanry","25th Btn Imperial Yeomanry","26th Btn Imperial Yeomanry",
    "27th Btn Imperial Yeomanry","28th Btn Imperial Yeomanry","29th Btn Imperial Yeomanry",
    "30th Btn Imperial Yeomanry","31st Btn Imperial Yeomanry","32nd Btn Imperial Yeomanry",
    "33rd Btn Imperial Yeomanry","34th Btn Imperial Yeomanry","35th Btn Imperial Yeomanry",
    "36th Btn Imperial Yeomanry",
    "Imperial Yeomanry Hospital",
]
yeomanry = [{"unit": u, "side": "British", "type": "yeomanry", "theater": "All"} for u in yeomanry_btns]

# ── OFS COMMANDOS ────────────────────────────────────────────────────────────
ofs_commandos = [
    "Bethlehem Commando","Bethulie Commando","Bloemfontein Commando","Boshof Commando",
    "Bothaville Commando","Brandfort Commando","Edenburg Commando","Fauresmith Commando",
    "Ficksburg Commando","Frankfort Commando","Heilbron Commando","Hoopstad Commando",
    "Jacobsdal Commando","Kroonstad Commando","Ladybrand Commando","Lindley Commando",
    "Parys Commando","Philippolis Commando","Rouxville Commando","Senekal Commando",
    "Smithfield Commando","Thaba Nchu Commando","Ventersburg Commando","Vrede Commando",
    "Vredefort Commando","Wepener Commando","Winburg Commando",
]
boer_ofs = [{"unit": u, "side": "Boer", "type": "commando", "theater": "OFS"} for u in ofs_commandos]

# ── TRANSVAAL COMMANDOS ──────────────────────────────────────────────────────
tvl_commandos = [
    "Bethal Commando","Bloemhof Commando","Boksburg Commando","Carolina Commando",
    "Christiana Commando","Elandsrivier Commando","Ermelo Commando","Fordsburg Commando",
    "Gatsrand Commando","Germiston Commando","Heidelberg Commando","Jeppestown Commando",
    "Johannesburg Commando","Klerksdorp Commando","Krugersdorp Commando","Lichtenburg Commando",
    "Lydenburg Commando","Marico Commando","Middelburg Commando","Piet Retief Commando",
    "Potchefstroom Commando","Pretoria Commando","Rustenburg Commando","Standerton Commando",
    "Swaziland Commando","Utrecht Commando","Vryheid Commando","Wakkerstroom Commando",
    "Waterberg Commando","Zoutpansberg Commando","Zwartruggens Commando",
    # Additional from source mining
    "Artillerie (OFS)","Foreign volunteers",
]
boer_tvl = [{"unit": u, "side": "Boer", "type": "commando", "theater": "Transvaal"} for u in tvl_commandos]

# ── SOUTH AFRICAN COLONIAL UNITS ─────────────────────────────────────────────
sa_units = [
    "Ashburner's Light Horse","Baca Contingent","Bechuanaland Rifle Volunteers","Beddy's Scouts",
    "Bethune's Mounted Infantry","Border Horse","Border Mounted Rifles","Border Scouts",
    "Brabant's Horse","Brett's Scouts","British South Africa Police","Burgher Camps Department",
    "Bush Veldt Carbineers","Canadian Scouts","Cape Colonial Forces","Cape Colony Cyclists' Corps",
    "Cape Colony Volunteers","Cape Garrison Artillery","Cape Government Railways",
    "Cape Infantry","Cape Medical Staff Corps","Cape Mounted Rifles","Cape Police",
    "Cape Railway Sharpshooters","Cape Town Highlanders","Clarke's Light Horse","Colonial Light Horse",
    "Colonial Scouts","Commander in Chief's Body Guard","Corps of Cattle Rangers","Cullinan's Horse",
    "Damant's Horse","De Beers Maxim Battery","Dennison's Scouts","Diamond Fields Artillery",
    "Diamond Fields Horse","District Mounted Rifles","Driscoll's Scouts",
    "Duke of Edinburgh's Own Volunteer Rifles","Durban Light Infantry","East Griqualand Field Force",
    "East Griqualand Mounted Rifles","Eastern Province Horse","Field Intelligence Department",
    "Fingo Levies","First City (Grahamstown) Volunteers","French's Scouts","Frontier Light Horse",
    "Frontier Mounted Rifles","Gorringe's Flying Column","Imperial Bearer Corps",
    "Imperial Hospital Corps","Imperial Light Horse","Imperial Light Infantry",
    "Imperial Military Railways","Imperial Transport Service","Imperial Yeomanry Scouts",
    "Johannesburg Mounted Rifles","Kaffrarian Rifles","Kimberley Mounted Corps","Kimberley Regiment",
    "Kitchener's Fighting Scouts","Kitchener's Horse","Loch's Horse","Marshall's Horse",
    "Midland Mounted Rifles","Montmorency's Scouts","Murray's Horse and Scouts",
    "Namaqualand Border Scouts","Natal Carbineers","Natal Field Artillery","Natal Government Railways",
    "Natal Guides","Natal Mounted Infantry","Natal Mounted Rifles","Natal Naval Volunteers",
    "Natal Police","Natal Royal Rifles","Natal Volunteer Composite Regiment",
    "National Scouts","Nesbitt's Horse","Orange River Scouts","Orpen's Light Horse",
    "Prince Alfred's Guard Mounted Infantry","Prince of Wales' Light Horse","Protectorate Regiment",
    "Queensland Contingents","Railway Pioneer Regiment","Rand Rifles","Rhodesia Regiment",
    "Rhodesian Volunteers","Roberts' Horse","Ross Machine Gun Battery","Scottish Horse",
    "South African Constabulary","South African Light Horse","South African Mounted Irregular Forces",
    "Steinaecker's Horse","Thorneycroft's Mounted Infantry","Town Guard and District Mounted Troops",
    "Umvoti Mounted Rifles","Warren's Mounted Infantry","Western Light Horse",
    "Western Province Mounted Rifles","Mafeking Cadet Corps","Mafeking Railway Volunteers",
]
colonial_sa = [{"unit": u, "side": "Colonial", "type": "colonial", "theater": "Cape/Natal"} for u in sa_units]

# ── AUSTRALIAN / NZ / CANADIAN ───────────────────────────────────────────────
colonial_other = [
    {"unit":"Queensland Contingents","side":"Colonial","type":"colonial","theater":"All"},
    {"unit":"West Australian Contingents","side":"Colonial","type":"colonial","theater":"All"},
    {"unit":"Victorian Contingents","side":"Colonial","type":"colonial","theater":"All"},
    {"unit":"Tasmanian Contingents","side":"Colonial","type":"colonial","theater":"All"},
    {"unit":"South Australian Contingents","side":"Colonial","type":"colonial","theater":"All"},
    {"unit":"New South Wales Contingents","side":"Colonial","type":"colonial","theater":"All"},
    {"unit":"New Zealand - 1st Contingent","side":"Colonial","type":"colonial","theater":"All"},
    {"unit":"New Zealand - 2nd Contingent","side":"Colonial","type":"colonial","theater":"All"},
    {"unit":"New Zealand - 3rd Contingent","side":"Colonial","type":"colonial","theater":"All"},
    {"unit":"New Zealand - 4th Contingent","side":"Colonial","type":"colonial","theater":"All"},
    {"unit":"New Zealand - 5th Contingent","side":"Colonial","type":"colonial","theater":"All"},
    {"unit":"New Zealand - 6th Contingent","side":"Colonial","type":"colonial","theater":"All"},
    {"unit":"New Zealand - 7th Contingent","side":"Colonial","type":"colonial","theater":"All"},
    {"unit":"New Zealand - 8th Contingent","side":"Colonial","type":"colonial","theater":"All"},
    {"unit":"New Zealand - 9th Contingent","side":"Colonial","type":"colonial","theater":"All"},
    {"unit":"New Zealand - 10th Contingent","side":"Colonial","type":"colonial","theater":"All"},
    {"unit":"1st Canadian Mounted Rifles (Royal Canadian Dragoons)","side":"Colonial","type":"cavalry","theater":"All"},
    {"unit":"2nd Canadian Mounted Rifles","side":"Colonial","type":"cavalry","theater":"All"},
    {"unit":"Strathcona's Horse","side":"Colonial","type":"cavalry","theater":"All"},
    {"unit":"Royal Canadian Regiment of Infantry","side":"Colonial","type":"infantry","theater":"OFS"},
    {"unit":"Royal Canadian Artillery","side":"Colonial","type":"artillery","theater":"All"},
    {"unit":"10th Canadian Field Hospital","side":"Colonial","type":"support","theater":"All"},
]

# ── COMBINE ALL ──────────────────────────────────────────────────────────────
all_units = imperial + yeomanry + boer_ofs + boer_tvl + colonial_sa + colonial_other

# Add source-mined units that aren't already covered
# (load the agent output if it exists)
import os
src = 'boer_war_units.json'
if os.path.exists(src):
    mined = json.load(open(src, encoding='utf-8'))
    existing_names = {u['unit'].lower() for u in all_units}
    added = 0
    for m in mined:
        nm = m.get('unit','').lower()
        if nm and nm not in existing_names:
            all_units.append(m)
            existing_names.add(nm)
            added += 1
    print(f'Added {added} units from source mining')

# Deduplicate by unit name (case-insensitive)
seen = set()
deduped = []
for u in all_units:
    k = u['unit'].lower()
    if k not in seen:
        seen.add(k)
        deduped.append(u)

out = 'data/unit_roster.json'
json.dump(deduped, open(out, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print(f'Master roster: {len(deduped)} units -> {out}')

# Summary by type
from collections import Counter
types = Counter(u.get('type','?') for u in deduped)
sides = Counter(u.get('side','?') for u in deduped)
print('By side:', dict(sides))
print('By type:', dict(types.most_common()))
