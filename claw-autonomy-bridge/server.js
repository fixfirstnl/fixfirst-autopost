'use strict';
require('dotenv').config();
const express = require('express');
const app = express();

const PORT = parseInt(process.env.PORT || '3006', 10);

app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));

const apiRoutes = require('./routes/api');
app.use('/api', apiRoutes);

const healthRouter = require('./health');
app.use(healthRouter);

// Extended autonomy modules
app.use('/api/later', require('./modules/later-scheduler'));
app.use('/api/tiktok', require('./modules/tiktok-poster'));
app.use('/api/instagram', require('./modules/instagram-poster'));
app.use('/api/youtube', require('./modules/youtube-uploader'));
app.use('/api/pinterest', require('./modules/pinterest-pinner'));
app.use('/api/gumroad', require('./modules/gumroad-manager'));
app.use('/api/digistore', require('./modules/digistore-manager'));
app.use('/api/notion', require('./modules/notion-sync'));
app.use('/api/mailerlite', require('./modules/mailerlite-manager'));
app.use('/api/analytics', require('./modules/analytics-aggregator'));
app.use('/api/queue', require('./modules/content-queue'));
app.use('/api/cron', require('./modules/cron-scheduler'));

const { checkHealth, getLastHealth } = require('./orchestrator/health-monitor');
const { getStatus } = require('./orchestrator/task-queue');

app.get('/api/health', async (req, res) => {
  const health = getLastHealth();
  const queue = getStatus();
  res.json({
    status: 'ok',
    service: 'claw-autonomy-bridge',
    port: PORT,
    uptime: process.uptime(),
    health,
    queue,
    timestamp: new Date().toISOString()
  });
});

app.listen(PORT, () => {
  console.log(`[claw-autonomy-bridge] Running on port ${PORT}`);

  const scheduler = require('./orchestrator/scheduler');
  scheduler.start();

  const { startCronJobs } = require('./modules/cron-scheduler');
  startCronJobs();

  checkHealth().catch(err => console.error('[health] Initial check failed:', err.message));
});

module.exports = app;
