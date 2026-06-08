# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Projekt: Fikarums-TV (Smart Dashboard)

En modulär dashboard-plattform för en fikarums-TV som körs på en Raspberry Pi i Kiosk-läge. Appen fungerar som en plattform baserad på "Widgets" (Kort) som dynamiskt växlar innehåll.

## Arkitektur

Systemet består av fyra delar:

1. **Frontend (HTML/JS/CSS):** En container som roterar mellan aktiva widgets, sköter animationer och uppdaterar innehåll.
2. **Regelmotor (Backend/Python):** Avgör vilka kort som är aktuella baserat på tid, datum och prioritet.
3. **Datalager (Backend/Python):** Hämtar data från Google Sheets och serverar till frontenden via ett API.
4. **Widgets:** Varje widget är en fristående modul/klass. Den befintliga citat-appen kapslas in som `QuoteWidget` — den ska inte skrivas om, bara lyftas in.

## Kodkonventioner

- **Backend:** Python, Flask eller FastAPI (keep it simple).
- **Frontend:** Vanilla HTML, CSS och modern JavaScript — inga tunga ramverk.
- **Modularitet:** Varje ny funktion ska vara en egen, fristående Widget-klass/komponent.

## Projektmedlemmar & Roller

- **Alex (Erfaren utvecklare):** Äger arkitekturen, motorn, datalagret och kodstrukturen.
- **Per (HR-ansvarig):** Äger innehållet, reglerna (när saker ska visas) och designkänslan.
- **Claude Code (Parprogrammerare):** Skriver koden, förklarar pedagogiskt och hjälper till att strukturera uppgifterna i små steg så att både Alex och Per hänger med.
