"""
Movement arrows batch 3:
- Methuen's western advance (Oct-Dec 1899): Orange River → Belmont → Graspan → Modder River → Magersfontein
- French's Kimberley relief dash (Feb 1900)
- Buller's final Natal advance (Feb-Jun 1900)
- Kritzinger's eastern Cape raid (1901)
- Hertzog's western Cape raid (1901)
- Column drives (Kitchener's blocks, 1901-02)
IDs start at 706.
"""
import csv

FIELDS = ['id','side','force','commander','units','date_start','date_end',
          'event_type','from_place','to_place','action_place','description',
          'confidence','source','note']

ROWS = [
    # ── METHUEN'S WESTERN ADVANCE (Nov-Dec 1899) ─────────────────────────────
    dict(id=706, side='British', force="Methuen's advance: Orange River → Belmont",
         commander='Methuen, Lord', units="1st Division; Guards Brigade; 9th Brigade",
         date_start='1899-11-21', date_end='1899-11-23',
         event_type='advance', from_place='Orange River Station', to_place='Belmont',
         action_place='Belmont',
         description="Methuen's 1st Division marched north from Orange River Station and defeated a Boer force at Belmont (23 Nov 1899), the first engagement of his drive to relieve Kimberley.",
         confidence='high', source='Conan Doyle ch.XI', note=''),
    dict(id=707, side='British', force="Methuen's advance: Belmont → Graspan",
         commander='Methuen, Lord', units="1st Division; Naval Brigade",
         date_start='1899-11-25', date_end='1899-11-25',
         event_type='advance', from_place='Belmont', to_place='Graspan',
         action_place='Graspan',
         description="Methuen's force fought the Battle of Graspan (Enslin) on 25 Nov 1899, the Naval Brigade storming the kopjes and clearing the Boer position at a cost of 180 casualties.",
         confidence='high', source='Conan Doyle ch.XI', note=''),
    dict(id=708, side='British', force="Methuen's advance: Graspan → Modder River",
         commander='Methuen, Lord', units="1st Division; Guards Brigade",
         date_start='1899-11-28', date_end='1899-11-28',
         event_type='advance', from_place='Graspan', to_place='Modder River',
         action_place='Modder River',
         description="Battle of Modder River (28 Nov 1899): Methuen's column pinned down all day in open ground by De la Rey and Prinsloo along the Modder and Riet rivers; British eventually crossed after nightfall, Boers withdrew.",
         confidence='high', source='Conan Doyle ch.XI', note=''),
    dict(id=709, side='British', force="Methuen's advance: Modder River → Magersfontein",
         commander='Methuen, Lord', units="1st Division; Highland Brigade",
         date_start='1899-12-11', date_end='1899-12-11',
         event_type='defeat', from_place='Modder River', to_place='Magersfontein',
         action_place='Magersfontein',
         description="Battle of Magersfontein (11 Dec 1899): the Highland Brigade marched in mass formation in darkness and was ambushed at dawn by De la Rey's entrenched Boers; ~900 British casualties including Gen Wauchope killed; advance stalled for 10 weeks.",
         confidence='high', source='Conan Doyle ch.XI', note=''),

    # ── FRENCH'S KIMBERLEY RELIEF DASH (Feb 1900) ───────────────────────────
    dict(id=710, side='British', force="French's cavalry dash to Kimberley",
         commander='French, J.D.P.', units="Cavalry Division: 1st, 2nd, 3rd Cavalry Brigades",
         date_start='1900-02-12', date_end='1900-02-15',
         event_type='advance', from_place='Modder River', to_place='Kimberley',
         action_place='Kimberley',
         description="French's Cavalry Division made a famous 40-mile dash from Klip Drift (12 Feb 1900) through the Boer lines, riding through at the gallop past Abon's Dam and entering Kimberley on 15 Feb 1900, ending the 124-day siege.",
         confidence='high', source='Conan Doyle ch.XIV', note=''),

    # ── BULLER'S FINAL NATAL ADVANCE (Mar-Jun 1900) ──────────────────────────
    dict(id=711, side='British', force="Buller's advance: Ladysmith → Dundee",
         commander='Buller, Sir Redvers', units="Natal Army; 2nd, 4th, 5th Divisions",
         date_start='1900-03-01', date_end='1900-03-15',
         event_type='advance', from_place='Ladysmith', to_place='Dundee',
         action_place='Dundee',
         description="After relieving Ladysmith, Buller's Natal Army advanced north and cleared the Boers from Dundee and the Newcastle district by mid-March 1900, recovering the area lost in the October 1899 invasion.",
         confidence='high', source='Conan Doyle ch.XIX', note=''),
    dict(id=712, side='British', force="Buller's advance: Dundee → Laing's Nek",
         commander='Buller, Sir Redvers', units="Natal Army",
         date_start='1900-05-10', date_end='1900-06-12',
         event_type='advance', from_place='Dundee', to_place="Laing's Nek",
         action_place="Laing's Nek",
         description="Buller forced the Biggarsberg Range (May 1900) and pushed through Botha's Pass and Laing's Nek (12 Jun 1900), finally crossing the border where Colley had failed in 1881 and entering the Transvaal.",
         confidence='high', source='Conan Doyle ch.XIX', note=''),
    dict(id=713, side='British', force="Buller's advance: Laing's Nek → Standerton",
         commander='Buller, Sir Redvers', units="Natal Army",
         date_start='1900-06-12', date_end='1900-07-01',
         event_type='advance', from_place="Laing's Nek", to_place='Standerton',
         action_place='Standerton',
         description="Buller's Natal Army crossed into the Transvaal after Laing's Nek and advanced east to Standerton on the Vaal River, linking up with Roberts's main force coming from Pretoria and completing the conquest of the Transvaal.",
         confidence='high', source='Conan Doyle ch.XIX', note=''),

    # ── KRITZINGER'S EASTERN CAPE RAID (1901) ────────────────────────────────
    dict(id=714, side='Boer', force="Kritzinger's Cape raid — entry",
         commander='Kritzinger, P.H.', units="Kritzinger's commando (~1,000)",
         date_start='1900-12-16', date_end='1901-01-15',
         event_type='raid', from_place='Springfontein', to_place='Middelburg (Cape)',
         action_place='Middelburg (Cape)',
         description="Kritzinger crossed the Orange River near Springfontein in December 1900 with ~1,000 burghers, pushed into the Cape Midlands and operated around Middelburg (Cape), beginning the sustained Boer presence in the eastern Cape Colony.",
         confidence='high', source='angloboerwar.com', note=''),
    dict(id=715, side='Boer', force="Kritzinger's Cape raid — south",
         commander='Kritzinger, P.H.', units="Kritzinger's commando",
         date_start='1901-01-15', date_end='1901-06-01',
         event_type='raid', from_place='Middelburg (Cape)', to_place='Murraysburg',
         action_place='Murraysburg',
         description="Kritzinger's commando pushed deep into the Karoo, reaching as far south as Murraysburg and Richmond districts in early 1901, recruiting Cape rebels and tying down thousands of British troops in fruitless pursuit.",
         confidence='high', source='angloboerwar.com', note=''),

    # ── HERTZOG'S WESTERN CAPE RAID (1901) ───────────────────────────────────
    dict(id=716, side='Boer', force="Hertzog's western Cape raid",
         commander='Hertzog, J.B.M.', units="Hertzog's commando (~1,000)",
         date_start='1901-12-16', date_end='1902-02-28',
         event_type='raid', from_place='Colesberg', to_place='Worcester',
         action_place='Clanwilliam',
         description="Hertzog's audacious raid crossed the Orange River at Christmas 1901 and drove deep into the western Cape as far as the Calvinia and Clanwilliam districts, coming within 150 miles of Cape Town before being turned back.",
         confidence='high', source='angloboerwar.com', note=''),

    # ── KITCHENER'S COLUMN DRIVES (1901-02) ──────────────────────────────────
    dict(id=717, side='British', force="Kitchener's New Model drives — ORC",
         commander='Kitchener, Lord', units="Multiple flying columns (Rimington, Plumer, Bruce Hamilton)",
         date_start='1901-02-01', date_end='1901-08-01',
         event_type='drive', from_place='Bloemfontein', to_place='Kroonstad',
         action_place='Bloemfontein',
         description="Kitchener organised co-ordinated column drives across the Orange River Colony in 1901, using multiple converging columns, blockhouse lines, and drives to sweep De Wet's burghers; costly and wearing for both sides.",
         confidence='high', source='angloboerwar.com', note=''),
    dict(id=718, side='British', force="Kitchener's drives — Transvaal (1901-02)",
         commander='Kitchener, Lord', units="Multiple columns (Walter Kitchener, Smith-Dorrien, Rawlinson)",
         date_start='1901-09-01', date_end='1902-04-01',
         event_type='drive', from_place='Pretoria', to_place='Vereeniging',
         action_place='Pretoria',
         description="Kitchener's systematic drives across the Transvaal 1901-02 used expanding blockhouse networks and timed sweeps to compress Botha's and De la Rey's commandos; each drive yielded captures but Boer mobility made annihilation impossible.",
         confidence='high', source='angloboerwar.com', note=''),

    # ── BOTHA'S NATAL OFFENSIVE (1901) ───────────────────────────────────────
    dict(id=719, side='Boer', force="Botha's Natal offensive",
         commander='Botha, Louis', units="Eastern Transvaal commandos (~2,000)",
         date_start='1901-09-17', date_end='1901-10-10',
         event_type='raid', from_place='Volksrust', to_place='Itala',
         action_place='Itala',
         description="Botha's largest offensive of the guerrilla phase crossed into Natal in September 1901 with ~2,000 burghers, attacking forts at Itala and Fort Prospect (26 Sep 1901) but failing to break through; forced back by Benson's and Gough's columns.",
         confidence='high', source='angloboerwar.com', note=''),

    # ── PEACE NEGOTIATIONS JOURNEY ────────────────────────────────────────────
    dict(id=720, side='Boer', force="Boer delegates to Vereeniging",
         commander='Botha, Louis; De Wet, Christiaan; De la Rey, Koos', units="Boer Peace Delegates",
         date_start='1902-05-15', date_end='1902-05-31',
         event_type='redeployment', from_place='Pretoria', to_place='Vereeniging',
         action_place='Vereeniging',
         description="Boer delegates from all districts assembled at Vereeniging to debate the peace terms; after bitter debate, 54 voted to accept the Treaty of Vereeniging on 31 May 1902, ending nearly three years of war.",
         confidence='high', source='Conan Doyle ch.XXIV', note=''),
]

with open('data/movements.csv', 'a', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    for r in ROWS:
        w.writerow({k: str(r.get(k,'')) for k in FIELDS})

print(f"Appended {len(ROWS)} rows, IDs 706-{705+len(ROWS)}")
print("A dict entries needed:")
for r in ROWS:
    rid = r['id']; pt = r['action_place']; fp = r['from_place']; tp = r['to_place']
    print(f' "{rid}": dict(pt="{pt}", line=("{fp}","{tp}"), region="north"),')
