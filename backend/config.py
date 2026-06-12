import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

QUOTES_API_URL = os.getenv("QUOTES_API_URL", "http://quotes.lkpg.cendio.se/api/quotes/random")
DISPLAY_SECONDS = int(os.getenv("DISPLAY_SECONDS", "20"))
BACKGROUND_IMAGES = [
    img.strip()
    for img in os.getenv("BACKGROUND_IMAGES", "bg_01.jpg").split(",")
    if img.strip()
]
