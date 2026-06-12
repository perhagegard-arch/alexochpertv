from flask import Blueprint, jsonify, request
from .providers.quotes import QuoteProvider
from .providers.weather import WeatherProvider
from .cards.quote_card import build_quote_card
from .cards.weather_card import build_weather_card

api = Blueprint("api", __name__)

_quote_provider = QuoteProvider()
_weather_provider = WeatherProvider()

_rotation = ["quote", "weather"]
_rotation_index = 0


@api.route("/api/card")
def get_card():
    global _rotation_index
    card_type = _rotation[_rotation_index % len(_rotation)]
    _rotation_index += 1

    try:
        if card_type == "quote":
            ignore_id = request.args.get("ignore", type=int)
            data = _quote_provider.get(ignore_id=ignore_id)
            return jsonify(build_quote_card(data))
        else:
            data = _weather_provider.get()
            return jsonify(build_weather_card(data))
    except Exception as exc:
        return jsonify({"error": str(exc)}), 502
