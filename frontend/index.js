const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const app = express();

// Middleware to parse form data
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// Serve the main page with form
app.get('/', async (req, res) => {
    try {
        const catalogResponse = await axios.get('http://localhost:5001/api/catalog');
        const products = catalogResponse.data;
        const ordersResponse = await axios.get('http://localhost:5002/api/orders');
        const orders = ordersResponse.data;

        let html = `
            <h1>E-commerce App</h1>
            <h2>Products</h2>
            <ul>`;
        products.forEach(p => {
            html += `<li>${p.name} - $${p.price}</li>`;
        });
        html += `</ul>
            <h2>Orders</h2>
            <ul>`;
        orders.forEach(o => {
            html += `<li>Order #${o.id} - Product ID: ${o.product_id}, Qty: ${o.quantity}, Total: $${o.total}</li>`;
        });
        html += `</ul>
            <h2>Create Order</h2>
            <form action="/create-order" method="POST">
                <label>Product ID: <input type="number" name="product_id" required></label>
                <label>Quantity: <input type="number" name="quantity" required></label>
                <button type="submit">Submit Order</button>
            </form>`;
        res.send(html);
    } catch (error) {
        res.send(`Error: ${error.message}`);
    }
});

// Handle order creation
app.post('/create-order', async (req, res) => {
    try {
        const { product_id, quantity } = req.body;
        const orderResponse = await axios.post('http://localhost:5002/api/orders', {
            product_id: parseInt(product_id),
            quantity: parseInt(quantity)
        });
        res.redirect('/');
    } catch (error) {
        res.send(`Error creating order: ${error.message}`);
    }
});

app.listen(3000, () => {
    console.log('Frontend running on port 3000');
});