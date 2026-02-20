'use strict';
const { createClient, getParams } = require('./gumroad-client');

async function listProducts() {
  const client = createClient();
  const res = await client.get('/products', { params: getParams() });
  return res.data;
}

async function getProduct(productId) {
  const client = createClient();
  const res = await client.get(`/products/${productId}`, { params: getParams() });
  return res.data;
}

module.exports = { listProducts, getProduct };
