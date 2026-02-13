from flask import Flask
import os
import threading

app = Flask(__name__)

@app.route('/')
def health():
    return "Bot is running", 200

def run_server():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    run_server()
