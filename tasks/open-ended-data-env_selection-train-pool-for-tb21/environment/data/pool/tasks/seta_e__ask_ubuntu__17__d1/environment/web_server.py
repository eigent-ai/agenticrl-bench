from flask import Flask
import signal
import sys
import time

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/health')
def health():
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
