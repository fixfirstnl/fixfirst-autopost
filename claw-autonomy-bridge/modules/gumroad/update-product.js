'use strict';
const { createClient, getParams } = require('./gumroad-client');
const qs = require('querystring');

async function updateProduct(productId, updates) {
  const client = createClient();
  const data = qs.stringify({ ...getParams(), ...updates });
  const res = await client.put(`/products/${productId}`, data);
  return res.data;
}

module.exports = { updateProduct };
