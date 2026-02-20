'use strict';
const { Router } = require('express');

const router = Router();

router.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    service: 'claw-autonomy-bridge',
    uptime: process.uptime(),
    timestamp: new Date().toISOString()
  });
});

module.exports = router;
