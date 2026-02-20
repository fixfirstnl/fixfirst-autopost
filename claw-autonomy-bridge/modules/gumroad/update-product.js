'use strict';
const { createClient, getParams } = require('./gumroad-client');

async function updateProduct(productId, updates) {
  const client = createClient();
  const data = new URLSearchParams({ ...getParams(), ...updates }).toString();
  const res = await client.put(`/products/${productId}`, data);
  return res.data;
}

module.exports = { updateProduct };
