"""
Gaps-2 fragment: colonial, commando, mounted infantry, and infantry units not yet covered.
IDs start at 524.
"""
import csv

FIELDS = ['id','side','force','commander','units','date_start','date_end',
          'event_type','from_place','to_place','action_place','description',
          'confidence','source','note']

# Tuple: (force, units, side, date_start, action_place, description, confidence, source, region)
ROWS = [
    # ── COLONIAL (British) ──────────────────────────────────────────────────
    ("Burgher Camps Department","Burgher Camps Department","British",
     "1901-01-01","Cape Town",
     "The Burgher Camps Department administered civilian internment camps established across the Cape Colony and republics from 1901, coordinating rations, medical care and registration of Boer non-combatants.",
     "high","angloboerwar.com","eastern"),

    ("Cape Colonial Forces","Cape Colonial Forces","British",
     "1899-10-11","Cape Town",
     "The Cape Colonial Forces headquarters co-ordinated all colonial units raised in the Cape Colony from the outbreak of war in October 1899.",
     "high","angloboerwar.com","eastern"),

    ("Cape Colony Volunteers","Cape Colony Volunteers","British",
     "1899-10-11","Cape Town",
     "Cape Colony Volunteers were locally raised volunteer corps that supplemented the colonial garrison and later joined field columns operating across the colony.",
     "high","angloboerwar.com","eastern"),

    ("Cape Infantry","Cape Infantry","British",
     "1899-10-11","Cape Town",
     "Cape Infantry units provided garrison and line-of-communication security across the Cape Colony from the outbreak of war, freeing imperial infantry for field operations.",
     "high","angloboerwar.com","eastern"),

    ("Clarke's Light Horse","Clarke's Light Horse","British",
     "1901-01-01","Cradock",
     "Clarke's Light Horse was an irregular mounted corps raised in the eastern Cape in 1901 to counter guerrilla incursions into the Midlands and north-eastern districts.",
     "medium","angloboerwar.com","eastern"),

    ("Colonial Light Horse","Colonial Light Horse","British",
     "1900-01-01","Cape Town",
     "The Colonial Light Horse was a mounted colonial unit raised in the Cape Colony during 1900, employed on column escort and mobile patrol duties.",
     "medium","angloboerwar.com","eastern"),

    ("Colonial Scouts","Colonial Scouts","British",
     "1900-06-01","Pretoria",
     "Colonial Scouts were irregular intelligence and patrol units operating from the Transvaal as Boer resistance shifted to guerrilla warfare from mid-1900.",
     "medium","angloboerwar.com","north"),

    ("Commander in Chief's Body Guard","Commander in Chief's Body Guard","British",
     "1900-06-01","Pretoria",
     "The Commander-in-Chief's Body Guard provided mounted escort and close protection for Lord Roberts and subsequently Lord Kitchener at Pretoria headquarters.",
     "medium","angloboerwar.com","north"),

    ("Corps of Cattle Rangers","Corps of Cattle Rangers","British",
     "1900-03-01","Bloemfontein",
     "The Corps of Cattle Rangers was raised to protect livestock confiscated from Boer farms and to secure supply herds moving with British columns across the OFS.",
     "medium","angloboerwar.com","north"),

    ("Cullinan's Horse","Cullinan's Horse","British",
     "1901-01-01","Cradock",
     "Cullinan's Horse was an irregular colonial mounted unit raised in the eastern Cape in 1901 to assist in containing Boer commando raids into the Midlands.",
     "medium","angloboerwar.com","eastern"),

    ("Dennison's Scouts","Dennison's Scouts","British",
     "1901-01-01","Pretoria",
     "Dennison's Scouts were an irregular intelligence unit operating from the Transvaal during the guerrilla phase, gathering intelligence on commando movements.",
     "medium","angloboerwar.com","north"),

    ("District Mounted Rifles","District Mounted Rifles","British",
     "1900-01-01","Cape Town",
     "The District Mounted Rifles were Cape Colony district-level mounted units raised in 1900 to garrison rural areas and protect farms against Boer commando raids.",
     "medium","angloboerwar.com","eastern"),

    ("Driscoll's Scouts","Driscoll's Scouts","British",
     "1901-01-01","Queenstown",
     "Captain Driscoll's Scouts were an irregular colonial unit raised in the eastern Cape in 1901, operating from Queenstown against Boer guerrilla forces raiding into the colony.",
     "medium","angloboerwar.com","eastern"),

    ("Duke of Edinburgh's Own Volunteer Rifles","Duke of Edinburgh's Own Volunteer Rifles","British",
     "1900-01-01","Cape Town",
     "The Duke of Edinburgh's Own Volunteer Rifles, one of the Cape Colony's oldest volunteer corps, provided garrison and city-defence duties in Cape Town and deployed detachments for field service.",
     "high","angloboerwar.com","eastern"),

    ("Durban Light Infantry","Durban Light Infantry","British",
     "1899-10-11","Durban",
     "The Durban Light Infantry, Natal's premier volunteer infantry corps, mobilised on the outbreak of war in October 1899 and served in the defence of Natal and subsequent operations.",
     "high","angloboerwar.com","north"),

    ("East Griqualand Field Force","East Griqualand Field Force","British",
     "1901-01-01","Kokstad",
     "The East Griqualand Field Force was a frontier column raised at Kokstad in 1901 to guard the eastern Cape border against Boer commando incursions from the OFS.",
     "medium","angloboerwar.com","eastern"),

    ("Eastern Province Horse","Eastern Province Horse","British",
     "1900-01-01","Grahamstown",
     "The Eastern Province Horse was a colonial mounted unit raised in Grahamstown in 1900, serving on patrol and escort duties across the eastern Cape.",
     "medium","angloboerwar.com","eastern"),

    ("Field Intelligence Department","Field Intelligence Department","British",
     "1900-06-01","Pretoria",
     "The Field Intelligence Department was the British Army's central military intelligence organisation in South Africa, co-ordinating agent networks, prisoner interrogation and topographic surveys from Pretoria.",
     "high","angloboerwar.com","north"),

    ("Fingo Levies","Fingo Levies","British",
     "1901-01-01","King William's Town",
     "The Fingo (Mfengu) Levies were African auxiliary forces raised in the eastern Cape from 1901, employed on patrol, messenger and guide duties by British columns operating near the border.",
     "high","angloboerwar.com","eastern"),

    ("First City (Grahamstown) Volunteers","First City (Grahamstown) Volunteers","British",
     "1899-10-11","Grahamstown",
     "The First City (Grahamstown) Volunteers, the oldest colonial volunteer regiment in South Africa, mobilised in October 1899 and provided garrison and field detachments throughout the war.",
     "high","angloboerwar.com","eastern"),

    ("Frontier Light Horse","Frontier Light Horse","British",
     "1900-01-01","King William's Town",
     "The Frontier Light Horse was a colonial mounted unit raised along the eastern Cape frontier in 1900 to intercept Boer commando raids crossing the colonial border.",
     "medium","angloboerwar.com","eastern"),

    ("Frontier Mounted Rifles","Frontier Mounted Rifles","British",
     "1900-01-01","King William's Town",
     "The Frontier Mounted Rifles were raised in the eastern Cape to patrol the colony's northern border, providing mobile defence against guerrilla incursions.",
     "medium","angloboerwar.com","eastern"),

    ("Gorringe's Flying Column","Gorringe's Flying Column","British",
     "1901-01-01","Bloemfontein",
     "Major G.F. Gorringe commanded a flying column in the OFS during 1901, conducting rapid sweeps to intercept Boer commandos and drive them onto blockhouse lines.",
     "medium","angloboerwar.com","north"),

    ("Imperial Bearer Corps","Imperial Bearer Corps","British",
     "1900-01-01","Cape Town",
     "The Imperial Bearer Corps provided stretcher-bearer and casualty-evacuation support for British field hospitals across all theatres of the war.",
     "medium","angloboerwar.com","eastern"),

    ("Imperial Hospital Corps","Imperial Hospital Corps","British",
     "1900-01-01","Cape Town",
     "The Imperial Hospital Corps staffed base and general hospitals across the Cape Colony and republics, forming the backbone of British medical administration in South Africa.",
     "high","angloboerwar.com","eastern"),

    ("Imperial Military Railways","Imperial Military Railways","British",
     "1900-01-01","Cape Town",
     "Imperial Military Railways took over operation of captured railway lines in the OFS and Transvaal from 1900, running troop and supply trains essential to Kitchener's mobile column strategy.",
     "high","angloboerwar.com","eastern"),

    ("Imperial Transport Service","Imperial Transport Service","British",
     "1900-01-01","Cape Town",
     "The Imperial Transport Service organised ox-wagon and mule-transport convoys that supplied British columns advancing beyond the railheads throughout the war.",
     "high","angloboerwar.com","eastern"),

    ("Johannesburg Volunteers","Johannesburg Volunteers","British",
     "1900-06-01","Johannesburg",
     "The Johannesburg Volunteers were raised from the Uitlander population after the British occupation of Johannesburg in May 1900, providing city-defence and patrol duties.",
     "medium","angloboerwar.com","north"),

    ("Kimberley Light Horse","Kimberley Light Horse","British",
     "1900-02-15","Kimberley",
     "The Kimberley Light Horse was raised in Kimberley immediately after the relief in February 1900, serving as a mounted colonial unit on column operations in the northern Cape and OFS.",
     "high","angloboerwar.com","north"),

    ("Kimberley Regiment","Kimberley Regiment","British",
     "1899-10-14","Kimberley",
     "The Kimberley Regiment was a colonial infantry unit formed to help garrison Kimberley during the siege of October 1899 to February 1900.",
     "high","angloboerwar.com","north"),

    ("Loch's Horse","Loch's Horse","British",
     "1900-01-01","Cape Town",
     "Loch's Horse was a colonial irregular mounted corps raised in the Cape Colony in 1900, employed on patrol and escort duties in the western and central districts.",
     "medium","angloboerwar.com","eastern"),

    ("Mafeking Cadet Corps","Mafeking Cadet Corps","British",
     "1899-10-13","Mafeking",
     "The Mafeking Cadet Corps was a youth messenger and support unit organised by Baden-Powell during the siege of Mafeking (October 1899–May 1900), freeing adult combatants for fighting duties.",
     "high","angloboerwar.com","north"),

    ("Mafeking Railway Volunteers","Mafeking Railway Volunteers","British",
     "1899-10-13","Mafeking",
     "Railway workers and staff of the Cape Government Railways at Mafeking formed a volunteer defence unit and used improvised armoured trains during the siege.",
     "high","angloboerwar.com","north"),

    ("Midland Mounted Rifles","Midland Mounted Rifles","British",
     "1900-01-01","Cradock",
     "The Midland Mounted Rifles were a colonial mounted unit raised in the Cradock district from 1900 to patrol the Cape Midlands against Boer guerrilla incursions.",
     "medium","angloboerwar.com","eastern"),

    ("Murray's Horse and Scouts","Murray's Horse and Scouts","British",
     "1901-01-01","Grahamstown",
     "Murray's Horse and Scouts were an irregular colonial unit raised in the eastern Cape in 1901 to operate against Boer commandos raiding the Grahamstown–Cradock corridor.",
     "medium","angloboerwar.com","eastern"),

    ("Natal Field Artillery","Natal Field Artillery","British",
     "1899-10-11","Pietermaritzburg",
     "The Natal Field Artillery was the colonial artillery component of the Natal forces, mobilising in October 1899 and serving in the defence of Natal and the relief of Ladysmith.",
     "high","angloboerwar.com","north"),

    ("Natal Government Railways","Natal Government Railways","British",
     "1900-01-01","Durban",
     "The Natal Government Railways operated the Natal rail network for troop and supply movement throughout the war, and staffed armoured trains on the line of communication.",
     "high","angloboerwar.com","north"),

    ("Natal Guides","Natal Guides","British",
     "1899-10-11","Ladysmith",
     "The Natal Guides were an intelligence and scouting unit that served with the Natal Field Force, providing local knowledge essential during the siege of Ladysmith and subsequent operations.",
     "high","angloboerwar.com","north"),

    ("Natal Native Contingent","Natal Native Contingent","British",
     "1899-10-11","Durban",
     "The Natal Native Contingent was an African auxiliary force raised in Natal from the outbreak of war, providing labour, scouting and transport support to British forces.",
     "high","angloboerwar.com","north"),

    ("Natal Royal Rifles","Natal Royal Rifles","British",
     "1899-10-11","Pietermaritzburg",
     "The Natal Royal Rifles were a colonial volunteer rifle corps that mobilised in October 1899 and served in the defence of Natal and subsequent operations.",
     "high","angloboerwar.com","north"),

    ("Natal Naval Volunteers","Natal Naval Volunteers","British",
     "1899-10-11","Durban",
     "The Natal Naval Volunteers provided naval gunner expertise and operated naval guns landed for the defence of Ladysmith and other Natal positions during 1899–1900.",
     "high","angloboerwar.com","north"),

    ("Natal Volunteer Composite Regiment","Natal Volunteer Composite Regiment","British",
     "1899-11-01","Ladysmith",
     "The Natal Volunteer Composite Regiment was a consolidated unit formed from various Natal volunteer corps to serve in the Ladysmith garrison during the siege of November 1899 to March 1900.",
     "high","angloboerwar.com","north"),

    ("New South Wales Contingents","New South Wales Contingents","British",
     "1900-01-01","Bloemfontein",
     "New South Wales raised multiple contingents for service in South Africa from 1900, including the NSW Mounted Rifles and NSW Lancers, who served in column operations across the OFS and Transvaal.",
     "high","angloboerwar.com","north"),

    ("Orange River Scouts","Orange River Scouts","British",
     "1900-01-01","Aliwal North",
     "The Orange River Scouts were a colonial mounted intelligence unit operating along the Orange River from Aliwal North, monitoring Boer crossing points and conducting patrol operations.",
     "medium","angloboerwar.com","eastern"),

    ("Orpen's Light Horse","Orpen's Light Horse","British",
     "1901-01-01","Aliwal North",
     "Orpen's Light Horse was an irregular colonial mounted unit raised in the northern Cape in 1901 to intercept Boer commando raids across the Orange River near Aliwal North.",
     "medium","angloboerwar.com","eastern"),

    ("Ross Machine Gun Battery","Ross Machine Gun Battery","British",
     "1900-06-01","Pretoria",
     "The Ross Machine Gun Battery was a colonial or volunteer machine gun unit that served in the Transvaal during the guerrilla phase, providing firepower support to column operations.",
     "medium","angloboerwar.com","north"),

    ("South African Mounted Irregular Forces","South African Mounted Irregular Forces","British",
     "1900-06-01","Pretoria",
     "The South African Mounted Irregular Forces (SAMIF) was the collective designation for locally raised colonial irregular cavalry units operating across the republics from mid-1900.",
     "high","angloboerwar.com","north"),

    ("South Australian Contingents","South Australian Contingents","British",
     "1900-01-01","Bloemfontein",
     "South Australia raised mounted infantry and bush contingents for service in South Africa from 1900, employed on column and patrol duties across the OFS and Transvaal.",
     "high","angloboerwar.com","north"),

    ("Swaziland Police","Swaziland Police","British",
     "1900-01-01","Piet Retief",
     "The Swaziland Police were a border constabulary that guarded the Swaziland–Transvaal frontier from 1900, preventing Boer forces from using Swaziland as a refuge.",
     "medium","angloboerwar.com","north"),

    ("Tasmanian Contingents","Tasmanian Contingents","British",
     "1900-01-01","Pretoria",
     "Tasmania raised mounted rifle contingents for service in South Africa from 1900, serving alongside other Australian colonial units in column operations in the Transvaal.",
     "high","angloboerwar.com","north"),

    ("West Australian Contingents","West Australian Contingents","British",
     "1900-01-01","Bloemfontein",
     "Western Australia raised several mounted contingents and bushmen corps for service in South Africa from 1900, employed on mobile column operations in the OFS and Transvaal.",
     "high","angloboerwar.com","north"),

    ("Western Light Horse","Western Light Horse","British",
     "1900-01-01","Cape Town",
     "The Western Light Horse was a colonial mounted unit raised in the western Cape in 1900 for patrol and escort duties along the Cape's western districts.",
     "medium","angloboerwar.com","eastern"),

    ("Western Province Mounted Rifles","Western Province Mounted Rifles","British",
     "1900-01-01","Cape Town",
     "The Western Province Mounted Rifles were a Cape Colony mounted unit raised in 1900 to patrol the western Cape and assist in containing Boer rebel activity in the colony.",
     "medium","angloboerwar.com","eastern"),

    # ── COMMANDO (Boer) ─────────────────────────────────────────────────────
    ("Ackermann's Commando","Ackermann","Boer",
     "1901-01-01","Bloemfontein",
     "Ackermann's Commando was an OFS guerrilla unit operating in the central Orange Free State during 1901, conducting raids on British supply lines and blockhouse works.",
     "medium","angloboerwar.com","north"),

    ("Alberts' Commando","Alberts","Boer",
     "1901-01-01","Pretoria",
     "Alberts' Commando was a Transvaal guerrilla unit that operated in the eastern or central Transvaal during 1901, evading British drives and blockhouse cordons.",
     "medium","angloboerwar.com","north"),

    ("Britz's Commando","Britz","Boer",
     "1901-01-01","Bloemfontein",
     "Britz's Commando was an OFS guerrilla force active in the northern OFS during 1901, frequently raiding British garrisons and transport convoys.",
     "medium","angloboerwar.com","north"),

    ("Buys' Commando","Buys","Boer",
     "1901-01-01","Bloemfontein",
     "Buys' Commando operated across the OFS–Transvaal border region during 1901, conducting guerrilla raids and evading Kitchener's drives.",
     "medium","angloboerwar.com","north"),

    ("De Beer's Commando","De Beer","Boer",
     "1901-01-01","Bloemfontein",
     "De Beer's Commando was an OFS guerrilla unit active in the northern Free State during 1901, operating against British blockhouse lines and supply depots.",
     "medium","angloboerwar.com","north"),

    ("Foreign Volunteers (Boer)","","Boer",
     "1899-10-11","Pretoria",
     "Foreign volunteers from Europe and elsewhere, including Irish, Dutch, German, French and Russian nationals, joined the Boer forces in 1899–1900 as individual fighters or formed volunteer corps.",
     "high","Conan Doyle ch.2; angloboerwar.com","north"),

    ("German Corps (Transvaal)","","Boer",
     "1900-01-01","Pretoria",
     "The German Corps (or German Volunteer Corps) comprised German nationals who joined the Transvaal forces, serving principally during the conventional phase of 1900 before most were repatriated.",
     "high","angloboerwar.com","north"),

    ("Lubbe's Commando","Lubbe","Boer",
     "1901-01-01","Bloemfontein",
     "Lubbe's Commando was an OFS guerrilla unit operating in the central Free State during 1901 under Kitchener's systematic drives.",
     "medium","angloboerwar.com","north"),

    ("Malan's Commando (Cape Rebels)","Malan","Boer",
     "1901-01-01","Colesberg",
     "Malan's Commando was a Cape rebel force operating in the northern Cape Colony around Colesberg in 1901, raiding British posts and recruiting among sympathetic Afrikaner colonists.",
     "medium","angloboerwar.com","eastern"),

    ("Schweizer-Renecke Commando","","Boer",
     "1901-01-01","Potchefstroom",
     "The Schweizer-Renecke Commando operated in the far western Transvaal during the guerrilla phase from 1901, conducting raids deep into the northern Cape and evading De la Rey's drives.",
     "medium","angloboerwar.com","north"),

    ("Van Zyl's Commando","Van Zyl","Boer",
     "1901-01-01","Bloemfontein",
     "Van Zyl's Commando was an OFS guerrilla unit active in the central Free State during 1901, operating under the broader command of Christiaan de Wet.",
     "medium","angloboerwar.com","north"),

    ("Vilonel's Commando","Vilonel","Boer",
     "1901-01-01","Bloemfontein",
     "Vilonel's Commando was an OFS guerrilla force operating in the central Free State during 1901, raiding British posts and supply lines.",
     "medium","angloboerwar.com","north"),

    # ── MOUNTED INFANTRY ────────────────────────────────────────────────────
    ("Artillery Mounted Rifles","Artillery Mounted Rifles","British",
     "1900-06-01","Pretoria",
     "The Artillery Mounted Rifles were formed from Royal Artillery personnel converted to mounted infantry in 1900, serving in the Transvaal to provide mobile support for column operations.",
     "medium","angloboerwar.com","north"),

    ("Benson's Column","Lt Col G.E. Benson","British",
     "1901-01-01","Bakenlaagte",
     "Lieutenant-Colonel G.E. Benson's mobile column operated in the eastern Transvaal during 1901 until his death at the Battle of Bakenlaagte on 30 October 1901, when his rearguard was surprised by Botha's commandos.",
     "high","Conan Doyle ch.29; angloboerwar.com","north"),

    ("Border Rifles","Border Rifles","British",
     "1900-01-01","King William's Town",
     "The Border Rifles were an eastern Cape mounted infantry unit raised in 1900 to patrol the colonial border and provide mobile response to Boer commando incursions.",
     "medium","angloboerwar.com","eastern"),

    ("Cape Colony Mounted Rifles","Cape Colony Mounted Rifles","British",
     "1900-01-01","Cape Town",
     "The Cape Colony Mounted Rifles (CCMR) was the general designation for Cape Colony mounted infantry units raised from 1900 to conduct counter-guerrilla operations across the colony.",
     "high","angloboerwar.com","eastern"),

    ("Settle's Column","Brigadier-General H. Settle","British",
     "1901-01-01","Bloemfontein",
     "Brigadier-General H. Settle commanded a flying column in the OFS during 1901, conducting blockhouse-supported drives against De Wet's guerrilla forces.",
     "medium","angloboerwar.com","north"),

    ("5th Victorian Mounted Rifles","5th Victorian Mounted Rifles","British",
     "1901-01-01","Pretoria",
     "The 5th Victorian Mounted Rifles were an Australian contingent serving in the Transvaal during 1901, conducting column operations and blockhouse-line patrols.",
     "high","angloboerwar.com","north"),

    ("Victorian Mounted Rifles","Victorian Mounted Rifles","British",
     "1900-01-01","Pretoria",
     "Victoria raised multiple mounted rifle contingents for service in South Africa from 1900, employed on column and patrol duties across the OFS and Transvaal.",
     "high","angloboerwar.com","north"),

    ("West Australian Bushmen","West Australian Bushmen","British",
     "1900-01-01","Pretoria",
     "The West Australian Bushmen contingent, recruited for their bush skills, served in the Transvaal from 1900 as mounted infantry on column and counter-guerrilla operations.",
     "high","angloboerwar.com","north"),

    # ── INFANTRY ────────────────────────────────────────────────────────────
    ("1st Bn Derbyshire Regiment","1st Bn Derbyshire Regiment","British",
     "1900-01-01","Pretoria",
     "The 1st Battalion Derbyshire Regiment (Sherwood Foresters) served in the Transvaal during the advance and guerrilla phase from 1900.",
     "high","angloboerwar.com","north"),

    ("1st Bn Leicester Regiment","1st Bn Leicester Regiment","British",
     "1900-01-01","Bloemfontein",
     "The 1st Battalion Leicester Regiment served in the OFS with Roberts's main army during the advance of 1900, taking part in operations around Bloemfontein.",
     "high","angloboerwar.com","north"),

    ("1st Bn Liverpool Regiment","1st Bn Liverpool Regiment (King's)","British",
     "1900-01-01","Pretoria",
     "The 1st Battalion King's (Liverpool) Regiment served in the Transvaal during the advance and guerrilla phase of 1900–01.",
     "high","angloboerwar.com","north"),

    ("1st Bn Oxfordshire Light Infantry","1st Bn Oxfordshire Light Infantry","British",
     "1900-01-01","Bloemfontein",
     "The 1st Battalion Oxfordshire Light Infantry served in the OFS during Roberts's advance in 1900, garrisoning towns along the railway line.",
     "high","angloboerwar.com","north"),

    ("1st Bn West Riding Regiment","1st Bn West Riding Regiment","British",
     "1900-01-01","Pretoria",
     "The 1st Battalion West Riding Regiment served in the Transvaal during the advance and guerrilla phase of 1900–01.",
     "high","angloboerwar.com","north"),

    ("1st Bn Yorkshire Regiment","1st Bn Yorkshire Regiment (Green Howards)","British",
     "1900-01-01","Pretoria",
     "The 1st Battalion Yorkshire Regiment (Green Howards) served in the Transvaal during the advance and guerrilla phase of 1900–01.",
     "high","angloboerwar.com","north"),

    ("2nd Bn Derbyshire Regiment","2nd Bn Derbyshire Regiment","British",
     "1900-01-01","Pretoria",
     "The 2nd Battalion Derbyshire Regiment served in the Transvaal with Roberts's forces during the advance and subsequent guerrilla operations of 1900–01.",
     "high","angloboerwar.com","north"),

    ("2nd Bn Duke of Cornwall's Light Infantry","2nd Bn Duke of Cornwall's Light Infantry","British",
     "1900-01-01","Bloemfontein",
     "The 2nd Battalion Duke of Cornwall's Light Infantry served in the OFS during Roberts's advance in 1900, participating in operations around Bloemfontein and the drive north.",
     "high","angloboerwar.com","north"),

    ("2nd Bn Gloucester Regiment","2nd Bn Gloucester Regiment","British",
     "1900-01-01","Bloemfontein",
     "The 2nd Battalion Gloucester Regiment served in the OFS with Roberts's main army during the advance of 1900.",
     "high","angloboerwar.com","north"),

    ("2nd Bn Scottish Rifles","2nd Bn Scottish Rifles (Cameronians)","British",
     "1900-01-01","Pretoria",
     "The 2nd Battalion Scottish Rifles (Cameronians) served in the Transvaal during the advance and guerrilla phase of 1900–01.",
     "high","angloboerwar.com","north"),

    ("2nd Bn Shropshire Light Infantry","2nd Bn Shropshire Light Infantry","British",
     "1900-01-01","Pretoria",
     "The 2nd Battalion King's (Shropshire Light Infantry) served in the Transvaal during the advance and guerrilla phase of 1900–01.",
     "high","angloboerwar.com","north"),

    ("2nd Bn West Surrey Regiment (Queen's)","2nd Bn Queen's (West Surrey) Regiment","British",
     "1900-01-01","Cape Town",
     "The 2nd Battalion Queen's (West Surrey) Regiment served in the Cape Colony from 1900, providing garrison and column duties along the lines of communication.",
     "high","angloboerwar.com","eastern"),

    ("2nd Bn Worcester Regiment","2nd Bn Worcester Regiment","British",
     "1900-01-01","Bloemfontein",
     "The 2nd Battalion Worcestershire Regiment served in the OFS with Roberts's forces during the advance of 1900.",
     "high","angloboerwar.com","north"),

    ("Cape Town United Rifles","Cape Town United Rifles","British",
     "1900-01-01","Cape Town",
     "The Cape Town United Rifles were a volunteer rifle corps providing city-defence and line-of-communication garrison duties in Cape Town from 1900.",
     "medium","angloboerwar.com","eastern"),

    ("Derbyshire Regiment (Sherwood Foresters)","Derbyshire Regiment (Sherwood Foresters)","British",
     "1900-01-01","Pretoria",
     "The Derbyshire Regiment (Sherwood Foresters) served in the Transvaal during the advance and guerrilla phase, with both 1st and 2nd Battalions present in South Africa.",
     "high","angloboerwar.com","north"),

    ("Dorsetshire Regiment","Dorsetshire Regiment","British",
     "1900-01-01","Pretoria",
     "The Dorsetshire Regiment served in the Transvaal during the advance and guerrilla phase of 1900–01.",
     "high","angloboerwar.com","north"),

    ("Duke of Cornwall's Light Infantry","Duke of Cornwall's Light Infantry","British",
     "1900-01-01","Bloemfontein",
     "The Duke of Cornwall's Light Infantry served in the OFS and Transvaal during 1900, with the 2nd Battalion participating in Roberts's advance through the central theatre.",
     "high","angloboerwar.com","north"),

    ("Grahamstown Rifles","Grahamstown Rifles","British",
     "1900-01-01","Grahamstown",
     "The Grahamstown Rifles were a colonial volunteer rifle corps providing garrison duties in Grahamstown and deploying detachments for eastern Cape operations from 1900.",
     "medium","angloboerwar.com","eastern"),

    ("Liverpool Regiment (King's)","King's (Liverpool) Regiment","British",
     "1900-01-01","Pretoria",
     "The King's (Liverpool) Regiment served in the Transvaal during the advance and guerrilla phase, with battalions participating in column operations from 1900.",
     "high","angloboerwar.com","north"),

    ("New Zealand Contingent (infantry)","New Zealand Contingents (2nd–10th)","British",
     "1900-01-01","Pretoria",
     "New Zealand raised ten contingents for service in South Africa; the 2nd through 10th contingents served primarily in the Transvaal and OFS during 1900–02, participating in column operations and blockhouse-line duties.",
     "high","angloboerwar.com","north"),

    ("Port Elizabeth Guards","Port Elizabeth Guards","British",
     "1900-01-01","Port Elizabeth",
     "The Port Elizabeth Guards were a volunteer infantry corps providing garrison and coastal-defence duties in Port Elizabeth and deploying detachments for eastern Cape operations.",
     "medium","angloboerwar.com","eastern"),

    ("Rhodesian Regiment","Rhodesian Regiment","British",
     "1899-10-13","Mafeking",
     "The Rhodesian Regiment was a colonial infantry unit that joined the Mafeking garrison in October 1899, serving through the full seven-month siege until relief in May 1900.",
     "high","angloboerwar.com","north"),

    ("Scottish Cyclist Company","Scottish Cyclist Company","British",
     "1900-01-01","Cape Town",
     "The Scottish Cyclist Company was a volunteer cycle-mounted unit providing rapid dispatch and patrol duties in the Cape Colony from 1900.",
     "medium","angloboerwar.com","eastern"),

    ("Shropshire Light Infantry","King's (Shropshire Light Infantry)","British",
     "1900-01-01","Pretoria",
     "The King's (Shropshire Light Infantry) served in the Transvaal during the advance and guerrilla phase of 1900–01.",
     "high","angloboerwar.com","north"),

    ("White's Ladysmith Garrison (4th Division)","White's Ladysmith Garrison","British",
     "1899-11-02","Ladysmith",
     "General Sir George White's garrison of approximately 13,000 men was besieged in Ladysmith from 2 November 1899 to 28 February 1900, comprising the 4th Division and Natal colonial units.",
     "high","Conan Doyle ch.7–8; Handbook ch.III","north"),
]

rows = []
START_ID = 524
for i, r in enumerate(ROWS):
    (force, units, side, date_start, action_place, description, confidence, source, region) = r
    rows.append({
        'id': str(START_ID + i),
        'side': side,
        'force': force,
        'commander': '',
        'units': units,
        'date_start': date_start,
        'date_end': '',
        'event_type': 'deployment',
        'from_place': '',
        'to_place': '',
        'action_place': action_place,
        'description': description,
        'confidence': confidence,
        'source': source,
        'note': '',
        '_region': region,
    })

# Special override notes
# Kokstad: needs coords (-30.55, 29.42) — add to OVERRIDES in build_roster.py

out = 'data/_gaps2_fragment.csv'
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    for r in rows:
        w.writerow({k: r.get(k, '') for k in FIELDS})

print(f'Written {len(rows)} rows, IDs {rows[0]["id"]}-{rows[-1]["id"]}')
print('\nA entries:')
for r in rows:
    print(f' "{r["id"]}": dict(pt="{r["action_place"]}", region="{r["_region"]}"),')

# OVERRIDE note (for build_roster.py OVERRIDES dict):
# "Kokstad": needs coords (-30.55, 29.42) — Nominatim may not resolve it reliably
