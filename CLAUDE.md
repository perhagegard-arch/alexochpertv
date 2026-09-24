# CLAUDE.md – fika-portal

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Vad det här är

En informationsskärm för fikarummet hos Cendio (Linköping; vi gör ThinLinc).
En separat app, "quoted", visar idag kundcitat på en TV. Vi bygger en NY
**portal** som visar mer än citat och som är **kontextmedveten** — rätt
innehåll vid rätt tid. Citaten blir EN widget bland flera, hämtad via quoteds
API. **Vi rör aldrig quoted-appen.**

## Två appar

1. **quoted** (befintlig, OFÖRÄNDRAD): Flask-tjänst på VM:en. Vi konsumerar
   bara dess API.
2. **fika-portal** (det vi bygger): dashboard-plattformen — koden i detta repo.

## Hur vi jobbar

- Övningsprojekt. Alex är erfaren utvecklare, Per jobbar med HR. Förklara
  *varför*, inte bara *vad*.
- Små steg på en arbetsbranch. Föreslå plan innan större ändringar. Små commits.
- Ansvar: **Alex äger motorn** (visning, regler, datalager, admin-teknik),
  **Per äger innehåll och regler** (vilka kort, när de visas, vilken data).

## quoted-appens API (det vi konsumerar)

Binder `127.0.0.1:5000` via gunicorn/systemd.
- `GET /api/quotes/random?ignore=<id>` → JSON `{id, quote, author, company, date}`

Bas-URL ska vara konfigurerbar. I den här utvecklingsmiljön är den satt via
`.env` (`QUOTES_API_URL`) till `http://quotes.lkpg.cendio.se/api/quotes/random`
— den publika adressen för samma quoted-tjänst (se `backend/providers/quotes.py`).

## Skärmlayout: tre zoner

- **Mitten** – en stor glaspanel (4/5 av bredden, rundade hörn) som ROTERAR
  mellan widgets. Här bor "ögonblicken": citat, födelsedag, ny kund, m.m.
  Korten i mitten har ingen egen bakgrund — panelen är bakgrunden.
- **Två fasta zoner** till vänster (staplade, 1/5 av bredden) – visar var sin
  vald widget, roterar inte. Här bor alltid-relevant glasbart:
  klocka, väder, nästa händelse, global impact. (Högerzonerna togs bort
  2026-09-24 för att ge citaten mer plats.)
- Fasta zoner med en widget som inte alltid har innehåll MÅSTE ha reservinnehåll
  så zonen aldrig blir tom.

*Implementerat i `frontend/index.html` (CSS-grid med `zone-center` + två
`.zone`-divar), `style.css` och `app.js` (`showNext()` för mitten,
`showZone()` per fast zon) — se Teknisk referens nedan för detaljer.*

## Widget-arkitektur

- **Provider** (backend) per widget hämtar från sin källa (quoteds API, en
  inklistrad lista, ett API, config). Backenden håller ev. hemligheter.
- **Två render-lägen** per widget: kompakt (fasta zoner) och hjälte (mitten).
  Samma data, två renderingar.
- **Regelmotor** avgör vilka kort som är aktuella nu (tidsfönster, veckodag,
  dag-i-månaden, "finns innehåll just nu", prioritet).
- **Admin** (inloggad, inte öppen): på/av-toggle per widget, val av vilken
  widget som sitter i varje fast zon + vilka som roterar i mitten, och för
  widgets med eget innehåll ett enkelt redigeringsfält (t.ex. födelsedagar via
  inklistrad text — Sheets-integration uppskjuten till efter semestern).

*Status idag: providers, två render-lägen (`mode: "hero" | "compact"`) och
admin (toggles + zon-val + textfält) är byggda. Den generella regelmotorn
(tidsfönster, veckodag, prioritet) är fortfarande en stub i `backend/rules.py`
— det enda regelmotor-liknande som finns idag är födelsedagarnas
5-dagarsfönster, som ligger direkt i `backend/birthdays.py`/`backend/api.py`
snarare än i en separat regelmotor.*

## Designprinciper för skärmen (från benchmark av bra arbetsplatser)

- En idé per vy — läsavstånd på flera meter, korta rubriker.
- Fira UTFALL, visa inte måltal. Ingen KPI-press (extra viktigt för ett team
  på ~13 personer).
- Inget ljud.
- Inget gammalt innehåll — byt eller ta bort vyer som inte ändrats på länge.
- Led med igenkänning och firande, inte marknadsföring (teamet ser ThinLinc-
  varumärket hela dagen ändå).

## Widgets vi vill ha

**Till demon:** citat (quoted) · födelsedagar (inklistrad lista) ·
ny-kund-firande ("Välkommen, [org] i [land]!") · global impact
("~120 000 använder en Linux-desktop via oss; 500+ org") · klocka & datum ·
väder (Linköping).
**Efter semestern:** arbetsjubileum · "detta skeppade vi" (ThinLinc-release /
GitHub / TigerVNC-noVNC) · nyanställd-välkomst · eventbilder · transport
(avgångar från Mjärdevi) · "detta hände denna dag" · lunchmenyer · live-data
(CRM för kunder, Sheets för födelsedagar, riktiga impact-siffror).

*Status: citat ✅, väder ✅ och födelsedagar ✅ är implementerade widgets.
Ny-kund-firande, global impact och klocka & datum är inte byggda än.*

## Roadmap (uppdaterad — guide, inte kontrakt)

- **Pass 1:** Portal-scaffold + rotationsmotor + citat-widget via quoteds API.
- **Pass 2:** Femzonslayout + två render-lägen + klocka och väder i fasta zoner.
- **Pass 3:** Regelmotor + admin (toggles + zon-tilldelning + födelsedags-paste)
  + födelsedagskort + ny-kund-kort + global-impact-kort.
- **Pass 4:** Polish (festligt födelsedagskort, övergångar), demo-genrep, och
  stretch-mål om tid finns (gym-påminnelse, jubileum).
- **Efter semestern:** live-datakällor + övriga widgets ovan.

*Status 2026-09-24: kärnan i Pass 1–3 är byggd (rotationsmotor, citat-widget,
två render-lägen, väder, admin med toggles/zon-tilldelning/födelsedags-paste,
födelsedagskort). Layouten förenklades 2026-09-24 från fem till tre zoner
(två fasta till vänster + stor citatpanel). Kvar: klocka, ny-kund-kort och
global-impact-kort, samt den mer generella regelmotorn.*

## Driftsättning

**Live: `http://10.48.2.38:8080/`** på `lab-38` (`lab-38.lkpg.cendio.se`),
admin på `/admin`. Kör commit `f35c790`+ (tre-zons-layouten), ominstallerad
2026-09-24.

**Viktigt: lab-38 är en labbmaskin och kan rensas.** Installationen från
2026-08-03 försvann helt (katalog, tjänst, SSH-nyckel — troligen vid
omstarten 2026-09-07). Inte bekräftad som permanent TV-dator. Om TV-vyn är
borta: installera om enligt nedan.

### Så är den uppsatt

- **Inloggning:** `ssh -i ~/.ssh/id_ed25519_cendio claude@lab-38` (använd
  kortnamnet `lab-38` — det är det som finns i `known_hosts`). `claude` har
  sudo med lösenord.
- **Kod:** `/opt/fika-portal` (inte hemkatalog!). SELinux är Enforcing och
  blockerar tyst att systemd kör kod märkt `user_home_t` (`status=203/EXEC`,
  "Failed to load environment files"). `/opt` ger `usr_t` och fungerar.
- **Ingen git-klon på servern** — koden kopieras med `git archive`, så inga
  GitHub-nycklar behövs där. `DEPLOYED_COMMIT` visar vilken commit som körs.
- **Tjänst:** `fika-portal.service` (systemd, enabled, `Restart=always`),
  gunicorn från `.venv` på `0.0.0.0:8080`.
- **Brandvägg:** port 8080/tcp öppnad permanent i firewalld.
- **Hemligheter:** `.env` (chmod 600) med slumpat `ADMIN_PASSWORD` och
  `SECRET_KEY` samt Unsplash-nyckeln — **finns inte i repot**. Fråga Per om
  admin-lösenordet behövs.
- **Innehåll/inställningar** (widget-toggles, zoner, födelsedagslistan) ligger
  i `data/state.json` på servern och försvinner om maskinen rensas. Nuvarande
  uppsättning: mitten roterar bara citat, vänster topp = väder, vänster
  botten = födelsedagar. Lokala `data/state.json` hos Per är samma — kan
  laddas upp igen via admin-API:t.

### Uppdatera med ny kod (från repot lokalt)

```bash
git archive --format=tar main | ssh -i ~/.ssh/id_ed25519_cendio claude@lab-38 \
  "tar -xf - -C /opt/fika-portal && echo $(git rev-parse --short main) > /opt/fika-portal/DEPLOYED_COMMIT"
ssh -t -i ~/.ssh/id_ed25519_cendio claude@lab-38 'sudo systemctl restart fika-portal'
```

`tar -x` skriver över kodfilerna men rör inte `.env`, `.venv` eller `data/`.
Kör `.venv/bin/pip install -r requirements.txt` om beroenden ändrats.

### Installera om från början

1. `sudo mkdir -p /opt/fika-portal && sudo chown claude:claude /opt/fika-portal`
2. Kopiera koden med `git archive` enligt ovan.
3. `cd /opt/fika-portal && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`
4. `cp .env.example .env && chmod 600 .env`, fyll i `ADMIN_PASSWORD`,
   `SECRET_KEY` (`python3 -c "import secrets;print(secrets.token_hex(32))"`)
   och `UNSPLASH_ACCESS_KEY`.
5. `./install_service.sh`
6. `sudo firewall-cmd --permanent --add-port=8080/tcp && sudo firewall-cmd --reload`
7. Logga in på `/admin` och sätt zoner/toggles + klistra in födelsedagar.

### Historik

- **2026-08-03:** första testinstallationen. Två buggar fixade:
  `start_portal.sh` använde global `gunicorn` istället för venv:ets, och
  `.env.example` refererade `bg_02.jpg` som aldrig lagts till (trasig
  bakgrund ~50 % av gångerna).
- **2026-09-24:** ominstallerad efter att maskinen rensats, med ny layout.

### Nästa steg

1. Kolla med labbansvarig (eller Alex) om lab-38 får stå orörd, annars flytta
   till den riktiga datorn vid fikarums-TV:n och sätt webbläsaren i
   kiosk-läge mot rätt adress.
2. Byt lösenordet för `claude` på lab-38 (det har delats i en chatt).
3. Fortsätt med kvarvarande kort: klocka, ny-kund, global-impact.

---

## Teknisk referens

### Filstruktur

```
backend/
  main.py              # Flask-app, startar servern (port 8080), registrerar api + admin
  api.py               # GET /api/card (mitt-rotation) + GET /api/zone/<id> (fast zon) — delar _build_card
  admin.py             # Blueprint: /admin (sida) + /admin/api/* (login, widgets, zones, birthdays)
  auth.py              # login_required-decorator + lösenordskontroll (session-baserad)
  store.py             # JsonStore — läser/skriver data/state.json
  widgets_registry.py  # Delad källa: WIDGET_ORDER/WIDGETS samt ZONES/ZONE_IDS (de två fasta zonerna till vänster)
  birthdays.py          # parse_birthdays(), upcoming_within(), birthdays_today() — ren parsing-logik
  config.py            # Läser .env: QUOTES_API_URL, DISPLAY_SECONDS, BACKGROUND_IMAGES, ADMIN_PASSWORD, SECRET_KEY
  rules.py             # (stub) Regelmotor — generell regelmotor ej byggd än
  sheets.py            # (stub) Google Sheets-integration
  providers/
    quotes.py          # QuoteProvider — anropar quoted-appens API
    weather.py         # WeatherProvider — Open-Meteo API
    birthdays.py       # BirthdayProvider — läser store, returnerar upcoming inom 5 dagar
  cards/
    quote_card.py      # Bygger card-JSON från provider-data
    weather_card.py
    birthday_card.py   # Returnerar alltid kortet — content.people kan vara tom lista

data/
  state.json           # Körtids-state (widget-toggles, zon-tilldelningar, inklistrad födelsedagstext), gitignored

frontend/
  index.html           # 5-zon-grid: zone-center (cross-fade, hjälte-läge) + 4 .zone-divar (kompakt läge)
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

### Starta lokalt

```bash
pip install -r requirements.txt
cp .env.example .env   # sätt ADMIN_PASSWORD och SECRET_KEY
python -m backend.main # → http://localhost:8080 (admin: /admin)
```

### API (fika-portalens eget, inte quoteds)

**`GET /api/card?ignore=<id>`** — returnerar nästa kort för mitt-rotationen:

```json
{
  "type": "quote",
  "display_seconds": 20,
  "background": "/images/bg_01.jpg",
  "content": { "id": 94, "quote": "...", "author": "...", "company": "..." }
}
```

**`GET /api/zone/<zone_id>?ignore=<id>`** — returnerar kortet för den widget som är tilldelad en fast zon (`zone_id` ∈ `left-top`/`left-bottom`). Samma kort-form som ovan, eller `{"type": "empty", ...}` om zonen saknar tilldelning. Frontend renderar alltid i `"compact"`-läge för dessa.

### Admin-panel

`GET /admin` — login-skyddad sida (delat lösenord, `ADMIN_PASSWORD` i `.env`, sessionscookie signerad med `SECRET_KEY`).

- `POST /admin/api/login` `{password}` / `POST /admin/api/logout` / `GET /admin/api/session`
- `GET /admin/api/widgets` → lista widgets med `enabled`-state för **mitt-rotationen** (byggd från `widgets_registry.WIDGETS` + `store.py`)
- `POST /admin/api/widgets/<id>/toggle` `{enabled: bool}`
- `GET /admin/api/zones` → lista de två fasta zonerna med vilken widget (eller `null`) som är tilldelad
- `POST /admin/api/zones/<zone_id>` `{widget: "quote"|"weather"|"birthday"|null}`
- `GET /admin/api/birthdays` → `{raw: "..."}` (senast sparade inklistrade text)
- `POST /admin/api/birthdays` `{raw: "..."}` → sparar och returnerar förhandsgranskning: `{count, today: [namn...], invalid: [rader...]}`

Födelsedags-widgeten visas i mitt-rotationen 5 dagar innan någon fyller år (alla inom fönstret visas samtidigt) och utesluts annars helt. En fast zon tilldelad födelsedagar visar däremot alltid kortet — `content.people` kan vara en tom lista, och `BirthdayWidget.js` visar då en reservtext ("Inga födelsedagar inom kort") istället för att vara tom. Ingen Sheets-integration än, bara den inklistrade texten.

### Lägga till en ny widget

1. Skapa `backend/providers/<namn>.py` med en provider-klass.
2. Skapa `backend/cards/<namn>_card.py` med en `build_<namn>_card(data)`-funktion som **alltid** returnerar ett kort (reservinnehåll om datan är tom — fasta zoner ska aldrig bli blanka).
3. Lägg till typen i `backend/widgets_registry.py` (`WIDGET_ORDER` + `WIDGETS`, ange om den är `editable`).
4. Lägg till typen i `_build_card` i `backend/api.py`. Om widgeten bara ska delta i mitt-rotationen när den har något att visa (som födelsedagar), lägg den aktivitetskontrollen i `_active_rotation_types` — den gäller bara mitten, inte fasta zoner.
5. Skapa `frontend/widgets/<Namn>Widget.js` med en `render<Namn>Card(content, mode = "hero")`-funktion som hanterar både `"hero"`- och `"compact"`-läge.
6. Registrera renderaren i `frontend/app.js` under `renderers`.
7. Eventuellt `backend/admin.py` om widgeten behöver eget redigeringsfält.

### Kodkonventioner

- **Backend:** Python, Flask eller FastAPI (keep it simple).
- **Frontend:** Vanilla HTML, CSS och modern JavaScript — inga tunga ramverk.
- **Modularitet:** Varje ny funktion ska vara en egen, fristående Widget-klass/komponent.
