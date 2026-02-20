'use strict';
const express = require('express');
const router = express.Router();
const { createClient } = require('./notion/notion-client');
const { getContentQueue, updateContentHubItem } = require('./notion/update-content-hub');

async function notifyError(label, err) {
  try {
    const { sendMessage } = require('./telegram/status-reporter');
    await sendMessage(`❌ [notion-sync] ${label}: ${err.message}`);
  } catch (_) {}
}

// POST /api/notion/log
router.post('/log', async (req, res) => {
  const { action, platform, status, details } = req.body;
  if (!action) {
    return res.status(400).json({ success: false, error: 'action is required' });
  }
  try {
    const client = createClient();
    const dbId = process.env.NOTION_TASKS_DB;
    const result = await client.post('/pages', {
      parent: { database_id: dbId },
      properties: {
        Name: { title: [{ text: { content: action } }] },
        Platform: { rich_text: [{ text: { content: platform || '' } }] },
        Status: { select: { name: status || 'Logged' } },
        Details: { rich_text: [{ text: { content: details || '' } }] },
        'Logged At': { date: { start: new Date().toISOString() } }
      }
    });
    res.json({ success: true, data: result.data });
  } catch (err) {
    await notifyError('log', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

// GET /api/notion/content-calendar
router.get('/content-calendar', async (req, res) => {
  try {
    const result = await getContentQueue();
    res.json({ success: true, data: result });
  } catch (err) {
    await notifyError('content-calendar', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

// PATCH /api/notion/update/:page_id
router.patch('/update/:page_id', async (req, res) => {
  try {
    const result = await updateContentHubItem(req.params.page_id, req.body);
    res.json({ success: true, data: result });
  } catch (err) {
    await notifyError('update', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

// POST /api/notion/create-page
router.post('/create-page', async (req, res) => {
  const { database_id, properties } = req.body;
  if (!database_id || !properties) {
    return res.status(400).json({ success: false, error: 'database_id and properties are required' });
  }
  try {
    const client = createClient();
    const result = await client.post('/pages', {
      parent: { database_id },
      properties
    });
    res.json({ success: true, data: result.data });
  } catch (err) {
    await notifyError('create-page', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

module.exports = router;
