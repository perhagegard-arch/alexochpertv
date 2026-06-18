import random
from ..config import BACKGROUND_IMAGES, DISPLAY_SECONDS


def build_birthday_card(data):
    return {
        "type": "birthday",
        "display_seconds": DISPLAY_SECONDS,
        "background": f"/images/{random.choice(BACKGROUND_IMAGES)}",
        "content": {"people": data["upcoming"]},
    }
