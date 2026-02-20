'use strict';
const cron = require('node-cron');

let schedulerStarted = false;

function start() {
  if (schedulerStarted) return;
  schedulerStarted = true;

  // Daily routine at 08:00
  cron.schedule('0 8 * * *', async () => {
    const { runDailyRoutine } = require('./auto-poster');
    try {
      if (typeof runDailyRoutine === 'function') await runDailyRoutine();
    } catch (err) {
      console.error('[scheduler] daily-routine error:', err.message);
    }
  }, { timezone: 'Europe/Amsterdam' });

  // Health check every 30 minutes
  cron.schedule('*/30 * * * *', async () => {
    const { checkHealth } = require('./health-monitor');
    try {
      await checkHealth();
    } catch (err) {
      console.error('[scheduler] health-check error:', err.message);
    }
  });

  console.log('[scheduler] Started cron jobs');
}

module.exports = { start };
