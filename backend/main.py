from pathlib import Path
from flask import Flask, send_from_directory
from .api import api
from .admin import admin
from .config import SECRET_KEY

FRONTEND_DIR = str(Path(__file__).parent.parent / "frontend")

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.register_blueprint(api)
app.register_blueprint(admin)


@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:path>")
def frontend(path):
    return send_from_directory(FRONTEND_DIR, path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
