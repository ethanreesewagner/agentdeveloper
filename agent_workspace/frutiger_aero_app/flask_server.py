from flask import Flask, jsonify, request

app = Flask(__name__)

items = {}

@app.route('/create', methods=['POST'])
def create_item():
    try:
        data = request.json
        item_id = len(items) + 1
        items[item_id] = data.get('name', 'Unnamed')
        return jsonify({'message': 'Item created', 'id': item_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/read', methods=['GET'])
def read_items():
    try:
        return jsonify({'items': items})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/update/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    try:
        if item_id in items:
            data = request.json
            items[item_id] = data.get('name', items[item_id])
            return jsonify({'message': 'Item updated'})
        else:
            return jsonify({'error': 'Item not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/delete/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        if item_id in items:
            del items[item_id]
            return jsonify({'message': 'Item deleted'})
        else:
            return jsonify({'error': 'Item not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(port=5000)
