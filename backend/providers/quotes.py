import requests
from ..config import QUOTES_API_URL


class QuoteProvider:
    def get(self, ignore_id=None):
        params = {"ignore": ignore_id} if ignore_id is not None else {}
        resp = requests.get(QUOTES_API_URL, params=params, timeout=5)
        resp.raise_for_status()
        return resp.json()
