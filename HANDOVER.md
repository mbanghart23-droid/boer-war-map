# Boer War Map — Handover (2026-06-16)

## What this project is
An interactive web map of the **Second Boer War (1899–1902)** — British & Boer troop movements,
unit journeys, QSA medal clasps, and the blockhouse network. It began as **Eastern-Cape-only** and
was deliberately **widened to ALL FRONTS** (Natal, OFS, Transvaal, Western Cape) at the user's request.
Overriding rule throughout: **accuracy / no hallucinations** — every movement is source-cited with a
confidence rating, and source conflicts are *flagged on the row*, never silently merged.

Project dir: `C:\Users\mbang\Downloads\boer-war-eastern-cape\`

## Current state (verify with the snippet below)
- **224 map features · 185 movement rows · 63 unit-columns.** Events by year: 1899: 34 · 1900: 55 ·
  1901: 80 · 1902: 13. Regions: eastern 121, north 48, western 6, logistics 7.
- Live tunnel (ephemeral): **https://jill-task-eternal-nasa.trycloudflare.com** (serve.py :8090 + cloudflared,
  both running in background this session; will die when the session/processes end — restart per below).

## Files
- `data/movements.csv` — the master data. **15 columns:**
  `id,side,force,commander,units,date_start,date_end,event_type,from_place,to_place,action_place,description,confidence,source,note`
  - `side` = British|Boer. `force` = column/commando/division. `units` = regiments, `;`-separated
    (drives the regiment/squadron filter). `event_type` = engagement|raid|capture|move|advance|pursuit|
    drive|deployment|defeat|skirmish|siege|surrender|occupation|garrison|execution|disembark|rail-move…
  - **CSV PITFALL:** any field containing a comma MUST be quoted. The safe way to add many rows is to
    Write them to a fragment file (e.g. `data/_north.csv`) then `cat frag >> data/movements.csv` —
    bash heredocs choke on apostrophes (Cronje's, King's). Always re-check with the verify snippet.
- `build_map.py` — geocodes anchors and writes `web/data/events.geojson`. Key structures:
  - `OVERRIDES` = {placeKey: (lat, lon, conf)} hand-set coords (farms, kopjes, national battle sites).
  - `TOWNS` = {placeKey: "Nominatim query"} geocoded via OSM, cached to `data/gazetteer.json`.
  - `REGT_RULES` / `_canon_regt` / `_subs` / `unit_groups()` — normalize unit names to a canonical
    regiment + squadron, emitted as `groups` = [[regiment, squadron], …] per feature.
  - `category_of()` — buckets event_type → map symbol (battle/movement/garrison/capture/execution/
    logistics). `MAJOR` = {id: label} for big set-piece battles (bigger marker + gold label).
  - `UNIT` = {id: canonical column name} (overrides `force` for the column grouping).
  - `A` = {id: dict(pt=placeKey, line=(from,to), region=eastern|north|western|logistics)} — **every row
    that should appear on the map needs an `A` entry**; `region` controls the default fit (all kinds
    now) and keeps far-flung points from distorting. Rows in `# intentionally omitted` have no `A`.
- `web/index.html` — single-file MapLibre app (raster basemap = Esri World Topo, **no glyphs** → use
  HTML markers or icon symbols, NOT text-field). Layers: `hist-layer` (1900 map img), `qsa-*`,
  `bh-line`/`bh-forts`, `routes`/`moves`/`route-arrows`/`move-arrows`, `pts` (symbol, shaped icons).
  Icons are drawn in-canvas in `drawIcon()` (+`addIcons()`). Filter = `buildFilter`/`applyGrouping`
  (regiment⇄column toggle via MODES)/`visibleIds`/`applyFilter`. Toggles: Regiments, QSA, Blockhouses
  (default on), Legend (contains the 1900-map checkbox+opacity), time slider + Play.
- `web/data/events.geojson` (built), `web/data/qsa.geojson` (5 state/area polygons + 19 battle clasps;
  hand-written, approximate polygons), `web/data/blockhouses.geojson` (10 national lines, hand-written).
- `data/report.md` — the cited narrative + audit-pass log (passes 1–9). Keep it in sync.
- `sources/` — **full texts downloaded for offline mining** (no truncation): `conan_doyle_great_boer_war.txt`
  (ch.32 & 35 = Cape; ch.10/14/21/22 = Stormberg/Colesberg/Brabant), `davitt_boer_fight_for_freedom.txt`
  (week-by-week diary), `gutenberg_15699.txt` (Handbook of the Boer War), `gutenberg_48534.txt`
  (With the Flag to Pretoria vol.1 — Stormberg & Colesberg), and the user's PDF at
  `C:\Users\mbang\Downloads\boerfightforfree00daviuoft.pdf`.

## How to build & serve
```
cd C:\Users\mbang\Downloads\boer-war-eastern-cape
python build_map.py                 # regenerates web/data/events.geojson
python web/serve.py                 # no-cache static server on :8090  (user normally runs this)
./cloudflared.exe tunnel --url http://localhost:8090   # prints a fresh https://…trycloudflare.com
```
Verify after every data change:
```
python -c "import csv,json;from collections import Counter;\
r=list(csv.reader(open('data/movements.csv',encoding='utf-8')));h=len(r[0]);\
print('bad',[x[0] for x in r if len(x)!=h] or 'none');\
ids=[x[0] for x in r[1:]];print('dups',[i for i in set(ids) if ids.count(i)>1] or 'none');\
g=json.load(open('web/data/events.geojson',encoding='utf-8'));print('features',len(g['features']))"
```
Validate inline JS: extract the largest `<script>` block and `node --check` it.

## Hard-won gotchas
- **I cannot screenshot the map.** The connected Chrome automation browser stalls MapLibre's style
  load (WebGL + workers both test fine, zero errors, but `getStyle()` stays undefined) — so verify via
  `node --check`, the CSV/feature counts, and `curl` HTTP 200s, then ask the user to eyeball. The map
  renders fine in the user's own browser.
- **angloboerwar.com is offline** ("Due back Wednesday 17 June") AND Cloudflare-blocks server fetch.
  Its Davitt diary chapters and full unit registry are still pending (task #27). Chrome passes
  Cloudflare but only shows the maintenance notice. archive.org serves Davitt's djvu.txt only via a JS
  reader; `curl` the raw text instead (that's how the sources/ files were obtained).
- Research pattern that worked: spawn **parallel `Agent` subagents** (general-purpose) that each return
  a **JSON array** of rows {date,side,force,commander,units,event_type,from/to/action_place,description,
  confidence,source,region|eastern_cape}. Then dedup vs existing, add anchors (OVERRIDES/TOWNS + `A`),
  append via fragment file, rebuild, verify. (Workflow tool NOT used — no explicit opt-in.)
- Memory dir `C:\Users\mbang\.claude\projects\C--Users-mbang-Downloads\memory\` has relevant notes
  (no-auto-preview, permission-prompts, spell-out-acronyms, wait-for-clear-answer).

## Open threads / next steps
1. **Deepen all-fronts movements** (task #26) — northern fronts are now seeded with the major battles
   but thinner than the Cape; add more dated actions/sub-steps. Sources in `sources/` are barely tapped
   for non-Cape detail.
2. **angloboerwar pull** (task #27, ~17 June) — Davitt diary day-by-day + unit registry (Crewe/Kavanagh/
   Alexander/Wyndham column compositions; more town guards) via Chrome once the site is back.
3. **1900 historical-map overlay is a ROUGH corner-fit** — `web/index.html` `hist` source pins a
   portrait Wikimedia war map (`upload.wikimedia.org/.../e/e6/South_Africa_and_the_Transvaal_War_(1900)_(14786161043).jpg`)
   to a landscape box, so it's stretched/offset. For accuracy, georeference it (warped XYZ tiles via
   David Rumsey/Allmaps/MapWarper) and swap the `image` source for a `raster` tile source. The user is
   aware it's approximate and is deciding whether to pursue accurate tiles.
4. **Eyeball items** (can't self-verify): arrow direction on lines, the anchor/blockhouse icons, QSA
   polygon shapes (approximate), and the 1900-overlay alignment.
5. **QSA polygons & blockhouse lines are hand-traced approximations** — could be replaced with real
   boundary/railway data if precision is wanted.

## Family thread (do not lose — personal to the user)
The user's ancestors were **Kruger veldkornets**. Veldkornet **Jan Kruger** was killed by the 17th
Lancers at **Ruigtevlei** (night attack S of Steynsburg, ~7 Jun 1901; user has seen the headstone).
**Christiaan Kruger** survived (Lion-Cachet once cut a bullet from him). Two Kruger brothers were
exiled to **Bermuda** (Hawkins Island). These are in `movements.csv` (rows ~25–32 area) and `report.md`
§3c, tagged family-record vs documentary. The 17th Lancers have a full traced journey (their column
actions + India→Cape→Diamond Hill→Cape arc).
