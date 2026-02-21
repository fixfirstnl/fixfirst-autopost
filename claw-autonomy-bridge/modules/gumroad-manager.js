'use strict';
const express = require('express');
const router = express.Router();
const { listProducts, getProduct } = require('./gumroad/manage-products');
const { updateProduct } = require('./gumroad/update-product');
const { getSales } = require('./gumroad/sales-analytics');
const { createClient, getParams } = require('./gumroad/gumroad-client');

async function notifyError(label, err) {
  try {
    const { sendMessage } = require('./telegram/status-reporter');
    await sendMessage(`❌ [gumroad-manager] ${label}: ${err.message}`);
  } catch (_) {}
}

// POST /api/gumroad/product
router.post('/product', async (req, res) => {
  const { name, description, price, file_url, preview_url } = req.body;
  if (!name || price === undefined) {
    return res.status(400).json({ success: false, error: 'name and price are required' });
  }
  try {
    const client = createClient();
    const params = getParams({ name, description, price, url: file_url, preview_url });
    const result = await client.post('/products', new URLSearchParams(params).toString());
    res.json({ success: true, data: result.data });
  } catch (err) {
    await notifyError('create-product', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

// PATCH /api/gumroad/product/:id
router.patch('/product/:id', async (req, res) => {
  try {
    const result = await updateProduct(req.params.id, req.body);
    res.json({ success: true, data: result });
  } catch (err) {
    await notifyError('update-product', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

// GET /api/gumroad/sales
router.get('/sales', async (req, res) => {
  try {
    const result = await getSales(req.query);
    res.json({ success: true, data: result });
  } catch (err) {
    await notifyError('sales', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

module.exports = router;
