from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/data')
def get_data():
    return jsonify({"status": "ok", "data": [1, 2, 3]})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
