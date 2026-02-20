'use strict';
const { createClient, getParams } = require('./gumroad-client');

async function getSales({ productId, after, before } = {}) {
  const client = createClient();
  const params = getParams();
  if (productId) params.product_id = productId;
  if (after) params.after = after;
  if (before) params.before = before;
  const res = await client.get('/sales', { params });
  return res.data;
}

async function getRevenueSummary() {
  const data = await getSales();
  const sales = data.sales || [];
  const total = sales.reduce((sum, s) => sum + parseFloat(s.price || 0), 0);
  return { totalSales: sales.length, totalRevenue: total.toFixed(2), currency: 'USD', sales };
}

module.exports = { getSales, getRevenueSummary };
