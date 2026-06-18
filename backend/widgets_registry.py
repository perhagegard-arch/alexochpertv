WIDGET_ORDER = ["quote", "weather", "birthday"]

WIDGETS = {
    "quote": {"label": "Citat", "editable": False},
    "weather": {"label": "Väder", "editable": False},
    "birthday": {"label": "Födelsedagar", "editable": True},
}

ZONES = {
    "left-top": "Vänster topp",
    "left-bottom": "Vänster botten",
    "right-top": "Höger topp",
    "right-bottom": "Höger botten",
}
ZONE_IDS = list(ZONES.keys())
