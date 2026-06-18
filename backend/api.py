from flask import Blueprint, jsonify, request
from .providers.quotes import QuoteProvider
from .providers.weather import WeatherProvider
from .providers.birthdays import BirthdayProvider
from .cards.quote_card import build_quote_card
from .cards.weather_card import build_weather_card
from .cards.birthday_card import build_birthday_card
from .store import JsonStore
from .widgets_registry import WIDGET_ORDER, ZONE_IDS

api = Blueprint("api", __name__)

_store = JsonStore()
_quote_provider = QuoteProvider()
_weather_provider = WeatherProvider()
_birthday_provider = BirthdayProvider(_store)

_rotation_index = 0

_EMPTY_CARD = {"type": "empty", "display_seconds": 10, "content": {}}


def _build_card(widget_type, ignore_id):
    if widget_type == "quote":
        data = _quote_provider.get(ignore_id=ignore_id)
        return build_quote_card(data)
    if widget_type == "weather":
        data = _weather_provider.get()
        return build_weather_card(data)
    if widget_type == "birthday":
        data = _birthday_provider.get()
        return build_birthday_card(data)
    raise ValueError(f"Okänd widget-typ: {widget_type}")


def _active_rotation_types():
    """Widget-typer som är påslagna och har något att visa just nu.

    Födelsedagar kräver att minst en person ligger inom 5-dagarsfönstret;
    det går att kolla utan nätverksanrop, så vi gör det för alla requests.
    """
    active = []
    for widget_type in WIDGET_ORDER:
        if not _store.get_widget_enabled(widget_type):
            continue
        if widget_type == "birthday":
            data = _birthday_provider.get()
            if not data["upcoming"]:
                continue
        active.append(widget_type)
    return active


@api.route("/api/card")
def get_card():
    global _rotation_index

    active_types = _active_rotation_types()
    if not active_types:
        return jsonify(_EMPTY_CARD)

    card_type = active_types[_rotation_index % len(active_types)]
    _rotation_index += 1

    ignore_id = request.args.get("ignore", type=int)
    try:
        card = _build_card(card_type, ignore_id)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 502
    return jsonify(card)


@api.route("/api/zone/<zone_id>")
def get_zone(zone_id):
    if zone_id not in ZONE_IDS:
        return jsonify({"error": "Okänd zon"}), 404

    widget_type = _store.get_zone(zone_id)
    if not widget_type:
        return jsonify(_EMPTY_CARD)

    ignore_id = request.args.get("ignore", type=int)
    try:
        card = _build_card(widget_type, ignore_id)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 502
    return jsonify(card)
