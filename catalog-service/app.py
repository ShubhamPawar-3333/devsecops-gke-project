from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Use your Atlas connection string
connection_string = 'mongodb+srv://shubhamdpawar3333:PROdYeLHrcSmO3Ec@cluster0.pxoxxui.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(connection_string)
db = client['ecommerce']
products_collection = db['products']

# Seed initial data (run once, then comment out after first run)
if products_collection.count_documents({}) == 0:
    products_collection.insert_many([
        {"id": 1, "name": "Laptop", "price": 999.99},
        {"id": 2, "name": "Phone", "price": 499.99},
        {"id": 3, "name": "Headphones", "price": 59.99}
    ])

# # In-memory product catalog (to be replaced with MongoDB later)
# products = [
#     {"id": 1, "name": "Laptop", "price": 999.99},
#     {"id": 2, "name": "Phone", "price": 499.99},
#     {"id": 3, "name": "Headphones", "price": 59.99}
# ]

@app.route('/api/catalog', methods=['GET'])
def get_products():
    products = list(products_collection.find({}, {'_id': 0}))
    return jsonify(products)

@app.route('/api/catalog/<int:product_id>', methods=['GET'])
def get_product(product_id):
    # product = next((p for p in products if p["id"] == product_id), None)
    product = products_collection.find_one({"id": product_id}, {'_id': 0})
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)