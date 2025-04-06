from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory order list (to be replaced with MongoDB later)
orders = [
    {"id": 1, "product_id": 1, "quantity": 2, "total": 1999.98},
    {"id": 2, "product_id": 2, "quantity": 1, "total": 499.99}
]

@app.route('/api/orders', methods=['GET'])
def get_orders():
    return jsonify(orders)

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    if not data or 'product_id' not in data or 'quantity' not in data:
        return jsonify({"error": "Missing product_id or quantity"}), 400
    new_order = {
        "id": len(orders) + 1,
        "product_id": data['product_id'],
        "quantity": data['quantity'],
        "total": data['quantity'] * 999.99  # Dummy price, will integrate with catalog later
    }
    orders.append(new_order)
    return jsonify(new_order), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)