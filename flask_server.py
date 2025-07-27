from flask import Flask, request, jsonify
import os

app = Flask(__name__)
images_folder = 'saved_images'
os.makedirs(images_folder, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_image():
    image_bytes = request.data
    image_id = len(os.listdir(images_folder)) + 1
    image_path = os.path.join(images_folder, f'image_{image_id}.png')
    with open(image_path, 'wb') as f:
        f.write(image_bytes)
    return jsonify({'status': 'success', 'image_id': image_id})

@app.route('/images', methods=['GET'])
def list_images():
    image_files = os.listdir(images_folder)
    return jsonify({'images': image_files})

if __name__ == '__main__':
    app.run(port=5000)