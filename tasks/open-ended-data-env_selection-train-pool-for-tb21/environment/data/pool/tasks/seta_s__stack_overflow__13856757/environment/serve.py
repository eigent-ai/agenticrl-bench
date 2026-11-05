#!/usr/bin/env python3
"""Flask server that serves processed video thumbnails over HTTP."""
from flask import Flask, send_from_directory, abort
import os

app = Flask(__name__)

THUMBNAIL_DIR = "/app/cache"

@app.route("/thumbnail/<video_id>")
def serve_thumbnail(video_id: str):
    filename = f"{video_id}.jpg"
    filepath = os.path.join(THUMBNAIL_DIR, filename)
    if not os.path.exists(filepath):
        abort(404)
    return send_from_directory(THUMBNAIL_DIR, filename, mimetype="image/jpeg")

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
