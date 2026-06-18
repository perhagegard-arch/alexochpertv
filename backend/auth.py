import hmac
from functools import wraps
from flask import session, jsonify
from .config import ADMIN_PASSWORD


def check_password(password):
    return hmac.compare_digest(password or "", ADMIN_PASSWORD)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("logged_in"):
            return jsonify({"error": "Inte inloggad"}), 401
        return view(*args, **kwargs)

    return wrapped
