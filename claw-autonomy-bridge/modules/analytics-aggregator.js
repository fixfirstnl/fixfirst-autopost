'use strict';
const express = require('express');
const router = express.Router();
const { getUnifiedDashboard } = require('./analytics/unified-dashboard');
const { getRevenueReport } = require('./analytics/revenue-tracker');
const { getContentPerformance } = require('./analytics/content-performance');
const { getAccountAnalytics } = require('./tiktok/analytics');

async function notifyError(label, err) {
  try {
    const { sendMessage } = require('./telegram/status-reporter');
    await sendMessage(`❌ [analytics-aggregator] ${label}: ${err.message}`);
  } catch (_) {}
}

// GET /api/analytics/dashboard
router.get('/dashboard', async (req, res) => {
  try {
    const result = await getUnifiedDashboard();
    res.json({ success: true, data: result });
  } catch (err) {
    await notifyError('dashboard', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

// GET /api/analytics/revenue
router.get('/revenue', async (req, res) => {
  try {
    const result = await getRevenueReport();
    res.json({ success: true, data: result });
  } catch (err) {
    await notifyError('revenue', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

// GET /api/analytics/engagement
router.get('/engagement', async (req, res) => {
  try {
    const videoIds = req.query.ids ? req.query.ids.split(',') : [];
    const [tiktokAccount, contentPerf] = await Promise.allSettled([
      getAccountAnalytics(),
      getContentPerformance(videoIds)
    ]);
    res.json({
      success: true,
      data: {
        tiktok: tiktokAccount.status === 'fulfilled' ? tiktokAccount.value : { error: tiktokAccount.reason.message },
        content: contentPerf.status === 'fulfilled' ? contentPerf.value : { error: contentPerf.reason.message },
        timestamp: new Date().toISOString()
      }
    });
  } catch (err) {
    await notifyError('engagement', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

// GET /api/analytics/report
router.get('/report', async (req, res) => {
  try {
    const [revenue, dashboard] = await Promise.all([getRevenueReport(), getUnifiedDashboard()]);
    const report = {
      period: req.query.period || 'daily',
      revenue,
      dashboard,
      generated_at: new Date().toISOString()
    };
    try {
      const { sendReport } = require('./telegram/status-reporter');
      await sendReport({
        title: `📊 FixFirst ${report.period} Report`,
        body: `Gumroad: €${(revenue.gumroad || {}).revenue || 0} (${(revenue.gumroad || {}).sales || 0} sales)\nDigistore24: €${(revenue.digistore24 || {}).revenue || 0}\nTotal: €${(revenue.total || {}).revenue || 0}`
      });
    } catch (_) {}
    res.json({ success: true, data: report });
  } catch (err) {
    await notifyError('report', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

module.exports = router;
