import random
from ..config import BACKGROUND_IMAGES, DISPLAY_SECONDS


def build_weather_card(data):
    return {
        "type": "weather",
        "display_seconds": DISPLAY_SECONDS,
        "background": f"/images/{random.choice(BACKGROUND_IMAGES)}",
        "content": data,
    }
