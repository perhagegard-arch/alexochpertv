import random
from ..config import BACKGROUND_IMAGES, DISPLAY_SECONDS


def build_quote_card(data):
    return {
        "type": "quote",
        "display_seconds": DISPLAY_SECONDS,
        "background": f"/images/{random.choice(BACKGROUND_IMAGES)}",
        "content": {
            "id": data["id"],
            "quote": data["quote"],
            "author": data["author"],
            "company": data.get("company", ""),
            "date": data.get("date", ""),
        },
    }
