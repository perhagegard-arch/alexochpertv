# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Projekt: Fikarums-TV (Smart Dashboard)

En modulär dashboard-plattform för en fikarums-TV som körs på en Raspberry Pi i Kiosk-läge. Appen fungerar som en plattform baserad på "Widgets" (Kort) som dynamiskt växlar innehåll.

## Arkitektur

Systemet består av fyra delar:

1. **Frontend (HTML/JS/CSS):** Skärmen är indelad i fem zoner: en stor mittzon som roterar mellan aktiva widgets (cross-fade, "hjälte"-läge) och fyra fasta zoner runtom (vänster topp/botten, höger topp/botten) som var och en alltid visar en admin-vald widget i ett kompakt läge.
2. **Regelmotor (Backend/Python):** Avgör vilka kort som är aktuella baserat på tid, datum och prioritet (`backend/rules.py`, ej implementerad än — utöver det enkla 5-dagarsfönstret för födelsedagar, se nedan).
3. **Datalager (Backend/Python):** Hämtar data från Google Sheets och serverar till frontenden via ett API (`backend/sheets.py`, ej implementerad än). Tills den finns klistras innehåll in manuellt via admin-panelen och sparas i `data/state.json`.
4. **Widgets:** Varje widget är en fristående modul/klass. Den befintliga citat-appen kapslas in som `QuoteWidget` — den ska inte skrivas om, bara lyftas in.
5. **Admin-panel (`/admin`):** Per kan logga in med ett delat lösenord, välja vilka widgets som ingår i mitt-rotationen, välja vilken widget varje fast zon visar, och redigera innehåll för widgets som har det (just nu bara födelsedagar). Allt sparas i `data/state.json` och respekteras av `backend/api.py`.

## Filstruktur

```
backend/
  main.py              # Flask-app, startar servern (port 8080), registrerar api + admin
  api.py               # GET /api/card (mitt-rotation) + GET /api/zone/<id> (fast zon) — delar _build_card
  admin.py             # Blueprint: /admin (sida) + /admin/api/* (login, widgets, zones, birthdays)
  auth.py              # login_required-decorator + lösenordskontroll (session-baserad)
  store.py             # JsonStore — läser/skriver data/state.json
  widgets_registry.py  # Delad källa: WIDGET_ORDER/WIDGETS samt ZONES/ZONE_IDS (de fyra fasta zonerna)
  birthdays.py          # parse_birthdays(), upcoming_within(), birthdays_today() — ren parsing-logik
  config.py            # Läser .env: QUOTES_API_URL, DISPLAY_SECONDS, BACKGROUND_IMAGES, ADMIN_PASSWORD, SECRET_KEY
  rules.py             # (stub) Regelmotor — generell regelmotor ej byggd än
  sheets.py            # (stub) Google Sheets-integration
  providers/
    quotes.py          # QuoteProvider — anropar citattjänsten
    weather.py         # WeatherProvider — Open-Meteo API
    birthdays.py       # BirthdayProvider — läser store, returnerar upcoming inom 5 dagar
  cards/
    quote_card.py      # Bygger card-JSON från provider-data
    weather_card.py
    birthday_card.py   # Returnerar alltid kortet — content.people kan vara tom lista

data/
  state.json           # Körtids-state (widget-toggles, zon-tilldelningar, inklistrad födelsedagstext), gitignored

frontend/
  index.html           # 5-zon-grid: zone-center (cross-fade, hjälte-läge) + 4 .zone-divs (kompakt läge)
  style.css            # CSS-grid-layout + .compact-varianter av varje kortklass
  app.js               # showNext() pollar /api/card (mitten), showZone() per fast zon pollar /api/zone/<id>
  images/              # Bakgrundsbilder (.jpg) — listas i .env
  widgets/
    QuoteWidget.js     # render<Namn>Card(content, mode) — mode: "hero" | "compact"
    WeatherWidget.js
    BirthdayWidget.js  # Visar reservtext i compact-läge om content.people är tom
  admin.html            # Login + widget-toggles (mitten) + zon-dropdowns (fasta zoner) + textruta för födelsedagar
  admin.css             # Egen, enkel adminstil (separat från TV-kioskens style.css)
  admin.js              # All admin-logik: login, toggles, zon-tilldelning, spara/förhandsgranska födelsedagar
```

## Starta lokalt

```bash
pip install -r requirements.txt
cp .env.example .env   # sätt ADMIN_PASSWORD och SECRET_KEY
python -m backend.main # → http://localhost:8080 (admin: /admin)
```

## API

**`GET /api/card?ignore=<id>`** — returnerar nästa kort för mitt-rotationen:

```json
{
  "type": "quote",
  "display_seconds": 20,
  "background": "/images/bg_01.jpg",
  "content": { "id": 94, "quote": "...", "author": "...", "company": "..." }
}
```

**`GET /api/zone/<zone_id>?ignore=<id>`** — returnerar kortet för den widget som är tilldelad en fast zon (`zone_id` ∈ `left-top`/`left-bottom`/`right-top`/`right-bottom`). Samma kort-form som ovan, eller `{"type": "empty", ...}` om zonen saknar tilldelning. Frontend renderar alltid i `"compact"`-läge för dessa.

## Citattjänst

Extern tjänst på `http://quotes.lkpg.cendio.se/api/quotes/random?ignore=<id>` — ska **inte** ändras, bara konsumeras.

## Admin-panel

`GET /admin` — login-skyddad sida (delat lösenord, `ADMIN_PASSWORD` i `.env`, sessionscookie signerad med `SECRET_KEY`).

- `POST /admin/api/login` `{password}` / `POST /admin/api/logout` / `GET /admin/api/session`
- `GET /admin/api/widgets` → lista widgets med `enabled`-state för **mitt-rotationen** (byggd från `widgets_registry.WIDGETS` + `store.py`)
- `POST /admin/api/widgets/<id>/toggle` `{enabled: bool}`
- `GET /admin/api/zones` → lista de fyra fasta zonerna med vilken widget (eller `null`) som är tilldelad
- `POST /admin/api/zones/<zone_id>` `{widget: "quote"|"weather"|"birthday"|null}`
- `GET /admin/api/birthdays` → `{raw: "..."}` (senast sparade inklistrade text)
- `POST /admin/api/birthdays` `{raw: "..."}` → sparar och returnerar förhandsgranskning: `{count, today: [namn...], invalid: [rader...]}`

Födelsedags-widgeten visas i mitt-rotationen 5 dagar innan någon fyller år (alla inom fönstret visas samtidigt) och utesluts annars helt. En fast zon tilldelad födelsedagar visar däremot alltid kortet — `content.people` kan vara en tom lista, och `BirthdayWidget.js` visar då en reservtext ("Inga födelsedagar inom kort") istället för att vara tom. Ingen Sheets-integration än, bara den inklistrade texten.

## Lägga till en ny widget

1. Skapa `backend/providers/<namn>.py` med en provider-klass.
2. Skapa `backend/cards/<namn>_card.py` med en `build_<namn>_card(data)`-funktion som **alltid** returnerar ett kort (reservinnehåll om datan är tom — fasta zoner ska aldrig bli blanka).
3. Lägg till typen i `backend/widgets_registry.py` (`WIDGET_ORDER` + `WIDGETS`, ange om den är `editable`).
4. Lägg till typen i `_build_card` i `backend/api.py`. Om widgeten bara ska delta i mitt-rotationen när den har något att visa (som födelsedagar), lägg den aktivitetskontrollen i `_active_rotation_types` — den gäller bara mitten, inte fasta zoner.
5. Skapa `frontend/widgets/<Namn>Widget.js` med en `render<Namn>Card(content, mode = "hero")`-funktion som hanterar både `"hero"`- och `"compact"`-läge.
6. Registrera renderaren i `frontend/app.js` under `renderers`.
7. Eventuellt `backend/admin.py` om widgeten behöver eget redigeringsfält.

## Kodkonventioner

- **Backend:** Python, Flask eller FastAPI (keep it simple).
- **Frontend:** Vanilla HTML, CSS och modern JavaScript — inga tunga ramverk.
- **Modularitet:** Varje ny funktion ska vara en egen, fristående Widget-klass/komponent.

## Projektmedlemmar & Roller

- **Alex (Erfaren utvecklare):** Äger arkitekturen, motorn, datalagret och kodstrukturen.
- **Per (HR-ansvarig):** Äger innehållet, reglerna (när saker ska visas) och designkänslan.
- **Claude Code (Parprogrammerare):** Skriver koden, förklarar pedagogiskt och hjälper till att strukturera uppgifterna i små steg så att både Alex och Per hänger med.
