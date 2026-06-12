from flask import Blueprint, jsonify, request
from .providers.quotes import QuoteProvider
from .cards.quote_card import build_quote_card

api = Blueprint("api", __name__)
_quote_provider = QuoteProvider()


@api.route("/api/card")
def get_card():
    ignore_id = request.args.get("ignore", type=int)
    try:
        data = _quote_provider.get(ignore_id=ignore_id)
        return jsonify(build_quote_card(data))
    except Exception as exc:
        return jsonify({"error": str(exc)}), 502
