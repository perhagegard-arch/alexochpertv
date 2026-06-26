from datetime import date
from ..birthdays import parse_birthdays, upcoming_within
from ..config import BIRTHDAY_WINDOW_DAYS


class BirthdayProvider:
    def __init__(self, store):
        self.store = store

    def get(self):
        entries, _ = parse_birthdays(self.store.get_birthdays_raw())
        upcoming = upcoming_within(entries, date.today(), window_days=BIRTHDAY_WINDOW_DAYS)
        return {"upcoming": upcoming}
