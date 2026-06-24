"""
Deeper movement arrows for:
- Natal advance: Dundee → Ladysmith → Tugela → Newcastle → Laing's Nek → Volksrust
- OFS encirclement: Brandwater Basin surrender, Prinsloo trap
- Smuts's Cape raid: Transvaal → eastern Cape → west
- Buller's advance through Natal into Transvaal
- Roberts's main advance: Orange River → Bloemfontein → Pretoria
- Hunter's OFS sweeps
IDs start at 625 (leaving room for gaps2 fragment which starts at 524)
"""
import csv

FIELDS = ['id','side','force','commander','units','date_start','date_end',
          'event_type','from_place','to_place','action_place','description',
          'confidence','source','note']

ROWS = [
    # =====================================================================
    # NATAL ADVANCE — BULLER'S RELIEF OF LADYSMITH AND PUSH NORTH
    # =====================================================================
    ("Buller's Natal Army","General Buller","Royal Dublin Fusiliers;Devon Regiment;Inniskilling Fusiliers",
     "1899-12-15","engagement","Chieveley","Colenso","Colenso",
     "Buller's first attempt to cross the Tugela at Colenso on 15 December 1899 was repulsed with 1,139 British casualties; 10 guns were temporarily lost. It was the worst of Black Week's three defeats.",
     "high","Conan Doyle ch.11","north"),

    ("Buller's 2nd Attempt — Spion Kop","General Buller","Lancashire Fusiliers;Royal Inniskilling Fusiliers;Leinster Regiment",
     "1900-01-19","engagement","Trichard's Drift","Spion Kop","Spion Kop",
     "Buller's second Tugela crossing, flanking westward to Spion Kop, seized the summit on 24 January 1900 but British forces were driven off with 1,500 casualties in one of the bloodiest days of the war.",
     "high","Conan Doyle ch.12","north"),

    ("Buller's 3rd Attempt — Vaal Krantz","General Buller","",
     "1900-02-05","engagement","Trichard's Drift","Vaal Krantz","Vaal Krantz",
     "Buller's third Tugela crossing seized Vaal Krantz on 5 February 1900 but the position proved untenable under Boer fire; another costly withdrawal followed.",
     "high","Conan Doyle ch.12","north"),

    ("Buller's 4th Attempt — Hlangwane and Relief","General Buller","Irish Brigade;Devons;Inniskillings",
     "1900-02-14","engagement","Chieveley","Ladysmith","Ladysmith",
     "Buller's final Tugela crossing seized Hlangwane Hill on 14 February and broke through to relieve Ladysmith on 28 February 1900, ending the 118-day siege.",
     "high","Conan Doyle ch.12; Handbook ch.XI","north"),

    ("Buller's advance — Natal to Transvaal","General Buller","Natal Army",
     "1900-05-01","movement","Ladysmith","Volksrust","Laing's Nek",
     "After the relief of Ladysmith, Buller's Natal Army advanced northward through Dundee and up to Laing's Nek, forcing the pass on 8 June 1900 and entering the Transvaal at Volksrust, linking up with Roberts's main advance.",
     "high","Conan Doyle ch.26; Handbook ch.XIII","north"),

    ("Buller Dundee to Laing's Nek","General Buller","Natal Army",
     "1900-05-15","movement","Dundee","Laing's Nek","Newcastle",
     "Buller's advance from Dundee toward the Transvaal border: through Newcastle, past Majuba Hill and the scene of the 1881 battle, breaching the Drakensberg at Laing's Nek in June 1900.",
     "high","Handbook ch.XIII","north"),

    # =====================================================================
    # NATAL: EARLY BOER ADVANCES AND REVERSES
    # =====================================================================
    ("Boer invasion of Natal","General Joubert","Natal Commandos",
     "1899-10-11","movement","Volksrust","Ladysmith","Dundee",
     "The Boer forces under Joubert invaded Natal on 11 October 1899, advancing through Laing's Nek down to Dundee and Ladysmith; within three weeks they had besieged Ladysmith and cut off Penn Symons's garrison at Talana Hill.",
     "high","Conan Doyle ch.6; Handbook ch.IV","north"),

    ("Boer siege of Ladysmith — investment","General Joubert","Natal Commandos",
     "1899-11-02","engagement","Dundee","Ladysmith","Ladysmith",
     "After Talana Hill and Elandslaagte, Joubert's forces invested Ladysmith from 2 November 1899, beginning the 118-day siege of 13,500 British troops under General White.",
     "high","Conan Doyle ch.7; Handbook ch.V","north"),

    ("Joubert's raid south of Ladysmith","General Joubert","Natal commandos",
     "1899-11-09","engagement","Ladysmith","Colenso","Estcourt",
     "Joubert's commando pushed south of Ladysmith on 9 November 1899, reaching Estcourt before being checked by armoured train resistance; Lord Dundonald's cavalry subsequently pushed them back toward the Tugela.",
     "high","Conan Doyle ch.10","north"),

    # =====================================================================
    # OFS ENCIRCLEMENT — PRINSLOO SURRENDER
    # =====================================================================
    ("Hunter's OFS encirclement","General Hunter","6th Division;7th Division;8th Division",
     "1900-07-01","movement","Bloemfontein","Brandwater Basin","Senekal",
     "General Hunter coordinated five columns converging on the eastern OFS in July 1900, trapping 7,000 Boers (under Prinsloo) in the Brandwater Basin between the Witteberg and Rooiberge ranges.",
     "high","Conan Doyle ch.21; Handbook ch.XV","north"),

    ("Prinsloo's force — trapped in Brandwater Basin","General Prinsloo","OFS commandos",
     "1900-07-16","engagement","Slabbert's Nek","Brandwater Basin","Brandwater Basin",
     "Prinsloo's 4,000-strong OFS force was encircled in the Brandwater Basin; attempts to escape through Naauwpoort Nek on 29 July failed. Prinsloo surrendered 4,314 men on 30 July 1900 — the largest Boer capitulation of the war.",
     "high","Conan Doyle ch.21; Handbook ch.XV","north"),

    # =====================================================================
    # SMUTS'S CAPE RAID
    # =====================================================================
    ("Smuts's Cape Raid — departure","General Jan Smuts","Smuts's commando",
     "1901-09-03","movement","Modderfontein","Clanwilliam","Okiep",
     "General Jan Smuts led ~340 men into the Cape Colony on 3 September 1901, crossing the Orange River near Modderfontein and driving west through Calvinia toward the copper-mining districts of Namaqualand.",
     "high","Conan Doyle ch.36; Hancock 'Smuts'","eastern"),

    ("Smuts's Cape Raid — Elands River Poort","General Jan Smuts","Smuts's commando",
     "1901-09-17","engagement","Calvinia","Elands River Poort","Elands River Poort",
     "At Elands River Poort on 17 September 1901, Smuts's commando ambushed and destroyed a British column of the 17th Lancers, capturing horses, weapons, and supplies that transformed his ragged force into a formidable mounted unit.",
     "high","Conan Doyle ch.36","eastern"),

    ("Smuts's Cape Raid — spread through Namaqualand","General Jan Smuts","Smuts's commando",
     "1901-10-01","movement","Elands River Poort","Okiep","Calvinia",
     "After Elands River Poort, Smuts's commando ranged widely through the western Cape and Namaqualand during late 1901 and early 1902, recruiting Cape rebels and besieging Okiep copper mine before the Peace of Vereeniging ended the war.",
     "high","Conan Doyle ch.36; Hancock","eastern"),

    # =====================================================================
    # ROBERTS'S MAIN ADVANCE — OFS TO PRETORIA
    # =====================================================================
    ("Roberts's advance — Orange River to Paardeberg","Field Marshal Roberts","6th Division;7th Division;Cavalry Division",
     "1900-02-10","movement","Orange River","Paardeberg","Modder River",
     "Roberts outflanked Cronjé's position on the Modder River on 10 February 1900, sending French's cavalry on the famous dash to relieve Kimberley while infantry converged on Cronjé's laager at Paardeberg.",
     "high","Conan Doyle ch.14","north"),

    ("Cronjé's surrender at Paardeberg","General Cronje","OFS and TVL commandos",
     "1900-02-17","engagement","Koedoesberg Drift","Paardeberg","Paardeberg",
     "General Cronjé's 4,000-man force was encircled at Paardeberg and bombarded for 10 days; Cronjé surrendered on 27 February 1900 (Majuba Day), the largest Boer capitulation of the conventional phase.",
     "high","Conan Doyle ch.14; Handbook ch.XII","north"),

    ("Roberts's advance — Paardeberg to Bloemfontein","Field Marshal Roberts","Roberts's army",
     "1900-03-01","movement","Paardeberg","Bloemfontein","Poplar Grove",
     "After Paardeberg, Roberts advanced rapidly east along the Modder River; the Boers offered rearguard resistance at Poplar Grove and Abraham's Kraal but Bloemfontein fell on 13 March 1900.",
     "high","Conan Doyle ch.15","north"),

    ("Roberts's advance — Bloemfontein to Pretoria","Field Marshal Roberts","Roberts's army",
     "1900-05-01","movement","Bloemfontein","Pretoria","Kroonstad",
     "Roberts resumed the advance from Bloemfontein on 1 May 1900: Kroonstad fell on 12 May, Johannesburg on 31 May, and Pretoria on 5 June 1900, effectively ending the conventional phase of the war.",
     "high","Conan Doyle ch.18; Handbook ch.XIV","north"),

    # =====================================================================
    # GUERRILLA PHASE — DE WET'S ESCAPES
    # =====================================================================
    ("De Wet's first escape — Roodeval","Christiaan de Wet","De Wet's commando",
     "1900-06-07","engagement","Roodeval","Heilbron","Roodeval",
     "De Wet raided Roodeval on 7 June 1900, destroying a British supply train and 50,000 infantry rounds; he then evaded converging British columns to escape northward, launching the guerrilla campaign in earnest.",
     "high","Conan Doyle ch.19","north"),

    ("De Wet's first invasion of Cape Colony","Christiaan de Wet","De Wet's commando",
     "1900-12-01","movement","Commando Drift on Vaal River","Aliwal North","Springhaan's Nek",
     "De Wet made his first attempt to invade the Cape Colony in December 1900, crossing the Orange River but being chased back north by Kitchener's columns before reaching the rebel districts.",
     "high","Conan Doyle ch.30","north"),

    ("De Wet's second escape — February 1901","Christiaan de Wet","De Wet's commando",
     "1901-02-01","movement","Springhaan's Nek","Bloemfontein","Philippolis",
     "De Wet eluded a massive British net in February 1901 (Kitchener's 'De Wet hunt'), slipping through Springhaan's Nek with 2,600 men to escape a force of 30,000 British troops.",
     "high","Conan Doyle ch.31","north"),

    # =====================================================================
    # WESTERN FRONT — KIMBERLEY RELIEF
    # =====================================================================
    ("French's cavalry — relief of Kimberley","General French","Cavalry Division",
     "1900-02-13","movement","Modder River","Kimberley","Klip Drift",
     "General French's cavalry division made a famous 35-mile dash from Klip Drift on 13-15 February 1900, brushing aside Boer positions at Abon's Dam and entering Kimberley on 15 February 1900, ending the 124-day siege.",
     "high","Conan Doyle ch.14; Handbook ch.XII","north"),

    # =====================================================================
    # EASTERN TRANSVAAL — FINAL CONVENTIONAL PHASE
    # =====================================================================
    ("Buller's advance — Laing's Nek to Machadodorp","General Buller","Natal Army",
     "1900-06-10","movement","Laing's Nek","Machadodorp","Belfast",
     "After forcing Laing's Nek in June 1900, Buller advanced along the Natal-Pretoria railway through Newcastle, Volksrust, and Standerton toward Machadodorp, converging with Roberts from the west; Buller's forces met Roberts's near Belfast in August 1900.",
     "high","Conan Doyle ch.26; Handbook ch.XIII","north"),

    ("Battle of Bergendal — last conventional engagement","General Buller / Roberts","Rifle Brigade;Inniskilling Fusiliers",
     "1900-08-27","engagement","Belfast","Machadodorp","Bergendal Farm",
     "The Battle of Bergendal (Dalmanutha) on 27 August 1900 was the last pitched battle of the conventional phase; a Zarps (ZAR Police) position was stormed, breaking the final Boer defensive line east of Pretoria.",
     "high","Conan Doyle ch.26","north"),
]

rows = []
START_ID = 625
for i, r in enumerate(ROWS):
    (force, commander, units, date_start, event_type, from_place, to_place, action_place,
     description, confidence, source, region) = r
    rows.append({
        'id': str(START_ID + i),
        'side': 'British' if event_type in ('movement','engagement') and 'De Wet' not in force and 'Boer' not in force and 'Smuts' not in force and 'Joubert' not in force and 'Prinsloo' not in force and 'Cronje' not in force else 'Boer',
        'force': force,
        'commander': commander,
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
        '_from': from_place,
        '_to': to_place,
    })

# Fix sides for Boer rows
for r in rows:
    force = r['force']
    if any(x in force for x in ['De Wet','Joubert','Boer','Prinsloo','Cronje','Smuts']):
        r['side'] = 'Boer'

out = 'data/_movements2_fragment.csv'
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    for r in rows:
        w.writerow({k: r.get(k,'') for k in FIELDS})

print(f'Written {len(rows)} rows, IDs {rows[0]["id"]}-{rows[-1]["id"]}')
print('\nA entries (with lines where from/to both exist):')
for r in rows:
    fr = r['_from']
    to = r['_to']
    pt = r['action_place']
    reg = r['_region']
    if fr and to:
        print(f' "{r["id"]}": dict(pt="{pt}", line=("{fr}","{to}"), region="{reg}"),')
    else:
        print(f' "{r["id"]}": dict(pt="{pt}", region="{reg}"),')
