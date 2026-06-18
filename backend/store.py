import json
from .config import STATE_FILE
from .widgets_registry import WIDGET_ORDER, ZONE_IDS

DEFAULT_STATE = {
    "widgets": {widget_type: True for widget_type in WIDGET_ORDER},
    "zones": {zone_id: None for zone_id in ZONE_IDS},
    "birthdays_raw": "",
}


class JsonStore:
    def __init__(self, path=STATE_FILE):
        self.path = path

    def _load(self):
        if not self.path.exists():
            self._save(DEFAULT_STATE)
            return dict(DEFAULT_STATE)
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)
        data.setdefault("widgets", {})
        for widget_type in WIDGET_ORDER:
            data["widgets"].setdefault(widget_type, True)
        data.setdefault("zones", {})
        for zone_id in ZONE_IDS:
            data["zones"].setdefault(zone_id, None)
        data.setdefault("birthdays_raw", "")
        return data

    def _save(self, data):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_widget_enabled(self, widget_type):
        return bool(self._load()["widgets"].get(widget_type, True))

    def get_widget_states(self):
        return dict(self._load()["widgets"])

    def set_widget_enabled(self, widget_type, enabled):
        data = self._load()
        data["widgets"][widget_type] = bool(enabled)
        self._save(data)

    def get_zone(self, zone_id):
        return self._load()["zones"].get(zone_id)

    def get_zones(self):
        return dict(self._load()["zones"])

    def set_zone(self, zone_id, widget_type):
        data = self._load()
        data["zones"][zone_id] = widget_type
        self._save(data)

    def get_birthdays_raw(self):
        return self._load()["birthdays_raw"]

    def set_birthdays_raw(self, text):
        data = self._load()
        data["birthdays_raw"] = text
        self._save(data)
