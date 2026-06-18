# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Projekt: Fikarums-TV (Smart Dashboard)

En modulär dashboard-plattform för en fikarums-TV som körs på en Raspberry Pi i Kiosk-läge. Appen fungerar som en plattform baserad på "Widgets" (Kort) som dynamiskt växlar innehåll.

## Arkitektur

Systemet består av fyra delar:

1. **Frontend (HTML/JS/CSS):** En container som roterar mellan aktiva widgets, sköter animationer och uppdaterar innehåll.
2. **Regelmotor (Backend/Python):** Avgör vilka kort som är aktuella baserat på tid, datum och prioritet (`backend/rules.py`, ej implementerad än — utöver det enkla 5-dagarsfönstret för födelsedagar, se nedan).
3. **Datalager (Backend/Python):** Hämtar data från Google Sheets och serverar till frontenden via ett API (`backend/sheets.py`, ej implementerad än). Tills den finns klistras innehåll in manuellt via admin-panelen och sparas i `data/state.json`.
4. **Widgets:** Varje widget är en fristående modul/klass. Den befintliga citat-appen kapslas in som `QuoteWidget` — den ska inte skrivas om, bara lyftas in.
5. **Admin-panel (`/admin`):** Per kan logga in med ett delat lösenord, slå på/av widgets och redigera innehåll för widgets som har det (just nu bara födelsedagar). Toggle-state och inklistrad text sparas i `data/state.json` och respekteras av rotationen i `backend/api.py`.

## Filstruktur

```
backend/
  main.py              # Flask-app, startar servern (port 8080), registrerar api + admin
  api.py               # GET /api/card?ignore=<id> — dynamisk rotation, respekterar toggles
  admin.py             # Blueprint: /admin (sida) + /admin/api/* (login, widgets, birthdays)
  auth.py              # login_required-decorator + lösenordskontroll (session-baserad)
  store.py             # JsonStore — läser/skriver data/state.json
  widgets_registry.py  # Delad källa: vilka widget-typer finns, ordning, redigerbara eller inte
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
    birthday_card.py   # Returnerar None om ingen har födelsedag inom 5 dagar

data/
  state.json           # Körtids-state (widget-toggles + inklistrad födelsedagstext), gitignored

frontend/
  index.html           # Shell med två .card-layer divs (A/B för cross-fade)
  style.css            # Fullskärm, cross-fade via opacity-transition
  app.js               # Pollar /api/card, roterar kort med cross-fade
  images/              # Bakgrundsbilder (.jpg) — listas i .env
  widgets/
    QuoteWidget.js     # Renderar HTML för citat-kortet
    WeatherWidget.js
    BirthdayWidget.js
  admin.html            # Login + widget-toggles + textruta för födelsedagar
  admin.css             # Egen, enkel adminstil (separat från TV-kioskens style.css)
  admin.js              # All admin-logik: login, toggles, spara/förhandsgranska födelsedagar
```

## Starta lokalt

```bash
pip install -r requirements.txt
cp .env.example .env   # sätt ADMIN_PASSWORD och SECRET_KEY
python -m backend.main # → http://localhost:8080 (admin: /admin)
```

## API

**`GET /api/card?ignore=<id>`** — returnerar nästa kort att visa:

```json
{
  "type": "quote",
  "display_seconds": 20,
  "background": "/images/bg_01.jpg",
  "content": { "id": 94, "quote": "...", "author": "...", "company": "..." }
}
```

## Citattjänst

Extern tjänst på `http://quotes.lkpg.cendio.se/api/quotes/random?ignore=<id>` — ska **inte** ändras, bara konsumeras.

## Admin-panel

`GET /admin` — login-skyddad sida (delat lösenord, `ADMIN_PASSWORD` i `.env`, sessionscookie signerad med `SECRET_KEY`).

- `POST /admin/api/login` `{password}` / `POST /admin/api/logout` / `GET /admin/api/session`
- `GET /admin/api/widgets` → lista widgets med `enabled`-state (byggd från `widgets_registry.WIDGETS` + `store.py`)
- `POST /admin/api/widgets/<id>/toggle` `{enabled: bool}`
- `GET /admin/api/birthdays` → `{raw: "..."}` (senast sparade inklistrade text)
- `POST /admin/api/birthdays` `{raw: "..."}` → sparar och returnerar förhandsgranskning: `{count, today: [namn...], invalid: [rader...]}`

Födelsedags-widgeten visas i TV-rotationen 5 dagar innan någon fyller år (alla inom fönstret visas samtidigt) och försvinner annars helt — ingen Sheets-integration än, bara den inklistrade texten.

## Lägga till en ny widget

1. Skapa `backend/providers/<namn>.py` med en provider-klass.
2. Skapa `backend/cards/<namn>_card.py` med en `build_<namn>_card(data)`-funktion. Returnera `None` om widgeten inte ska visas just nu (se `birthday_card.py`).
3. Lägg till typen i `backend/widgets_registry.py` (`WIDGET_ORDER` + `WIDGETS`, ange om den är `editable`).
4. Registrera typen i `backend/api.py` (rotation) och eventuellt `backend/admin.py` om den behöver eget redigeringsfält.
5. Skapa `frontend/widgets/<Namn>Widget.js` med en `render<Namn>Card(content)`-funktion.
6. Registrera renderaren i `frontend/app.js` under `renderers`.

## Kodkonventioner

- **Backend:** Python, Flask eller FastAPI (keep it simple).
- **Frontend:** Vanilla HTML, CSS och modern JavaScript — inga tunga ramverk.
- **Modularitet:** Varje ny funktion ska vara en egen, fristående Widget-klass/komponent.

## Projektmedlemmar & Roller

- **Alex (Erfaren utvecklare):** Äger arkitekturen, motorn, datalagret och kodstrukturen.
- **Per (HR-ansvarig):** Äger innehållet, reglerna (när saker ska visas) och designkänslan.
- **Claude Code (Parprogrammerare):** Skriver koden, förklarar pedagogiskt och hjälper till att strukturera uppgifterna i små steg så att både Alex och Per hänger med.
