from datetime import date
from pathlib import Path
from flask import Blueprint, jsonify, request, session, send_from_directory
from .auth import check_password, login_required
from .store import JsonStore
from .widgets_registry import WIDGETS, WIDGET_ORDER, ZONES
from .birthdays import parse_birthdays, birthdays_today

admin = Blueprint("admin", __name__)

FRONTEND_DIR = str(Path(__file__).parent.parent / "frontend")

_store = JsonStore()


@admin.route("/admin")
def admin_page():
    return send_from_directory(FRONTEND_DIR, "admin.html")


@admin.route("/admin/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    if check_password(data.get("password")):
        session["logged_in"] = True
        return jsonify({"ok": True})
    return jsonify({"error": "Fel lösenord"}), 401


@admin.route("/admin/api/logout", methods=["POST"])
def logout():
    session.pop("logged_in", None)
    return jsonify({"ok": True})


@admin.route("/admin/api/session")
def session_status():
    return jsonify({"logged_in": bool(session.get("logged_in"))})


@admin.route("/admin/api/widgets")
@login_required
def list_widgets():
    states = _store.get_widget_states()
    result = [
        {
            "id": widget_type,
            "label": WIDGETS[widget_type]["label"],
            "editable": WIDGETS[widget_type]["editable"],
            "enabled": states.get(widget_type, True),
        }
        for widget_type in WIDGET_ORDER
    ]
    return jsonify(result)


@admin.route("/admin/api/widgets/<widget_id>/toggle", methods=["POST"])
@login_required
def toggle_widget(widget_id):
    if widget_id not in WIDGETS:
        return jsonify({"error": "Okänd widget"}), 404
    data = request.get_json(silent=True) or {}
    _store.set_widget_enabled(widget_id, bool(data.get("enabled")))
    return jsonify({"ok": True})


@admin.route("/admin/api/zones")
@login_required
def list_zones():
    current = _store.get_zones()
    result = [
        {"id": zone_id, "label": label, "widget": current.get(zone_id)}
        for zone_id, label in ZONES.items()
    ]
    return jsonify(result)


@admin.route("/admin/api/zones/<zone_id>", methods=["POST"])
@login_required
def set_zone(zone_id):
    if zone_id not in ZONES:
        return jsonify({"error": "Okänd zon"}), 404
    data = request.get_json(silent=True) or {}
    widget = data.get("widget") or None
    if widget is not None and widget not in WIDGETS:
        return jsonify({"error": "Okänd widget"}), 400
    _store.set_zone(zone_id, widget)
    return jsonify({"ok": True})


@admin.route("/admin/api/birthdays", methods=["GET"])
@login_required
def get_birthdays():
    return jsonify({"raw": _store.get_birthdays_raw()})


@admin.route("/admin/api/birthdays", methods=["POST"])
@login_required
def save_birthdays():
    data = request.get_json(silent=True) or {}
    raw = data.get("raw", "")
    _store.set_birthdays_raw(raw)

    entries, invalid_lines = parse_birthdays(raw)
    today_names = birthdays_today(entries, date.today())
    return jsonify({
        "count": len(entries),
        "today": today_names,
        "invalid": invalid_lines,
    })
