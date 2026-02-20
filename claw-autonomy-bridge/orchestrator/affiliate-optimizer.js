'use strict';
const { getProductCatalog } = require('../modules/digistore24/product-catalog');
const { generateMultipleLinks } = require('../modules/digistore24/affiliate-links');
const { bulkCreatePins } = require('../modules/pinterest/bulk-pin');
const { sendBlast } = require('../modules/mailerlite/send-blast');
const { sendMessage } = require('../modules/telegram/status-reporter');

const PRODUCTS = [
  { productId: 'no-grid-survival', name: 'No Grid Survival' },
  { productId: 'off-grid-generator', name: 'OFF-GRID Generator' },
  { productId: 'woodwork101', name: 'Woodwork101' }
];

async function runAffiliatePush({ imageUrl = '' } = {}) {
  let catalog;
  try {
    catalog = await getProductCatalog();
  } catch {
    catalog = { products: PRODUCTS };
  }

  const products = (catalog.data || PRODUCTS).slice(0, 3);
  const links = await generateMultipleLinks(products.map(p => ({ productId: p.productId || p.product_id || p.id })));

  const pins = links.map((l, i) => ({
    title: products[i].name || `Product ${i + 1}`,
    description: `Get ${products[i].name} now! Best deal available. ${l.link}`,
    imageUrl: imageUrl || `https://via.placeholder.com/800x1200?text=${encodeURIComponent(products[i].name || 'Product')}`,
    link: l.link
  }));

  const pinsResult = await bulkCreatePins(Array.from({ length: 30 }, (_, i) => pins[i % pins.length]));

  const emailHtml = `<h1>Top 3 FixFirst Deals</h1>${links.map((l, i) => `<p><a href="${l.link}">${products[i].name || 'Product'}</a></p>`).join('')}`;
  let blastResult;
  try {
    blastResult = await sendBlast({ subject: '🔥 Top 3 FixFirst Deals Today', htmlContent: emailHtml });
  } catch (err) {
    blastResult = { error: err.message };
  }

  await sendMessage(`🚀 Affiliate push: ${pinsResult.succeeded} pins created, email blast sent`).catch(() => {});

  return { links, pins: pinsResult, emailBlast: blastResult };
}

module.exports = { runAffiliatePush };
