# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Projekt: Fikarums-TV (Smart Dashboard)

En modulär dashboard-plattform för en fikarums-TV som körs på en Raspberry Pi i Kiosk-läge. Appen fungerar som en plattform baserad på "Widgets" (Kort) som dynamiskt växlar innehåll.

## Arkitektur

Systemet består av fyra delar:

1. **Frontend (HTML/JS/CSS):** En container som roterar mellan aktiva widgets, sköter animationer och uppdaterar innehåll.
2. **Regelmotor (Backend/Python):** Avgör vilka kort som är aktuella baserat på tid, datum och prioritet (`backend/rules.py`, ej implementerad än).
3. **Datalager (Backend/Python):** Hämtar data från Google Sheets och serverar till frontenden via ett API (`backend/sheets.py`, ej implementerad än).
4. **Widgets:** Varje widget är en fristående modul/klass. Den befintliga citat-appen kapslas in som `QuoteWidget` — den ska inte skrivas om, bara lyftas in.

## Filstruktur

```
backend/
  main.py              # Flask-app, startar servern (port 8080)
  api.py               # GET /api/card?ignore=<id>
  config.py            # Läser .env: QUOTES_API_URL, DISPLAY_SECONDS, BACKGROUND_IMAGES
  rules.py             # (stub) Regelmotor
  sheets.py            # (stub) Google Sheets-integration
  providers/
    quotes.py          # QuoteProvider — anropar citattjänsten
  cards/
    quote_card.py      # Bygger card-JSON från provider-data

frontend/
  index.html           # Shell med två .card-layer divs (A/B för cross-fade)
  style.css            # Fullskärm, cross-fade via opacity-transition
  app.js               # Pollar /api/card, roterar kort med cross-fade
  images/              # Bakgrundsbilder (.jpg) — listas i .env
  widgets/
    QuoteWidget.js     # Renderar HTML för citat-kortet
```

## Starta lokalt

```bash
pip install -r requirements.txt
cp .env.example .env   # justera vid behov
python -m backend.main # → http://localhost:8080
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

## Lägga till en ny widget

1. Skapa `backend/providers/<namn>.py` med en provider-klass.
2. Skapa `backend/cards/<namn>_card.py` med en `build_<namn>_card(data)`-funktion.
3. Registrera typen i `backend/api.py`.
4. Skapa `frontend/widgets/<Namn>Widget.js` med en `render<Namn>Card(content)`-funktion.
5. Registrera renderaren i `frontend/app.js` under `renderers`.

## Kodkonventioner

- **Backend:** Python, Flask eller FastAPI (keep it simple).
- **Frontend:** Vanilla HTML, CSS och modern JavaScript — inga tunga ramverk.
- **Modularitet:** Varje ny funktion ska vara en egen, fristående Widget-klass/komponent.

## Projektmedlemmar & Roller

- **Alex (Erfaren utvecklare):** Äger arkitekturen, motorn, datalagret och kodstrukturen.
- **Per (HR-ansvarig):** Äger innehållet, reglerna (när saker ska visas) och designkänslan.
- **Claude Code (Parprogrammerare):** Skriver koden, förklarar pedagogiskt och hjälper till att strukturera uppgifterna i små steg så att både Alex och Per hänger med.
