const express = require('express');
const axios = require('axios');
const app = express();

// Serve static HTML
app.get('/', async (req, res) => {
    try {
        // Fetch product from Catalog Service
        const catalogResponse = await axios.get('http://localhost:5001/api/catalog');
        const products = catalogResponse.data;

        // Fetch orders from Order Service
        const ordersResponse = await axios.get('http://localhost:5002/api/orders');
        const orders = ordersResponse.data;

        // Simple HTML response
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
        html += `</ul>`;
        res.send(html);
    } catch (error) {
        res.send(`Error: ${error.message}`);
    }
});

app.listen(3000, () => {
    console.log('Frontend running on port: 3000');
})