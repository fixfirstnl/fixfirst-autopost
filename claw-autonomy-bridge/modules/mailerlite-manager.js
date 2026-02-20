'use strict';
const express = require('express');
const router = express.Router();
const { sendBlast } = require('./mailerlite/send-blast');
const { addSubscriber, getStats } = require('./mailerlite/manage-subscribers');
const { triggerAutomation } = require('./mailerlite/automation-triggers');
const { createClient } = require('./mailerlite/mailerlite-client');

async function notifyError(label, err) {
  try {
    const { sendMessage } = require('./telegram/status-reporter');
    await sendMessage(`❌ [mailerlite-manager] ${label}: ${err.message}`);
  } catch (_) {}
}

// POST /api/mailerlite/campaign
router.post('/campaign', async (req, res) => {
  const { subject, html_content, group_ids, from_name, from_email } = req.body;
  if (!subject || !html_content) {
    return res.status(400).json({ success: false, error: 'subject and html_content are required' });
  }
  try {
    const result = await sendBlast({
      subject,
      htmlContent: html_content,
      groupIds: group_ids,
      fromName: from_name,
      fromEmail: from_email
    });
    res.json({ success: true, data: result });
  } catch (err) {
    await notifyError('campaign', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

// POST /api/mailerlite/subscriber
router.post('/subscriber', async (req, res) => {
  const { email, name, fields, groups } = req.body;
  if (!email) {
    return res.status(400).json({ success: false, error: 'email is required' });
  }
  try {
    const result = await addSubscriber({ email, name, fields, groups });
    res.json({ success: true, data: result });
  } catch (err) {
    await notifyError('subscriber', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

// GET /api/mailerlite/stats
router.get('/stats', async (req, res) => {
  try {
    const result = await getStats();
    res.json({ success: true, data: result });
  } catch (err) {
    await notifyError('stats', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

// POST /api/mailerlite/automation
router.post('/automation', async (req, res) => {
  const { automation_id, email } = req.body;
  if (!automation_id || !email) {
    return res.status(400).json({ success: false, error: 'automation_id and email are required' });
  }
  try {
    const result = await triggerAutomation({ automationId: automation_id, email });
    res.json({ success: true, data: result });
  } catch (err) {
    await notifyError('automation', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

module.exports = router;
