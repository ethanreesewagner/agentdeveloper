from flask import Flask, send_from_directory, jsonify
import os

app = Flask(__name__)

# Directory to save sketches
SKETCH_DIR = "sketches"
os.makedirs(SKETCH_DIR, exist_ok=True)

@app.route('/')
def index():
    return f'Hello, visit /sketches to view saved sketches.'

@app.route('/sketches')
def list_sketches():
    sketches = os.listdir(SKETCH_DIR)
    return jsonify(sketches)

@app.route('/sketches/<filename>')
def get_sketch(filename):
    return send_from_directory(SKETCH_DIR, filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)