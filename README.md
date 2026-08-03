# alexochpertv – fika-portal

TV-projekt: informationsskärm för fikarummet hos Cendio. Se `CLAUDE.md` för
bakgrund och arkitektur.

## Installation på en ny maskin (t.ex. den TV:n är kopplad till)

Kräver Python 3 och pip.

```bash
git clone <repo-url> fika-portal
cd fika-portal

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
nano .env   # sätt minst ADMIN_PASSWORD och SECRET_KEY
```

### Köra som systemd-tjänst (rekommenderas för TV-drift)

```bash
./install_service.sh
```

Scriptet installerar `fika-portal.service`, startar tjänsten och skriver ut
vilken adress TV:ns webbläsare ska öppna (`http://<IP>:8080/`). Tjänsten
startar automatiskt vid omstart (`Restart=always`, `WantedBy=multi-user.target`).

Kontrollera status/loggar:

```bash
sudo systemctl status fika-portal
sudo journalctl -u fika-portal -f
```

### Köra manuellt (utveckling/felsökning, utan systemd)

```bash
python -m backend.main   # → http://localhost:8080 (admin: /admin)
```

## Admin-panel

`http://<IP>:8080/admin` — logga in med lösenordet från `ADMIN_PASSWORD` i
`.env`. Här styrs vilka widgets som roterar i mitten, vilken widget som
sitter i varje fast zon, samt födelsedagslistan.
