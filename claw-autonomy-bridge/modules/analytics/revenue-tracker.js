'use strict';
const { getUnifiedDashboard } = require('./unified-dashboard');

async function getRevenueReport() {
  const dashboard = await getUnifiedDashboard();
  const gumroadRevenue = parseFloat(dashboard.gumroad.totalRevenue || 0);
  const digistoreRevenue = parseFloat(dashboard.digistore24.revenue || 0);
  const totalRevenue = (gumroadRevenue + digistoreRevenue).toFixed(2);

  return {
    gumroad: { revenue: gumroadRevenue, sales: dashboard.gumroad.totalSales },
    digistore24: { revenue: digistoreRevenue, conversions: dashboard.digistore24.total },
    total: { revenue: totalRevenue },
    timestamp: dashboard.timestamp
  };
}

module.exports = { getRevenueReport };
