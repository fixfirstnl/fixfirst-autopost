'use strict';
const express = require('express');
const router = express.Router();
const fs = require('fs');
const path = require('path');
const { v4: uuidv4 } = require('uuid');

const QUEUE_FILE = path.join(__dirname, '..', 'data', 'content-queue.json');

function loadQueue() {
  try {
    const dir = path.dirname(QUEUE_FILE);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    if (!fs.existsSync(QUEUE_FILE)) return [];
    return JSON.parse(fs.readFileSync(QUEUE_FILE, 'utf8'));
  } catch (err) {
    console.error('[content-queue] Failed to load queue:', err.message);
    return [];
  }
}

function saveQueue(queue) {
  const dir = path.dirname(QUEUE_FILE);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(QUEUE_FILE, JSON.stringify(queue, null, 2), 'utf8');
}

async function notifyError(label, err) {
  try {
    const { sendMessage } = require('./telegram/status-reporter');
    await sendMessage(`❌ [content-queue] ${label}: ${err.message}`);
  } catch (_) {}
}

// POST /api/queue/add
router.post('/add', (req, res) => {
  const { platform, content_type, payload, priority } = req.body;
  if (!platform || !payload) {
    return res.status(400).json({ success: false, error: 'platform and payload are required' });
  }
  try {
    const queue = loadQueue();
    const item = {
      id: uuidv4(),
      platform,
      content_type: content_type || 'post',
      payload,
      priority: priority || 0,
      status: 'pending',
      created_at: new Date().toISOString()
    };
    queue.push(item);
    queue.sort((a, b) => (b.priority || 0) - (a.priority || 0));
    saveQueue(queue);
    res.json({ success: true, data: item });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// GET /api/queue/next
router.get('/next', (req, res) => {
  try {
    const queue = loadQueue();
    const next = queue.find(item => item.status === 'pending');
    if (!next) return res.json({ success: true, data: null });
    res.json({ success: true, data: next });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// POST /api/queue/process
router.post('/process', async (req, res) => {
  try {
    const queue = loadQueue();
    const idx = queue.findIndex(item => item.status === 'pending');
    if (idx === -1) return res.json({ success: true, data: null, message: 'Queue is empty' });

    const item = queue[idx];
    queue[idx].status = 'processing';
    queue[idx].started_at = new Date().toISOString();
    saveQueue(queue);

    let result;
    try {
      const { postToAll } = require('../orchestrator/auto-poster');
      result = await postToAll(item.payload);
      queue[idx].status = 'done';
      queue[idx].result = result;
      queue[idx].completed_at = new Date().toISOString();
    } catch (postErr) {
      queue[idx].status = 'failed';
      queue[idx].error = postErr.message;
      queue[idx].failed_at = new Date().toISOString();
      await notifyError(`process:${item.platform}`, postErr);
    }
    saveQueue(queue);
    res.json({ success: true, data: queue[idx] });
  } catch (err) {
    await notifyError('process', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

// DELETE /api/queue/clear
router.delete('/clear', (req, res) => {
  try {
    saveQueue([]);
    res.json({ success: true, message: 'Queue cleared' });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

module.exports = router;
