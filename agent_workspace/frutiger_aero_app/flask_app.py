from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for example purposes
data_store = []

@app.route('/create', methods=['POST'])
def create_item():
    item = request.json.get('item')
    data_store.append(item)
    return jsonify({'message': 'Item created', 'item': item}), 201

@app.route('/read', methods=['GET'])
def read_items():
    return jsonify({'items': data_store}), 200

@app.route('/update/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    new_item = request.json.get('item')
    if 0 <= item_id < len(data_store):
        data_store[item_id] = new_item
        return jsonify({'message': 'Item updated', 'item': new_item}), 200
    return jsonify({'message': 'Item not found'}), 404

@app.route('/delete/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    if 0 <= item_id < len(data_store):
        removed_item = data_store.pop(item_id)
        return jsonify({'message': 'Item deleted', 'item': removed_item}), 200
    return jsonify({'message': 'Item not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)