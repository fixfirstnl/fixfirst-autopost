'use strict';
require('dotenv').config();
const express = require('express');
const app = express();

const PORT = parseInt(process.env.PORT || '3006', 10);

app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));

const apiRoutes = require('./routes/api');
app.use('/api', apiRoutes);

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

  checkHealth().catch(err => console.error('[health] Initial check failed:', err.message));
});

module.exports = app;
