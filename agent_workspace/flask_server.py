from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Directory to save sketches
SAVE_DIR = "sketches"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

@app.route('/save_sketch', methods=['POST'])
def save_sketch():
    try:
        # Get the image data from the request
        image_data = request.json.get('image_data')
        image_name = request.json.get('image_name', 'sketch.png')
        
        # Save the image data to a file
        image_path = os.path.join(SAVE_DIR, image_name)
        with open(image_path, 'w') as f:
            f.write(image_data)
        
        return jsonify({'status': 'success', 'message': f'Sketch saved as {image_name}'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)