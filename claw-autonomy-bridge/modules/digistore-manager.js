'use strict';
const express = require('express');
const router = express.Router();
const { getConversionStats } = require('./digistore24/commission-tracker');
const { createClient } = require('./digistore24/digistore-client');

async function notifyError(label, err) {
  try {
    const { sendMessage } = require('./telegram/status-reporter');
    await sendMessage(`❌ [digistore-manager] ${label}: ${err.message}`);
  } catch (_) {}
}

// POST /api/digistore/product
router.post('/product', async (req, res) => {
  const { product_name, price, description, category } = req.body;
  if (!product_name || price === undefined) {
    return res.status(400).json({ success: false, error: 'product_name and price are required' });
  }
  try {
    const client = createClient();
    const result = await client.post('/addProduct/1/en', {
      name: product_name,
      price,
      description: description || '',
      category: category || 'digital'
    });
    res.json({ success: true, data: result.data });
  } catch (err) {
    await notifyError('create-product', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

// GET /api/digistore/stats
router.get('/stats', async (req, res) => {
  try {
    const result = await getConversionStats();
    res.json({ success: true, data: result });
  } catch (err) {
    await notifyError('stats', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

module.exports = router;
