'use strict';
const { createClient } = require('./digistore-client');

async function getProductCatalog() {
  const client = createClient();
  const res = await client.get('/listAffiliateProducts/1/en');
  return res.data;
}

module.exports = { getProductCatalog };
