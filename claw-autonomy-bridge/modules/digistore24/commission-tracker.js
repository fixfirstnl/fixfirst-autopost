'use strict';
const { createClient } = require('./digistore-client');

async function getCommissions({ from, to } = {}) {
  const client = createClient();
  const params = {};
  if (from) params.from_date = from;
  if (to) params.to_date = to;
  const res = await client.get('/listTransactions/1/en', { params });
  return res.data;
}

async function getConversionStats() {
  const client = createClient();
  const res = await client.get('/listTransactions/1/en');
  const data = res.data;
  const transactions = data.data ? data.data.transactions : [];
  const total = transactions.length;
  const revenue = transactions.reduce((s, t) => s + parseFloat(t.earnings_eur || 0), 0);
  return { total, revenue: revenue.toFixed(2), currency: 'EUR', transactions };
}

module.exports = { getCommissions, getConversionStats };
