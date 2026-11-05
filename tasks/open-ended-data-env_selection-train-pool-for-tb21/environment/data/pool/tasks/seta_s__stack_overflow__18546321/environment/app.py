import pkg_resources
from flask import Flask, jsonify
import requests
import yaml

app = Flask(__name__)

@app.route('/health')
def health():
    versions = {
        'flask': pkg_resources.get_distribution('flask').version,
        'requests': requests.__version__,
        'pyyaml': yaml.__version__,
    }
    return jsonify(status='ok', versions=versions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
