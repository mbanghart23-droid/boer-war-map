"""
SA colonial, Australian, Canadian, NZ, and other imperial units.
IDs start at 419.
"""
import csv

FIELDS = ['id','side','force','commander','units','date_start','date_end',
          'event_type','from_place','to_place','action_place','description',
          'confidence','source','note']

ROWS = [
    # --- CAPE COLONIAL ---
    ("Cape Town Highlanders","Cape Town Highlanders",
     "1900-01-01","deployment","Cape Town","Cape Town","eastern",
     "The Cape Town Highlanders, a colonial volunteer unit, served in the Cape Colony garrison and column operations during the guerrilla phase 1900-02.",
     "high","angloboerwar.com"),

    ("Cape Garrison Artillery","Cape Garrison Artillery",
     "1899-10-01","deployment","Cape Town","Cape Town","eastern",
     "The Cape Garrison Artillery manned coastal and town defences at Cape Town from the outbreak of war, also providing field detachments for column service.",
     "high","angloboerwar.com"),

    ("Border Horse","Border Horse",
     "1900-01-01","deployment","King William's Town","King William's Town","eastern",
     "The Border Horse, raised in the eastern Cape, served in column operations along the Cape-OFS border during the guerrilla phase 1900-02.",
     "high","angloboerwar.com"),

    ("Border Mounted Rifles","Border Mounted Rifles",
     "1899-10-01","deployment","King William's Town","King William's Town","eastern",
     "The Border Mounted Rifles, a long-established eastern Cape colonial unit, served throughout the war providing mounted infantry for eastern Cape defence and column operations.",
     "high","angloboerwar.com"),

    ("Cape Colony Cyclists' Corps","Cape Colony Cyclists' Corps",
     "1900-06-01","deployment","Cape Town","Cape Town","eastern",
     "A cyclist company raised in the Cape Colony for rapid courier and reconnaissance duties during the guerrilla phase.",
     "medium","angloboerwar.com"),

    ("Cape Medical Staff Corps","Cape Medical Staff Corps",
     "1899-10-01","deployment","Cape Town","Cape Town","eastern",
     "The Cape Medical Staff Corps provided medical support to colonial and British forces in the Cape Colony throughout the war.",
     "medium","angloboerwar.com"),

    ("Cape Railway Sharpshooters","Cape Railway Sharpshooters",
     "1900-01-01","deployment","Cape Town","Cape Town","eastern",
     "The Cape Railway Sharpshooters protected the railway lines in the Cape Colony from Boer sabotage and commando raids during 1900-02.",
     "medium","angloboerwar.com"),

    ("East London Rifles","East London Rifles",
     "1900-06-01","deployment","East London","East London","eastern",
     "The East London Rifles, a Cape colonial volunteer corps, served in the eastern Cape and midlands during the guerrilla phase.",
     "medium","angloboerwar.com"),

    ("Kaffrarian Rifles","Kaffrarian Mounted Rifles",
     "1899-10-01","deployment","King William's Town","King William's Town","eastern",
     "The Kaffrarian Rifles (Mounted) were one of the oldest colonial units in the Cape Colony, serving in the eastern Cape throughout the war.",
     "high","angloboerwar.com"),

    ("Queenstown Mounted Rifles","Queenstown Mounted Rifles",
     "1899-10-01","deployment","Queenstown","Queenstown","eastern",
     "The Queenstown Mounted Rifles served in the midland Cape Colony from the outbreak of war, defending against Boer invasions and conducting column operations.",
     "high","angloboerwar.com"),

    ("Griqualand Mounted Rifles","Griqualand Mounted Rifles",
     "1900-01-01","deployment","Kimberley","Kimberley","north",
     "The Griqualand Mounted Rifles served in the northern Cape Colony and the OFS border area during the guerrilla phase.",
     "medium","angloboerwar.com"),

    ("Orpen's Horse","Orpen's Horse",
     "1901-01-01","deployment","Aliwal North","Aliwal North","eastern",
     "Orpen's Horse, an irregular colonial unit, was raised in the eastern Cape for column operations against the Boer guerrilla raiders during 1901-02.",
     "medium","angloboerwar.com"),

    ("Ashburner's Light Horse","Ashburner's Light Horse",
     "1900-06-01","deployment","Cape Town","Cape Town","eastern",
     "Ashburner's Light Horse was raised as an irregular colonial unit in the Cape Colony for guerrilla-phase column operations in 1900-01.",
     "medium","angloboerwar.com"),

    ("Beddy's Scouts","Beddy's Scouts",
     "1901-01-01","deployment","Cradock","Cradock","eastern",
     "Beddy's Scouts, a locally raised irregular unit, conducted intelligence and column duties in the midland Cape Colony during 1901-02.",
     "medium","angloboerwar.com"),

    ("Brett's Scouts","Brett's Scouts",
     "1901-01-01","deployment","Grahamstown","Grahamstown","eastern",
     "Brett's Scouts served in the eastern Cape, providing reconnaissance and escort to British columns during the guerrilla phase.",
     "medium","angloboerwar.com"),

    ("Border Scouts","Border Scouts",
     "1901-06-01","deployment","Aliwal North","Aliwal North","eastern",
     "The Border Scouts were an irregular intelligence unit operating along the Cape-OFS border during the later guerrilla phase.",
     "medium","angloboerwar.com"),

    ("Cape Government Railways","Cape Government Railways",
     "1899-10-01","deployment","Cape Town","Cape Town","eastern",
     "Cape Government Railways personnel served in armoured trains and as track guards throughout the war, critical to the British logistical system.",
     "high","angloboerwar.com"),

    # --- NATAL COLONIAL ---
    ("Natal Mounted Police","Natal Mounted Police",
     "1899-10-01","deployment","Pietermaritzburg","Pietermaritzburg","north",
     "The Natal Mounted Police served from the outbreak of war in Natal, providing colonial mounted police duties and joining field columns; they served in Ladysmith during the siege.",
     "high","Handbook ch.V; angloboerwar.com"),

    ("Natal Volunteers (general)","Natal Volunteers",
     "1899-10-01","deployment","Durban","Durban","north",
     "Natal Volunteer units including the Natal Field Artillery, Natal Naval Volunteers, and various corps served throughout the war in Natal and later in the Transvaal.",
     "high","angloboerwar.com"),

    ("Baca Contingent","Baca Contingent",
     "1900-01-01","deployment","Durban","Durban","north",
     "The Baca Contingent, drawn from the Baca (Mpondomise) people of Natal, provided auxiliary labour and scouting support to British columns.",
     "medium","angloboerwar.com"),

    # --- BECHUANALAND / RHODESIA ---
    ("Bechuanaland Border Police","Bechuanaland Border Police",
     "1899-10-01","deployment","Mafeking","Mafeking","north",
     "The Bechuanaland Border Police formed a key component of the Mafeking garrison during the siege of October 1899 - May 1900 under Colonel Baden-Powell.",
     "high","Conan Doyle ch.20; angloboerwar.com"),

    ("Bechuanaland Rifle Volunteers","Bechuanaland Rifle Volunteers",
     "1899-10-01","deployment","Mafeking","Mafeking","north",
     "The Bechuanaland Rifle Volunteers joined the Mafeking garrison in October 1899 and served throughout the 217-day siege.",
     "high","angloboerwar.com"),

    # --- CANADIAN ---
    ("Canadian Scouts","Canadian Scouts",
     "1901-01-01","deployment","Pretoria","Pretoria","north",
     "The Canadian Scouts, raised by Lieutenant-Colonel Sam Steele and others, served in the Transvaal during the guerrilla phase of 1901-02 conducting independent column operations.",
     "high","angloboerwar.com"),

    ("10th Canadian Field Hospital","10th Canadian Field Hospital",
     "1900-01-01","deployment","Pretoria","Pretoria","north",
     "The 10th Canadian Field Hospital provided medical support to Canadian and British forces in the Transvaal during 1900.",
     "medium","angloboerwar.com"),

    # --- AUSTRALIAN ---
    ("New South Wales Imperial Bushmen","New South Wales Imperial Bushmen",
     "1900-03-01","deployment","Bloemfontein","Bloemfontein","north",
     "The NSW Imperial Bushmen contingent arrived in South Africa in March 1900 and served in the OFS and Transvaal during the advance and guerrilla phases.",
     "high","angloboerwar.com"),

    ("New South Wales Mounted Rifles","New South Wales Mounted Rifles",
     "1900-01-01","deployment","Bloemfontein","Bloemfontein","north",
     "The NSW Mounted Rifles served in the OFS and Transvaal in 1900, contributing to Roberts's advance.",
     "high","angloboerwar.com"),

    ("South Australian Imperial Bushmen","South Australian Imperial Bushmen",
     "1900-03-01","deployment","Bloemfontein","Bloemfontein","north",
     "The South Australian Imperial Bushmen served in the OFS and Transvaal during 1900.",
     "high","angloboerwar.com"),

    ("South Australian Mounted Rifles","South Australian Mounted Rifles",
     "1900-01-01","deployment","Bloemfontein","Bloemfontein","north",
     "The South Australian Mounted Rifles served in the OFS and Transvaal in 1900 as part of the colonial mounted contingent.",
     "high","angloboerwar.com"),

    ("Victorian Imperial Bushmen","Victorian Imperial Bushmen",
     "1900-03-01","deployment","Pretoria","Pretoria","north",
     "The Victorian Imperial Bushmen served in the Transvaal during the advance and early guerrilla phase of 1900.",
     "high","angloboerwar.com"),

    ("1st Queensland Imperial Bushmen","1st Queensland Imperial Bushmen",
     "1900-03-01","deployment","Pretoria","Pretoria","north",
     "The Queensland Imperial Bushmen served in the Transvaal in 1900 as part of the Australian colonial contingent.",
     "high","angloboerwar.com"),

    ("Toronto Company (Mounted Rifles)","Toronto Company",
     "1900-01-01","deployment","Pretoria","Pretoria","north",
     "The Toronto Company of mounted rifles served with the 2nd (Special Service) Battalion Royal Canadian Regiment and later as an independent unit in the Transvaal.",
     "medium","angloboerwar.com"),

    # --- NZ ---
    ("New Zealand 5th Contingent","New Zealand 5th Contingent",
     "1901-01-01","deployment","Pretoria","Pretoria","north",
     "The New Zealand 5th Contingent served in the Transvaal during the guerrilla phase of 1901-02.",
     "high","angloboerwar.com"),

    # --- MISC SUPPORT ---
    ("Army Service Corps","Army Service Corps",
     "1899-10-01","deployment","Cape Town","Cape Town","north",
     "The Army Service Corps provided supply and transport throughout South Africa from the outbreak of war, managing the enormous logistical effort of feeding and supplying the British forces.",
     "high","angloboerwar.com"),

    ("Royal Army Medical Corps","Royal Army Medical Corps",
     "1899-10-01","deployment","Cape Town","Cape Town","north",
     "The Royal Army Medical Corps (formed 1898) served across all theatres in South Africa, establishing field hospitals and casualty clearing stations throughout the war.",
     "high","angloboerwar.com"),

    ("Army Ordnance Department","Army Ordnance Department",
     "1899-10-01","deployment","Cape Town","Cape Town","north",
     "The Army Ordnance Department managed ammunition and equipment supply across South Africa throughout the war.",
     "medium","angloboerwar.com"),

    ("Kimberley Defence Force","Kimberley Defence Force",
     "1899-10-14","deployment","Kimberley","Kimberley","north",
     "The Kimberley Defence Force, including De Beers company employees and local volunteers, formed the core of the town's garrison under Colonel Kekewich during the siege of October 1899 - February 1900.",
     "high","Conan Doyle ch.15; angloboerwar.com"),

    ("Mafeking Town Volunteers","Mafeking Town Guard",
     "1899-10-13","deployment","Mafeking","Mafeking","north",
     "The Mafeking Town Guard and civilian volunteers defended Mafeking under Baden-Powell during the famous 217-day siege from October 1899 to May 1900.",
     "high","Conan Doyle ch.20"),

    ("Durban Volunteers","Durban Volunteers",
     "1899-10-01","deployment","Durban","Durban","north",
     "The Durban Volunteer corps provided coastal and base defence at Durban throughout the war, freeing regular forces for field service.",
     "medium","angloboerwar.com"),

    ("Bayly's Mounted Rifles","Bayly's Mounted Rifles",
     "1901-01-01","deployment","Cradock","Cradock","eastern",
     "Bayly's Mounted Rifles, an irregular colonial unit, served in the eastern Cape during the guerrilla phase of 1901-02.",
     "medium","angloboerwar.com"),
]

rows = []
START_ID = 419
for i, r in enumerate(ROWS):
    (force, units, date_start, event_type, from_place, action_place, region, description, confidence, source) = r
    rows.append({
        'id': str(START_ID + i),
        'side': 'British',
        'force': force,
        'commander': '',
        'units': units,
        'date_start': date_start,
        'date_end': '',
        'event_type': event_type,
        'from_place': from_place,
        'to_place': '',
        'action_place': action_place,
        'description': description,
        'confidence': confidence,
        'source': source,
        'note': '',
        '_region': region,
    })

out = 'data/_colonial_fragment.csv'
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    for r in rows:
        w.writerow({k: r.get(k,'') for k in FIELDS})

print(f'Written {len(rows)} rows, IDs {rows[0]["id"]}-{rows[-1]["id"]}')
print('\nA entries:')
for r in rows:
    print(f' "{r["id"]}": dict(pt="{r["action_place"]}", region="{r["_region"]}"),')
