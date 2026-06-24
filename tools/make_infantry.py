"""
One deployment/action row per ungapped British infantry regiment.
IDs start at 356.
"""
import csv, json

FIELDS = ['id','side','force','commander','units','date_start','date_end',
          'event_type','from_place','to_place','action_place','description',
          'confidence','source','note']

# (force, units, date_start, event_type, from_place, to_place, action_place,
#  description, confidence, source, region)
ROWS = [
    # --- HIGHLAND BRIGADE (Methuen / 1st Division, OFS) ---
    ("Highland Brigade","Black Watch;Seaforth Highlanders;Highland Light Infantry;Argyll and Sutherland Highlanders",
     "1899-11-20","deployment","England","Cape Town","Cape Town",
     "The Highland Brigade (Black Watch, Seaforth Highlanders, HLI, A&SH) under Major-General Wauchope arrived at Cape Town in late November 1899 and joined Methuen's 1st Division for the advance on Kimberley.",
     "high","Conan Doyle ch.13; Handbook ch.IX","north"),

    ("Highland Brigade","Black Watch;Seaforth Highlanders;Highland Light Infantry;Argyll and Sutherland Highlanders",
     "1899-12-11","engagement","Modder River","","Magersfontein",
     "At Magersfontein on 11 December 1899 the Highland Brigade advanced in massed night formation and was caught in open ground at dawn by Boer rifles; Major-General Wauchope was killed and the brigade suffered 750 casualties before withdrawing.",
     "high","Conan Doyle ch.13; Handbook ch.IX p.199","north"),

    # --- GUARDS BRIGADE ---
    ("Guards Brigade","Grenadier Guards;Coldstream Guards;Scots Guards",
     "1899-11-15","deployment","England","Cape Town","Belmont",
     "The Guards Brigade (Grenadier, Coldstream, Scots Guards) under Methuen fought at Belmont and Modder River in November 1899 before the check at Magersfontein; they subsequently garrisoned the line of communications in the OFS.",
     "high","Conan Doyle ch.13","north"),

    ("Irish Guards","Irish Guards",
     "1900-03-01","deployment","England","Cape Town","Orange Free State",
     "The Irish Guards, newly raised in 1900, arrived in South Africa and served in the OFS during the advance phase, providing garrison duties and line-of-communications protection.",
     "medium","angloboerwar.com unit registry","north"),

    # --- NATAL BRIGADES (Symons/Penn Symons, White, Buller) ---
    ("1st Natal Brigade","Royal Dublin Fusiliers;Royal Inniskilling Fusiliers;Royal Irish Fusiliers",
     "1899-10-13","deployment","England","Durban","Dundee",
     "The 1st Natal Brigade under Penn Symons concentrated at Dundee in October 1899; the Royal Dublin Fusiliers, Royal Inniskilling Fusiliers, and Royal Irish Fusiliers were heavily engaged at Talana Hill on 20 October before the force retreated to Ladysmith.",
     "high","Conan Doyle ch.6; Handbook ch.IV","north"),

    ("Natal force","Devonshire Regiment;Gordon Highlanders;Manchester Regiment",
     "1899-10-01","deployment","England","Durban","Ladysmith",
     "The Devonshire Regiment, Gordon Highlanders, and Manchester Regiment formed part of White's Ladysmith garrison; the Gordons and Devons fought at Elandslaagte on 21 October 1899 and were besieged in Ladysmith from November 1899 to February 1900.",
     "high","Conan Doyle ch.7; Handbook ch.V","north"),

    ("Natal force","King's Royal Rifle Corps;Rifle Brigade",
     "1899-11-01","deployment","England","Durban","Ladysmith",
     "The King's Royal Rifle Corps and Rifle Brigade were among the regiments besieged in Ladysmith from November 1899 to February 1900 as part of White's garrison.",
     "high","Handbook ch.V","north"),

    ("Natal force","Leicesters;Liverpools;Gloucestershire Regiment",
     "1899-11-01","deployment","England","Durban","Ladysmith",
     "The Leicester Regiment, King's Liverpool Regiment, and Gloucestershire Regiment formed part of White's Ladysmith garrison during the siege from November 1899 to February 1900.",
     "high","Handbook ch.V","north"),

    ("Natal force — 2nd Brigade","Royal Fusiliers;East Surrey Regiment;West Yorkshire Regiment",
     "1899-12-01","deployment","England","Durban","Natal",
     "The Royal Fusiliers, East Surrey Regiment, and West Yorkshire Regiment arrived in Natal as part of Buller's reinforcing divisions and served in the Tugela operations from December 1899 to February 1900.",
     "high","Handbook ch.X; Conan Doyle ch.11","north"),

    ("Natal force","Connaught Rangers;Royal Inniskilling Fusiliers",
     "1900-01-01","deployment","Ireland","Durban","Natal",
     "The Connaught Rangers and further battalions of the Royal Inniskilling Fusiliers served in Buller's Natal Army during the Tugela campaign and the advance into the Transvaal via Laing's Nek.",
     "high","Handbook ch.XIII","north"),

    ("5th (Irish) Brigade — Natal","Leinster Regiment;Royal Munster Fusiliers;Royal Dublin Fusiliers",
     "1900-01-01","engagement","","","Spion Kop",
     "The 5th (Irish) Brigade including the Leinster Regiment, Royal Munster Fusiliers, and Royal Dublin Fusiliers fought at Spion Kop in January 1900, suffering heavy casualties on the summit alongside the Lancashire Fusiliers.",
     "high","Conan Doyle ch.12; Handbook ch.XI","north"),

    # --- ROBERTS'S MAIN ARMY (OFS / Transvaal advance 1900) ---
    ("6th Division","Lincolnshire Regiment;Royal Scots Fusiliers",
     "1900-01-01","deployment","England","Cape Town","Orange Free State",
     "The Lincolnshire Regiment and Royal Scots Fusiliers formed part of the 6th Division that advanced with Roberts from the Modder River to Bloemfontein and Pretoria in early 1900.",
     "high","Handbook ch.XII","north"),

    ("7th Division","Norfolk Regiment;South Lancashire Regiment;Cheshire Regiment",
     "1900-01-01","deployment","England","Cape Town","Orange Free State",
     "The Norfolk Regiment, South Lancashire Regiment, and Cheshire Regiment served in the 7th Division of Roberts's main army during the advance through the OFS to Pretoria in 1900.",
     "high","Handbook ch.XII","north"),

    ("8th Division","Worcestershire Regiment;Durham Light Infantry;East Lancashire Regiment",
     "1900-02-01","deployment","England","Cape Town","Orange Free State",
     "The Worcestershire Regiment, Durham Light Infantry, and East Lancashire Regiment formed part of the 8th Division that advanced under Roberts from the Orange River to Bloemfontein and beyond in early 1900.",
     "high","Handbook ch.XII","north"),

    ("9th Division","Essex Regiment;Warwickshire Regiment;Welsh Regiment",
     "1900-02-01","deployment","England","Cape Town","Orange Free State",
     "The Essex Regiment, Royal Warwickshire Regiment, and Welsh Regiment served in the 9th Division that crossed the Orange River with Roberts and fought through the OFS in 1900.",
     "high","Handbook ch.XII","north"),

    ("11th Division","Berkshire Regiment;East Yorkshire Regiment;Yorkshires",
     "1900-03-01","deployment","England","Cape Town","Orange Free State",
     "The Royal Berkshire Regiment, East Yorkshire Regiment, and Yorkshire Regiment served in the 11th Division that formed part of Roberts's main army advancing from the Orange River Colony to the Transvaal.",
     "high","Handbook ch.XII","north"),

    ("Roberts's army","Somerset Light Infantry;Northamptonshire Regiment",
     "1900-01-01","deployment","England","Cape Town","Orange Free State",
     "The Somerset Light Infantry and Northamptonshire Regiment arrived in South Africa with Roberts's reinforcements and served in the OFS advance from February 1900.",
     "high","Handbook ch.XII","north"),

    ("Roberts's army","Oxford Light Infantry;Wiltshire Regiment",
     "1900-01-01","deployment","England","Cape Town","Orange Free State",
     "The Oxfordshire Light Infantry and Wiltshire Regiment served in Roberts's main army during the advance through the OFS and into the Transvaal in 1900.",
     "high","Handbook ch.XII","north"),

    ("Roberts's army","East Kent Regiment;Hampshire Regiment",
     "1900-02-01","deployment","England","Cape Town","Orange Free State",
     "The East Kent Regiment (Buffs) and Hampshire Regiment served with Roberts's main army in the OFS and Transvaal campaigns of 1900.",
     "high","Handbook ch.XII","north"),

    ("Roberts's army","North Staffordshire Regiment;York and Lancaster Regiment",
     "1900-02-01","deployment","England","Cape Town","Orange Free State",
     "The North Staffordshire Regiment and York and Lancaster Regiment served in Roberts's columns advancing through the OFS and into the Transvaal in 1900.",
     "high","Handbook ch.XII","north"),

    ("Roberts's army","South Wales Borderers;South Staffordshire Regiment",
     "1900-02-01","deployment","England","Cape Town","Orange Free State",
     "The South Wales Borderers and South Staffordshire Regiment served with Roberts's main army during the advance from the Orange River to Pretoria in 1900.",
     "high","Handbook ch.XII","north"),

    ("Methuen's column","Loyal North Lancashire Regiment;Northumberland Fusiliers",
     "1899-11-01","deployment","England","Cape Town","Modder River",
     "The Loyal North Lancashire Regiment garrisoned Kimberley and joined Methuen's force; the Northumberland Fusiliers served in the western Transvaal and suffered heavily at Nooitgedacht in December 1900.",
     "high","Conan Doyle ch.31","north"),

    # --- CAPE / EASTERN THEATRE ---
    ("Cape Colony force","Cameron Highlanders;Cameronians;Bedfordshire Regiment",
     "1900-06-01","deployment","England","Cape Town","Cape Colony",
     "The Cameron Highlanders, Cameronians (Scottish Rifles), and Bedfordshire Regiment served in the Cape Colony theatre during 1900-01, providing garrisons and column escorts as the guerrilla campaign spread southward.",
     "high","angloboerwar.com; Handbook ch.XIV","eastern"),

    ("Cape Colony force","King's Own Scottish Borderers;Middlesex Regiment",
     "1900-06-01","deployment","England","Cape Town","Cape Colony",
     "The King's Own Scottish Borderers and Middlesex Regiment served as part of the Cape Colony garrison and column forces during the guerrilla phase 1900-02.",
     "high","angloboerwar.com","eastern"),

    ("Royal West Surrey Regiment","Royal West Surrey Regiment",
     "1900-06-01","deployment","England","Cape Town","Cape Colony",
     "The Royal West Surrey Regiment (Queen's) served in the Cape Colony during the guerrilla phase, providing garrison and column duties in the midland districts.",
     "high","angloboerwar.com","eastern"),

    ("Royal West Kent Regiment","Royal West Kent Regiment",
     "1900-06-01","deployment","England","Cape Town","Cape Colony",
     "The Royal West Kent Regiment served in the Cape Colony and later the ORC during the guerrilla phase 1900-02.",
     "high","angloboerwar.com","eastern"),

    ("Royal Irish Rifles","Royal Irish Rifles",
     "1899-11-01","deployment","Ireland","Cape Town","Natal",
     "The Royal Irish Rifles served in South Africa during 1900-01, operating in the Natal and Transvaal theatres during the guerrilla phase.",
     "high","angloboerwar.com","north"),

    ("Royal Sussex Regiment","Royal Sussex Regiment",
     "1900-06-01","deployment","England","Cape Town","Transvaal",
     "The Royal Sussex Regiment served in the Transvaal during the guerrilla phase as part of Bruce Hamilton's 21st Brigade, participating in column drives.",
     "high","angloboerwar.com","north"),
]

rows = []
for i, r in enumerate(ROWS):
    (force,units,date_start,event_type,from_place,to_place,action_place,
     description,confidence,source,region) = r
    rows.append({
        'id': str(356 + i),
        'side': 'British',
        'force': force,
        'commander': '',
        'units': units,
        'date_start': date_start,
        'date_end': '',
        'event_type': event_type,
        'from_place': from_place,
        'to_place': to_place,
        'action_place': action_place,
        'description': description,
        'confidence': confidence,
        'source': source,
        'note': '',
        '_region': region,
    })

out = 'data/_infantry_fragment.csv'
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    for r in rows:
        w.writerow({k: r.get(k,'') for k in FIELDS})

print(f'Written {len(rows)} rows, IDs {rows[0]["id"]}-{rows[-1]["id"]}')
print('\nA entries:')
for r in rows:
    region = r['_region']
    pt = r['action_place']
    fr = r.get('from_place','')
    to = r.get('to_place','')
    if fr and to and fr != 'England' and fr != 'Ireland' and fr != 'Scotland':
        print(f' "{r["id"]}": dict(pt="{pt}", line=("{fr}","{to}"), region="{region}"),')
    else:
        print(f' "{r["id"]}": dict(pt="{pt}", region="{region}"),')
