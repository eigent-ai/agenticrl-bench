import sys
sys.path.insert(0, '/app')
sys.path.insert(0, '/app/libs')

from flask import Flask, jsonify, request
from .routes import api_blueprint

app = Flask(__name__)


@app.route('/health')
def health():
    return jsonify({"status": "ok"})


app.register_blueprint(api_blueprint)


def create_app():
    return app


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
