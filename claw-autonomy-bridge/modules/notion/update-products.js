'use strict';
const { createClient } = require('./notion-client');

async function updateProduct(pageId, updates) {
  const client = createClient();
  const properties = {};
  if (updates.status) properties['Status'] = { select: { name: updates.status } };
  if (updates.price) properties['Price'] = { number: updates.price };
  if (updates.revenue) properties['Revenue'] = { number: updates.revenue };
  const res = await client.patch(`/pages/${pageId}`, { properties });
  return res.data;
}

module.exports = { updateProduct };
