'use strict';
const { getRevenueSummary } = require('../gumroad/sales-analytics');
const { getConversionStats } = require('../digistore24/commission-tracker');

async function getUnifiedDashboard() {
  const [gumroad, digistore] = await Promise.allSettled([
    getRevenueSummary(),
    getConversionStats()
  ]);

  return {
    gumroad: gumroad.status === 'fulfilled' ? gumroad.value : { error: gumroad.reason.message },
    digistore24: digistore.status === 'fulfilled' ? digistore.value : { error: digistore.reason.message },
    timestamp: new Date().toISOString()
  };
}

module.exports = { getUnifiedDashboard };
