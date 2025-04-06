from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Use your Atlas connection string
# Use your Atlas connection string
connection_string = 'mongodb+srv://shubhamdpawar3333:PROdYeLHrcSmO3Ec@cluster0.pxoxxui.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(connection_string)
db = client['ecommerce']
orders_collection = db['orders']

# Seed initial data (run once, then comment out after first run)
if orders_collection.count_documents({}) == 0:
    orders_collection.insert_many([
        {"id": 1, "product_id": 1, "quantity": 2, "total": 1999.98},
        {"id": 2, "product_id": 2, "quantity": 1, "total": 499.99}
    ])

# # In-memory order list (to be replaced with MongoDB later)
# orders = [
#     {"id": 1, "product_id": 1, "quantity": 2, "total": 1999.98},
#     {"id": 2, "product_id": 2, "quantity": 1, "total": 499.99}
# ]

@app.route('/api/orders', methods=['GET'])
def get_orders():
    orders = list(orders_collection.find({}, {'_id': 0}))
    return jsonify(orders)

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    if not data or 'product_id' not in data or 'quantity' not in data:
        return jsonify({"error": "Missing product_id or quantity"}), 400
    new_order = {
        "id": orders_collection.count_documents({}) + 1,
        "product_id": data['product_id'],
        "quantity": data['quantity'],
        "total": data['quantity'] * 999.99  # Dummy price, will integrate with catalog later
    }
    orders_collection.insert_one(new_order)
    new_order.pop('_id')  # Remove MongoDB's _id field for cleaner response
    return jsonify(new_order), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)