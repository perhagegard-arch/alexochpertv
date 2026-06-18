import re
from datetime import date

MONTH_NAMES = {
    "jan": 1, "januari": 1,
    "feb": 2, "februari": 2,
    "mar": 3, "mars": 3,
    "apr": 4, "april": 4,
    "maj": 5,
    "jun": 6, "juni": 6,
    "jul": 7, "juli": 7,
    "aug": 8, "augusti": 8,
    "sep": 9, "sept": 9, "september": 9,
    "okt": 10, "oktober": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}

NUMERIC_DATE_RE = re.compile(r"^(\d{1,2})[./-](\d{1,2})(?:[./-]\d{2,4})?$")
ISO_DATE_RE = re.compile(r"^(\d{4})-(\d{1,2})-(\d{1,2})$")


def parse_birthdays(raw_text):
    entries = []
    invalid_lines = []
    for line in (raw_text or "").splitlines():
        line = line.strip()
        if not line:
            continue
        entry = _parse_line(line)
        if entry is None:
            invalid_lines.append(line)
        else:
            entries.append(entry)
    return entries, invalid_lines


def _parse_line(line):
    raw_fields = line.split("\t") if "\t" in line else line.split(",")
    fields = [f.strip() for f in raw_fields if f.strip()]
    if len(fields) < 2:
        return None

    name = fields[0]
    if len(fields) >= 3:
        month = _parse_month(fields[1])
        day = _parse_day(fields[2])
        result = (month, day) if month and day else None
    else:
        result = _parse_date_string(fields[1])

    if result is None:
        return None
    month, day = result
    return {"name": name, "month": month, "day": day}


def _parse_month(s):
    s = s.strip().lower().rstrip(".")
    if s.isdigit():
        m = int(s)
        return m if 1 <= m <= 12 else None
    return MONTH_NAMES.get(s)


def _parse_day(s):
    s = s.strip()
    if s.isdigit():
        d = int(s)
        return d if 1 <= d <= 31 else None
    return None


def _parse_date_string(s):
    s = s.strip().lower()

    m = ISO_DATE_RE.match(s)
    if m:
        _, month_s, day_s = m.groups()
        return _validate(int(month_s), int(day_s))

    m = NUMERIC_DATE_RE.match(s)
    if m:
        day_s, month_s = m.groups()
        return _validate(int(month_s), int(day_s))

    parts = s.split()
    if len(parts) == 2:
        a, b = parts
        a = a.rstrip(".")
        b = b.rstrip(".")
        if a.isdigit() and not b.isdigit():
            month = MONTH_NAMES.get(b)
            if month:
                return _validate(month, int(a))
        elif b.isdigit() and not a.isdigit():
            month = MONTH_NAMES.get(a)
            if month:
                return _validate(month, int(b))

    return None


def _validate(month, day):
    if 1 <= month <= 12 and 1 <= day <= 31:
        return month, day
    return None


def _next_occurrence(month, day, today):
    for year in (today.year, today.year + 1):
        try:
            occ = date(year, month, day)
        except ValueError:
            if (month, day) != (2, 29):
                return None
            occ = date(year, 3, 1)
        if occ >= today:
            return occ
    return None


def _label(days_until):
    if days_until == 0:
        return "Idag"
    if days_until == 1:
        return "Imorgon"
    return f"Om {days_until} dagar"


def upcoming_within(entries, today, window_days=5):
    results = []
    for entry in entries:
        occ = _next_occurrence(entry["month"], entry["day"], today)
        if occ is None:
            continue
        days_until = (occ - today).days
        if 0 <= days_until <= window_days:
            results.append({
                "name": entry["name"],
                "month": entry["month"],
                "day": entry["day"],
                "days_until": days_until,
                "label": _label(days_until),
            })
    results.sort(key=lambda e: (e["days_until"], e["name"]))
    return results


def birthdays_today(entries, today):
    return [e["name"] for e in entries if e["month"] == today.month and e["day"] == today.day]
