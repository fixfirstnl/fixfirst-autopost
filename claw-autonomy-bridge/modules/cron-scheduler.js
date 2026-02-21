'use strict';
const express = require('express');
const router = express.Router();
const cron = require('node-cron');
const axios = require('axios');

let cronStarted = false;
const jobs = [];

function startCronJobs() {
  if (cronStarted) return;
  cronStarted = true;

  // Auto-check content queue every 30 minutes
  jobs.push(cron.schedule('*/30 * * * *', async () => {
    try {
      const port = process.env.PORT || 3006;
      await axios.post(`http://localhost:${port}/api/queue/process`);
      console.log('[cron-scheduler] Queue processed');
    } catch (err) {
      console.error('[cron-scheduler] queue-process error:', err.message);
      try {
        const { sendMessage } = require('./telegram/status-reporter');
        await sendMessage(`❌ [cron-scheduler] queue-process: ${err.message}`);
      } catch (_) {}
    }
  }));

  // Daily analytics report at 23:00
  jobs.push(cron.schedule('0 23 * * *', async () => {
    try {
      const port = process.env.PORT || 3006;
      await axios.get(`http://localhost:${port}/api/analytics/report?period=daily`);
      console.log('[cron-scheduler] Daily analytics report generated');
    } catch (err) {
      console.error('[cron-scheduler] analytics-report error:', err.message);
      try {
        const { sendMessage } = require('./telegram/status-reporter');
        await sendMessage(`❌ [cron-scheduler] analytics-report: ${err.message}`);
      } catch (_) {}
    }
  }, { timezone: 'Europe/Amsterdam' }));

  // Weekly content calendar sync from Notion (every Monday at 07:00)
  jobs.push(cron.schedule('0 7 * * 1', async () => {
    try {
      const port = process.env.PORT || 3006;
      const res = await axios.get(`http://localhost:${port}/api/notion/content-calendar`);
      const items = res.data.data || [];
      console.log(`[cron-scheduler] Weekly Notion sync: ${items.length} calendar items loaded`);
    } catch (err) {
      console.error('[cron-scheduler] notion-sync error:', err.message);
      try {
        const { sendMessage } = require('./telegram/status-reporter');
        await sendMessage(`❌ [cron-scheduler] notion-sync: ${err.message}`);
      } catch (_) {}
    }
  }, { timezone: 'Europe/Amsterdam' }));

  console.log('[cron-scheduler] Extended cron jobs started');
}

// GET /api/cron/status – internal status endpoint
router.get('/status', (req, res) => {
  res.json({
    success: true,
    data: {
      started: cronStarted,
      jobs: jobs.length,
      description: [
        'Queue processing: every 30 minutes',
        'Daily analytics report: 23:00 Amsterdam',
        'Weekly Notion calendar sync: Monday 07:00 Amsterdam'
      ]
    }
  });
});

// POST /api/cron/start – internal endpoint to (re)start cron jobs
router.post('/start', (req, res) => {
  startCronJobs();
  res.json({ success: true, message: 'Cron jobs started', jobs: jobs.length });
});

module.exports = router;
module.exports.startCronJobs = startCronJobs;

