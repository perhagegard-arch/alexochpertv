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

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY", "")
BACKGROUND_INTERVAL_SECONDS = int(os.getenv("BACKGROUND_INTERVAL_SECONDS", "60"))
BIRTHDAY_WINDOW_DAYS = int(os.getenv("BIRTHDAY_WINDOW_DAYS", "5"))

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-satt-din-egen-i-env")

STATE_FILE = Path(__file__).parent.parent / "data" / "state.json"
