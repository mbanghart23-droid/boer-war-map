"""
Add new movement rows to fill documented gaps.
Sources: angloboerwar.com, SA Military History Society Journal,
         Wikipedia (Boer War articles), Deneys Reitz 'Commando' (1929),
         Maurice 'History of the War in South Africa' (1906-1910)
"""
import csv
from pathlib import Path

HERE = Path(__file__).parent.parent
CSV_PATH = HERE / "data" / "movements.csv"

rows = list(csv.DictReader(open(CSV_PATH, encoding="utf-8")))
COLS = list(rows[0].keys())
max_id = max(int(r["id"]) for r in rows if r["id"].isdigit())
next_id = max_id + 1

def nid():
    global next_id
    i = next_id; next_id += 1; return str(i)

new_rows = []

def row(side, force, commander, units, date_start, date_end, event_type,
        from_place, to_place, action_place, description, confidence, source, note=""):
    return {
        "id": nid(), "side": side, "force": force, "commander": commander,
        "units": units, "date_start": date_start, "date_end": date_end,
        "event_type": event_type, "from_place": from_place, "to_place": to_place,
        "action_place": action_place, "description": description,
        "confidence": confidence, "source": source, "note": note
    }

# ═══════════════════════════════════════════════════════════════════════════
# HIGHLAND BRIGADE — Cape Town → Modder River (Nov 1899)
# Argylls, Seaforths, HLI, Black Watch traveled by rail Cape Western line
# via De Aar → Orange River Station → Modder River Station.
# Methuen left Cape Town 10 Nov; Highland Brigade arrived ~Nov 22-28.
# Source: britishbattles.com; Maurice Vol 1 Ch XII
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "British",
    "Highland Brigade (1st Division, Methuen's force)",
    "Maj-Gen A.G. Wauchope / Lord Methuen",
    "Black Watch; Seaforth Highlanders; Highland Light Infantry; Argyll and Sutherland Highlanders",
    "1899-11-10", "1899-11-28", "rail_move",
    "Cape Town", "Modder River",
    "Modder River",
    "Highland Brigade traveled by rail via Cape Western mainline: Cape Town → De Aar Junction → Orange River Station, then advanced north to Modder River Station. The Argylls and Seaforths arrived in time for the Battle of Modder River (28 Nov); the full brigade concentrated by ~28 November.",
    "high",
    "britishbattles.com; Maurice 'History of the War in South Africa' Vol 1 Ch XII (HMSO 1906); angloboerwar.com",
    "Rail route: Cape Town → Paarl → Wellington → Worcester → De Aar → Hanover Road → Orange River Station → Modder River Station"
))

# ═══════════════════════════════════════════════════════════════════════════
# CAPE MOUNTED RIFLES — Cape Town → Penhoek (Nov 1899)
# CMR deployed by rail to support Gatacre. Moved to Penhoek (E of Queenstown)
# to watch the passes. Were at Penhoek by Nov 22.
# Source: angloboerwar.com; Gatacre chapter XV angloboerwar.com
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "British",
    "Cape Mounted Rifles",
    "Under Gen. Gatacre (3rd Division)",
    "Cape Mounted Riflemen",
    "1899-11-01", "1899-11-22", "rail_move",
    "Cape Town", "Sterkstroom",
    "Sterkstroom",
    "CMR deployed by rail from Cape Town along the East London main line (via Queenstown) to Sterkstroom, then moved east by road to the Penhoek/Barkly East passes to watch the mountain crossings under Gatacre's 3rd Division.",
    "high",
    "angloboerwar.com; Gatacre chapter XV angloboerwar.com; Battle of Stormberg britishbattles.com",
    "CMR's 235 men with four 2.5-inch guns were ordered to Molteno on night of 9-10 Dec but failed to receive Gatacre's telegram; did not participate in the disastrous Stormberg raid"
))

# ═══════════════════════════════════════════════════════════════════════════
# BRABANT'S HORSE — East London → Penhoek (Nov 1899)
# Raised 5 Nov 1899 at East London; Gatacre sent them to Penhoek with CMR
# to watch the mountain passes. In position by late November.
# Source: angloboerwar.com; Brabant's Horse unit page
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "British",
    "Brabant's Colonial Division",
    "Brig-Gen Edward Brabant",
    "Brabant's Horse (1st corps, forming)",
    "1899-11-05", "1899-11-28", "advance",
    "East London", "Penhoek",
    "Penhoek",
    "Brabant's Horse raised at East London 5 November 1899 and moved inland toward the Eastern Cape passes. Gatacre assigned them to hold Penhoek pass (east of Queenstown) alongside the Cape Mounted Rifles to watch for Boer incursions from the Stormberg district.",
    "medium",
    "angloboerwar.com Brabant's Horse unit page; Gatacre chapter XV angloboerwar.com",
    "Specific towns on the East London → Penhoek road (likely Komani/Queenstown → Cathcart → Penhoek) not documented in surviving records"
))

# ═══════════════════════════════════════════════════════════════════════════
# BRABANT'S HORSE — Penhoek → Dordrecht (Dec 1899 - Jan 1900)
# After the Stormberg debacle (10 Dec), Brabant moved east to Dordrecht
# and the Herschel district as Boer raids intensified.
# Source: Brabant's Horse angloboerwar.com; Dordrecht engagement sources
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "British",
    "Brabant's Colonial Division",
    "Brig-Gen Edward Brabant",
    "Brabant's Horse",
    "1899-12-12", "1900-02-14", "advance",
    "Penhoek", "Dordrecht",
    "Dordrecht",
    "Following the Stormberg disaster (10 Dec 1899), Brabant's Horse moved east from the Penhoek area via Queenstown/Cathcart toward Dordrecht and the Herschel district, responding to Boer raids into the north-eastern Cape. Concentrated at Dordrecht by February 1900 in preparation for the Brabant's Colonial Division advance.",
    "medium",
    "angloboerwar.com Brabant's Horse; Edward Brabant Wikipedia; SA Mil. History Society Journal vol.146",
    "Specific waypoints Dec 1899 - Feb 1900 not documented in surviving unit records"
))

# ═══════════════════════════════════════════════════════════════════════════
# 10th HUSSARS — UK → Cape Colony (Nov-Dec 1899)
# CORRECTION: 10th Hussars were NOT at Ladysmith/Talana Hill.
# They sailed from Liverpool Nov 1899 on SS Ismore/Colombian,
# Ismore wrecked at Paternoster Point 2 Dec; all reached Cape Town by Dec 8.
# Forwarded by rail to Naauwpoort/Colesberg for French's cavalry.
# Source: horsepowermuseum.co.uk; angloboerwar.com
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "British",
    "10th (Prince of Wales's Own) Hussars",
    "Under Gen. John French (Colesberg district)",
    "10th Hussars (A & B Squadrons on Ismore; remainder on Colombian)",
    "1899-11-15", "1899-12-08", "disembark",
    "Liverpool (UK)", "Cape Town",
    "Cape Town",
    "10th Hussars sailed from Liverpool on troopships Ismore and Colombian. SS Ismore wrecked at Paternoster Point (north of Cape Town) 2 December 1899; personnel rescued and eventually re-equipped at Cape Town. SS Colombian arrived safely. Both contingents forwarded by rail to Naauwpoort/Colesberg front by 8-9 December to join French's cavalry operations.",
    "high",
    "horsepowermuseum.co.uk; angloboerwar.com/unit-information/imperial-units/495-10th-prince-of-waless-own-royal-hussars; Maurice Vol 1 Ch XXIV",
    "NOTE: 10th Hussars had NO service in Natal. Any data showing them at Talana Hill or Ladysmith is an error - those regiments were 18th Hussars and 5th Dragoon Guards"
))

new_rows.append(row(
    "British",
    "10th (Prince of Wales's Own) Hussars",
    "Under Gen. John French (Colesberg district)",
    "10th Hussars",
    "1899-12-08", "1899-12-08", "rail_move",
    "Cape Town", "Naauwpoort",
    "Naauwpoort",
    "10th Hussars forwarded from Cape Town by rail to Naauwpoort junction (8-9 December 1899), then to the Colesberg/Arundel front to join French's cavalry operations in the Colesberg district.",
    "high",
    "horsepowermuseum.co.uk; Maurice Vol 1 Ch XXIV; angloboerwar.com",
    ""
))

# ═══════════════════════════════════════════════════════════════════════════
# GORDON HIGHLANDERS — Elandslaagte → Ladysmith siege (Oct-Nov 1899)
# 2nd Gordons: arrived Durban from Bombay ~mid-Oct, railed to Ladysmith,
# fought at Elandslaagte, then besieged Nov 2 1899 - Feb 28 1900.
# Source: angloboerwar.com; gordonhighlanders.com
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "British",
    "2nd Battalion Gordon Highlanders",
    "Under Gen. George White (Ladysmith garrison)",
    "Gordon Highlanders (2nd Battalion)",
    "1899-10-22", "1900-02-28", "garrison",
    "Elandslaagte", "Ladysmith",
    "Ladysmith",
    "After the Battle of Elandslaagte (21 Oct 1899) the 2nd Gordons withdrew into Ladysmith with the rest of White's force. Besieged from 2 November 1899 to 28 February 1900 (118 days). Gordons held the Wagon Hill sector of the perimeter.",
    "high",
    "angloboerwar.com Gordon Highlanders; gordonhighlanders.com Late Victorian Era; britishbattles.com Ladysmith siege",
    "Gordons at Wagon Hill 6 Jan 1900 (critical assault repelled)"
))

new_rows.append(row(
    "British",
    "2nd Battalion Gordon Highlanders",
    "Under Gen. Buller (Natal Field Force)",
    "Gordon Highlanders (2nd Battalion)",
    "1900-03-01", "1900-06-09", "advance",
    "Ladysmith", "Laing's Nek",
    "Newcastle",
    "Following the relief of Ladysmith (28 Feb 1900), the 2nd Gordons recuperated then joined Buller's northward advance through Natal. Advanced via Dundee and Newcastle toward Laing's Nek, forcing the pass 2-9 June 1900 into Transvaal.",
    "high",
    "angloboerwar.com Gordon Highlanders; Maurice Vol 2; gordonhighlanders.com",
    "Buller crossed into Transvaal via Laing's Nek/Majuba area June 1900"
))

new_rows.append(row(
    "British",
    "2nd Battalion Gordon Highlanders",
    "Under Gen. Buller (Natal Field Force)",
    "Gordon Highlanders (2nd Battalion)",
    "1900-06-12", "1900-08-26", "advance",
    "Volksrust", "Belfast",
    "Amersfoort",
    "2nd Gordons advanced with Buller's column from Volksrust through the eastern Transvaal: Amersfoort (Jul 24 engagement, 9 killed/9 wounded), Van Wyk's Vlei (Aug 21 sharp fighting). Reached Belfast/Bergendal area for the last pitched battle of the war.",
    "high",
    "angloboerwar.com Gordon Highlanders; Maurice Vol 2; Battle of Bergendal SA Mil. History Journal vol.124",
    "The 1st Gordons came from the western side; 1st and 2nd Battalions met on a hill near Lydenburg after Bergendal"
))

# ═══════════════════════════════════════════════════════════════════════════
# SOUTH AFRICAN LIGHT HORSE — Natal → Cape Colony (Dec 1900 - Jan 1901)
# After Volksrust they railed: Volksrust → Bloemfontein → Naauwpoort → Cape.
# Operating against Kritzinger in Murraysburg district by 16 Jan 1901.
# Source: angloboerwar.com SALH; Wikipedia SALH; South African Light Horse
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "British",
    "South African Light Horse",
    "Under Gen. Byng (column operations, Cape Colony)",
    "South African Light Horse",
    "1900-12-01", "1901-01-11", "redeployment",
    "Volksrust (Transvaal)", "Murraysburg",
    "Naauwpoort",
    "South African Light Horse railed from Volksrust to Bloemfontein (early December 1900), then via Naauwpoort Junction to the Cape Colony to operate against Kritzinger's commando. In the Murraysburg district by 16 January 1901.",
    "medium",
    "angloboerwar.com SALH; South African Light Horse Wikipedia; SA Mil. History sources",
    "Inspected by Lord Roberts at Pretoria 15 October 1900 before redeployment south"
))

# ═══════════════════════════════════════════════════════════════════════════
# SCHEEPERS COMMANDO — filling movement gaps
# ═══════════════════════════════════════════════════════════════════════════

# Gap 1: Grootvlei (2 Jan) → Aberdeen/Willowmore (16 Jan) — 14 days, short
# Actually let's do the bigger ones:

# Gap: Aberdeen/Willowmore (16 Jan 1901) → south of Graaff-Reinet (27 Feb 1901)
# Scheepers raided northward toward Graaff-Reinet via the Camdeboo mountains
new_rows.append(row(
    "Boer",
    "Scheepers commando",
    "Commandant Gideon Scheepers",
    "Scheepers commando (Cape rebels + OFS burghers)",
    "1901-01-20", "1901-02-25", "raid",
    "Willowmore", "Graaff-Reinet district",
    "Graaff-Reinet",
    "Scheepers moved northeast from the Willowmore/Aberdeen area through the Camdeboo toward the Graaff-Reinet district. Attacked Jansenville (19 Mar) and Aberdeen (Apr). Killed five Georgehan Scouts in the Graaff-Reinet district 15 March 1901.",
    "medium",
    "Scheepers Wikipedia; SA Mil. History Journal vol.185 'Commandant Gideon Scheepers in the Cape Colony'; Graaff-Reinet vol.073",
    "Precise route through Camdeboo mountains not fully documented"
))

# Gap: Jansenville (19 Mar) → Bedford (7 May) — 49 days
# Scheepers ranged north toward Cradock/Bedford area
new_rows.append(row(
    "Boer",
    "Scheepers commando",
    "Commandant Gideon Scheepers",
    "Scheepers commando",
    "1901-03-20", "1901-05-06", "raid",
    "Jansenville", "Bedford district",
    "Pearston",
    "Scheepers ranged north from Jansenville through the Camdeboo highlands toward the Pearston/Bedford/Cradock area over six weeks, harassing loyalists and communications. Raided farms and threatened Pearston before appearing at Bedford 7 May.",
    "medium",
    "Scheepers Wikipedia; SA Mil. History Journal vol.185",
    "Probable route via Rietbron → Pearston → Bedford"
))

# Gap: Rooiklip/Aberdeen (6 Aug) → Prince Albert/capture (10 Oct) — 65 days
# Scheepers moved south toward the Langeberg range and Ladismith; ill on stretcher
new_rows.append(row(
    "Boer",
    "Scheepers commando",
    "Commandant Gideon Scheepers",
    "Scheepers commando",
    "1901-08-07", "1901-10-09", "movement",
    "Aberdeen district", "Ladismith (Langeberg)",
    "Ladismith",
    "Scheepers moved south from the Aberdeen district toward the Langeberg mountains and Ladismith, increasingly incapacitated by appendicitis. His commando 'had got as far south as Montagu' by late September. Scheepers, too ill to ride, commanded from a stretcher. Captured 10-11 October 1901 near Prince Albert Road.",
    "medium",
    "Scheepers Wikipedia; SA Mil. History Journal vol.185; angloboerwar.com",
    "Montagu is in the Breede River valley; Scheepers was captured near Dwyka-Gamka region. Transferred to Matjesfontein (Oct 19), then Graaff-Reinet, executed 18 Jan 1902"
))

# ═══════════════════════════════════════════════════════════════════════════
# KRITZINGER COMMANDO — filling movement gaps
# ═══════════════════════════════════════════════════════════════════════════

# Correction note: Kritzinger captured Dec 16 1901 near Hanover, NOT Jun 1901

# Gap: Murraysburg (15 Jan 1901) → Klipplaat (6 Feb 1901) — 22 days
new_rows.append(row(
    "Boer",
    "Kritzinger commando",
    "Gen. Pieter Hendrik Kritzinger",
    "Kritzinger commando (2nd Cape invasion)",
    "1901-01-16", "1901-02-05", "raid",
    "Murraysburg", "Klipplaat",
    "Jansenville",
    "Kritzinger moved from the Murraysburg area east through Jansenville toward Klipplaat, raiding farms and threatening the Midland railway. Appeared at Klipplaat 6 February 1901.",
    "medium",
    "Kritzinger Wikipedia; angloboerwar.com Kritzinger 'In the Shadow of Death' Ch V; SA Mil. History Journal vol.017",
    ""
))

# Gap: Pearston (3 Mar) → north, retreat to OFS (Apr-Aug 1901)
new_rows.append(row(
    "Boer",
    "Kritzinger commando",
    "Gen. Pieter Hendrik Kritzinger",
    "Kritzinger commando (2nd Cape invasion — withdrawal)",
    "1901-04-09", "1901-04-29", "retreat",
    "Middelburg (Cape)", "Orange River (Bethulie crossing)",
    "Venterstad",
    "After five months in the Cape Colony (Dec 1900 - Apr 1901), Kritzinger's commando withdrew north, crossing the Orange River near Bethulie on or about 29 April 1901. Kritzinger was promoted to General on his return to the Free State.",
    "high",
    "Kritzinger Wikipedia; angloboerwar.com; SA Mil. History Journal vol.017",
    "First invasion ended Apr 1901; third invasion began 19 May 1901 (Norvalspont)"
))

# Third invasion gap: Waterkloof (20 Jun 1901) → 4th invasion (Dec 1901)
# Kritzinger returned north Aug 14 1901 then came back Dec 1901
new_rows.append(row(
    "Boer",
    "Kritzinger commando",
    "Gen. Pieter Hendrik Kritzinger",
    "Kritzinger commando (3rd Cape invasion — withdrawal)",
    "1901-07-22", "1901-08-14", "retreat",
    "Cradock district", "Orange River (OFS border)",
    "Steynsburg",
    "Kritzinger withdrew his third invading force north after operations in the Cradock/Waterkloof area, crossing back into the Orange Free State approximately 14 August 1901.",
    "medium",
    "Kritzinger Wikipedia; SA Mil. History Journal vol.017",
    "Third invasion May 19 - Aug 14 1901; fourth invasion Dec 15-16 1901 (when captured)"
))

# ═══════════════════════════════════════════════════════════════════════════
# SMUTS COMMANDO — Cape Raid: Elands River Poort → western Cape
# After the ambush of 17th Lancers (17 Sep 1901), Smuts moved west
# Source: Deneys Reitz 'Commando' (1929); Jan Smuts in Boer War Wikipedia
# ═══════════════════════════════════════════════════════════════════════════

# Sep-Oct 1901: moving west from Tarkastad area through EC Karoo
new_rows.append(row(
    "Boer",
    "Smuts commando",
    "Gen. Jan Smuts",
    "Smuts commando (Cape raid column)",
    "1901-09-18", "1901-10-31", "raid",
    "Modderfontein (near Tarkastad)", "Murraysburg district",
    "Jansenville",
    "After Elands River Poort (17 Sep 1901), Smuts moved west through the Eastern Cape interior: Bedford, Adelaide, the Zuurberg range, then Jansenville/Camdeboo area, gathering Cape rebels as he went. Deneys Reitz describes marching 'almost due south through the centre of the Colony' toward Murraysburg.",
    "high",
    "Deneys Reitz 'Commando: A Boer Journal of the Boer War' (1929) Chs 22-24; Jan Smuts in Boer War Wikipedia; Taffy Shearing 'General Jan Smuts and His Long Ride' (1994)",
    "Reitz: 'we rode through the Zuurberg passes... then along the upper Fish River valley toward Jansenville'"
))

# Nov-Dec 1901: northwest to Calvinia
new_rows.append(row(
    "Boer",
    "Smuts commando",
    "Gen. Jan Smuts",
    "Smuts commando (Cape raid column)",
    "1901-11-01", "1901-12-31", "raid",
    "Murraysburg district", "Calvinia district",
    "Calvinia",
    "Smuts directed his column northwest from the Murraysburg area through the central Karoo toward Calvinia. By Christmas Day 1901, Deneys Reitz returned from an errand beyond Calvinia and found Smuts established on the Zak River between Kenhardt and Calvinia. Covered approximately 600km across the Karoo.",
    "high",
    "Deneys Reitz 'Commando' Ch 24 (Christmas Day 1901 Zak River reference); Jan Smuts in Boer War Wikipedia",
    "Route: Murraysburg → Sutherland → Calvinia belt. Probable waypoints: Beaufort West district → Loxton → Sutherland → Calvinia"
))

# Jan-Mar 1902: Van Rhynsdorp to coast and northeast to O'kiep
new_rows.append(row(
    "Boer",
    "Smuts commando",
    "Gen. Jan Smuts",
    "Smuts commando / Maritz's forces",
    "1902-01-01", "1902-03-31", "raid",
    "Calvinia district", "Springbok (Namaqualand)",
    "Van Rhynsdorp",
    "Smuts moved from Calvinia northwest into Namaqualand via Van Rhynsdorp (Maritz's force captured this town), along the Olifants River, reaching the sea briefly at the Olifants River mouth before turning northeast toward O'kiep and Springbok copper mining district.",
    "high",
    "Deneys Reitz 'Commando' Chs 24-25; Jan Smuts in Boer War Wikipedia; SA Mil. History Journal vol.165 Relief of O'kiep",
    "Reitz describes reaching the sea near the Olifants River mouth; then northeast to Springbok/Concordia/O'kiep for the final siege"
))

# ═══════════════════════════════════════════════════════════════════════════
# DE LA REY — Moedwil to Yzerspruit (Sep 1901 - Feb 1902)
# Source: De la Rey Wikipedia; chrisash.co.za; SA Mil. History Journal vol.193
# ═══════════════════════════════════════════════════════════════════════════

new_rows.append(row(
    "Boer",
    "De la Rey's commando",
    "Gen. Jacobus H. ('Koos') de la Rey",
    "Western Transvaal commandos under De la Rey",
    "1901-10-01", "1901-10-24", "movement",
    "Moedwil (near Magaliesberg)", "Driefontein (western Transvaal)",
    "Magaliesberg",
    "After the action at Moedwil (30 Sep 1901), De la Rey moved his forces through the Magaliesberg toward Driefontein for another attack on British forces.",
    "medium",
    "De la Rey Wikipedia; SA Mil. History Journal vol.193; warfarehistorynetwork.com",
    ""
))

new_rows.append(row(
    "Boer",
    "De la Rey's commando",
    "Gen. Jacobus H. ('Koos') de la Rey",
    "Western Transvaal commandos under De la Rey",
    "1901-10-24", "1901-10-24", "engagement",
    "Driefontein", "Driefontein",
    "Driefontein",
    "Battle of Driefontein (24 Oct 1901): De la Rey attacked a British camp in the western Transvaal; forced to withdraw after strong resistance. Another action in a series of guerrilla strikes against British columns in the Magaliesberg/western Transvaal theatre.",
    "medium",
    "De la Rey Wikipedia; SA Mil. History Journal vol.193; warfarehistorynetwork.com",
    ""
))

new_rows.append(row(
    "Boer",
    "De la Rey's commando",
    "Gen. Jacobus H. ('Koos') de la Rey",
    "Western Transvaal commandos under De la Rey",
    "1901-12-02", "1901-12-02", "raid",
    "Rustenburg area", "Rustenburg area",
    "Rustenburg",
    "De la Rey attacked a British wagon train east of Rustenburg (2 December 1901), inflicting ~118 casualties and capturing 100+ wagons — a significant logistical coup that resupplied his commando ahead of the Yzerspruit operation.",
    "medium",
    "De la Rey Wikipedia; SA Mil. History Journal vol.193; chrisash.co.za Cyferfontein",
    ""
))

new_rows.append(row(
    "Boer",
    "De la Rey's commando",
    "Gen. Jacobus H. ('Koos') de la Rey",
    "Western Transvaal commandos under De la Rey",
    "1902-01-05", "1902-01-05", "engagement",
    "Cyferfontein (near Magaliesberg)", "Cyferfontein",
    "Cyferfontein",
    "Battle of Cyferfontein (5 Jan 1902): De la Rey ambushed Woolls-Sampson's Imperial Light Horse at Cyferfontein farm, ~30 miles west of Krugersdorp, Magaliesberg. 18 British killed, 32 wounded. De la Rey then withdrew northward.",
    "high",
    "chrisash.co.za 5 Jan 1901 Cyferfontein; De la Rey Wikipedia; SA Mil. History Journal vol.193",
    ""
))

new_rows.append(row(
    "Boer",
    "De la Rey's commando",
    "Gen. Jacobus H. ('Koos') de la Rey",
    "Western Transvaal commandos under De la Rey",
    "1902-01-06", "1902-02-24", "movement",
    "Cyferfontein (Magaliesberg)", "Yzerspruit (near Wolmaransstad)",
    "Wolmaransstad",
    "De la Rey moved his forces southwest from the Magaliesberg to the Wolmaransstad district in preparation for the Yzerspruit operation, building strength and intelligence on Lt-Col von Donop's column.",
    "medium",
    "De la Rey Wikipedia; SA Mil. History Journal vol.193",
    "Followed by Yzerspruit (25 Feb 1902) — capture of von Donop's supply column. Then Tweebosch (7 Mar 1902) — capture of Lord Methuen, De la Rey's greatest tactical triumph."
))

# ═══════════════════════════════════════════════════════════════════════════
# HERTZOG'S COMMANDO — western Cape raid (Nov 1900 - Feb 1901)
# Crossed Orange River Dec 16 1900 with Kritzinger; raided toward Calvinia
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "Boer",
    "Hertzog's commando",
    "Gen. J.B.M. Hertzog",
    "OFS commando column under Hertzog",
    "1900-12-16", "1901-01-20", "advance",
    "Orange River (Odendaalstroom)", "Calvinia district",
    "Calvinia",
    "General Hertzog crossed the Orange River at Odendaalstroom (16 December 1900) alongside Kritzinger, then raided west into the Calvinia/Clanwilliam district. This was the western arm of the dual invasion; Kritzinger went south/east while Hertzog swept west.",
    "high",
    "Hertzog Wikipedia; De la Rey Wikipedia; Kritzinger Wikipedia; angloboerwar.com",
    "Hertzog was back in the OFS by early 1901; the Calvinia district invasion route later used by Smuts Sep 1901-May 1902"
))

# ═══════════════════════════════════════════════════════════════════════════
# OFS COMMANDO — escape from Brandwater Basin → eventual surrender
# Prinsloo's 4,000+ men surrendered Jul 1900; others under De Wet escaped
# ═══════════════════════════════════════════════════════════════════════════
new_rows.append(row(
    "Boer",
    "De Wet's commando",
    "Gen. Christiaan de Wet",
    "De Wet's OFS force (escaped Brandwater Basin)",
    "1900-08-01", "1900-08-07", "retreat",
    "Brandwater Basin (OFS)", "Slabbert's Nek (OFS)",
    "Slabbert's Nek",
    "De Wet escaped the Brandwater Basin encirclement with ~2,600 men through Slabbert's Nek, leaving Prinsloo to surrender with 4,000+ men (30 Jul 1900 - 9 Aug 1900). This escape allowed De Wet to continue guerrilla operations for 2 more years.",
    "high",
    "De Wet 'Three Years War' (1902); Prinsloo surrender Wikipedia; De Wet Wikipedia; Pakenham 'The Boer War'",
    "Prinsloo's surrender was the largest British capture of Boer forces in the war"
))

# ─────────────────────────────────────────────────────────────────────────────
print(f"New rows to add: {len(new_rows)}")
print("IDs:", new_rows[0]["id"], "to", new_rows[-1]["id"])

# Append to CSV
all_rows = rows + new_rows
with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(all_rows)

print(f"Written {len(all_rows)} rows to {CSV_PATH}")
print(f"Previous count: {len(rows)}, Added: {len(new_rows)}")
