'use strict';

function generateAffiliateLink({ productId, campaignKey = 'fixfirst' }) {
  const affiliateId = process.env.DIGISTORE24_AFFILIATE_ID;
  const link = `https://www.digistore24.com/redir/${productId}/${affiliateId}/${campaignKey}`;
  return { productId, affiliateId, campaignKey, link };
}

async function generateMultipleLinks(products) {
  return products.map(p => generateAffiliateLink(p));
}

module.exports = { generateAffiliateLink, generateMultipleLinks };
