'use strict';
const express = require('express');
const router = express.Router();
const { schedulePost, bulkSchedule, getCalendar } = require('./later/schedule-posts');
const { createClient } = require('./later/later-client');

async function notifyError(label, err) {
  try {
    const { sendMessage } = require('./telegram/status-reporter');
    await sendMessage(`❌ [later-scheduler] ${label}: ${err.message}`);
  } catch (_) {}
}

// POST /api/later/schedule
router.post('/schedule', async (req, res) => {
  const { media_url, caption, platforms, scheduled_time } = req.body;
  if (!caption || !scheduled_time) {
    return res.status(400).json({ success: false, error: 'caption and scheduled_time are required' });
  }
  try {
    const result = await schedulePost({
      caption,
      mediaUrl: media_url,
      scheduledAt: scheduled_time,
      platforms
    });
    res.json({ success: true, data: result });
  } catch (err) {
    await notifyError('schedule', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

// POST /api/later/bulk-schedule
router.post('/bulk-schedule', async (req, res) => {
  const posts = req.body.posts;
  if (!Array.isArray(posts) || posts.length === 0) {
    return res.status(400).json({ success: false, error: 'posts array is required' });
  }
  try {
    const result = await bulkSchedule(posts.map(p => ({
      caption: p.caption,
      mediaUrl: p.media_url,
      scheduledAt: p.scheduled_time,
      platforms: p.platforms
    })));
    res.json({ success: true, data: result });
  } catch (err) {
    await notifyError('bulk-schedule', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

// GET /api/later/upcoming
router.get('/upcoming', async (req, res) => {
  try {
    const result = await getCalendar(req.query.from, req.query.to);
    res.json({ success: true, data: result });
  } catch (err) {
    await notifyError('upcoming', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

// DELETE /api/later/cancel/:id
router.delete('/cancel/:id', async (req, res) => {
  try {
    const client = createClient();
    const result = await client.delete(`/posts/${req.params.id}`);
    res.json({ success: true, data: result.data });
  } catch (err) {
    await notifyError('cancel', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

module.exports = router;
