from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/api/status')
def status():
    return jsonify({"status": "ok", "version": "1.4.2", "tls": "enabled"})


@app.route('/health')
def health():
    return jsonify({"healthy": True})
