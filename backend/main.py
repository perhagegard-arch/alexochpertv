from pathlib import Path
from flask import Flask, send_from_directory
from .api import api

FRONTEND_DIR = str(Path(__file__).parent.parent / "frontend")

app = Flask(__name__)
app.register_blueprint(api)


@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:path>")
def frontend(path):
    return send_from_directory(FRONTEND_DIR, path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
