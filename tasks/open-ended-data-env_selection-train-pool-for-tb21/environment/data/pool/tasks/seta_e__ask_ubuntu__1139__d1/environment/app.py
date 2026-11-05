from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/api/info")
def info():
    return jsonify({"service": "flask-backend", "version": "1.0"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
