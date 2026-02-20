'use strict';
const { createClient, getParams } = require('./gumroad-client');
const qs = require('querystring');

async function createCoupon({ productId, name, amountOff, offerType = 'percent', maxPurchaseCount }) {
  const client = createClient();
  const params = getParams({ product_id: productId, name, amount_off: amountOff, offer_type: offerType });
  if (maxPurchaseCount) params.max_purchase_count = maxPurchaseCount;
  const res = await client.post('/offer_codes', qs.stringify(params));
  return res.data;
}

module.exports = { createCoupon };
