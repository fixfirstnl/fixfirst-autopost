'use strict';
const express = require('express');
const router = express.Router();
const { uploadVideo } = require('./youtube/upload-video');
const { uploadShort } = require('./youtube/upload-short');
const { createClient } = require('./youtube/youtube-client');

async function notifyError(label, err) {
  try {
    const { sendMessage } = require('./telegram/status-reporter');
    await sendMessage(`❌ [youtube-uploader] ${label}: ${err.message}`);
  } catch (_) {}
}

// POST /api/youtube/upload
router.post('/upload', async (req, res) => {
  const { video_url, title, description, tags, thumbnail_url, privacy_status } = req.body;
  if (!video_url || !title) {
    return res.status(400).json({ success: false, error: 'video_url and title are required' });
  }
  try {
    const result = await uploadVideo({
      videoPath: video_url,
      title,
      description: description || '',
      tags: tags || [],
      privacyStatus: privacy_status || 'public'
    });
    res.json({ success: true, data: result });
  } catch (err) {
    await notifyError('upload', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

// POST /api/youtube/shorts
router.post('/shorts', async (req, res) => {
  const { video_url, title, description, tags } = req.body;
  if (!video_url || !title) {
    return res.status(400).json({ success: false, error: 'video_url and title are required' });
  }
  try {
    const result = await uploadShort({
      videoPath: video_url,
      title,
      description: description || '',
      tags: tags || []
    });
    res.json({ success: true, data: result });
  } catch (err) {
    await notifyError('shorts', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

// PATCH /api/youtube/update/:id
router.patch('/update/:id', async (req, res) => {
  const { title, description, tags } = req.body;
  if (!title && description === undefined && !tags) {
    return res.status(400).json({ success: false, error: 'At least one of title, description, or tags is required' });
  }
  try {
    const client = await createClient();
    const snippet = {};
    if (title) snippet.title = title;
    if (description !== undefined) snippet.description = description;
    if (tags) snippet.tags = tags;
    const result = await client.put('/videos', {
      id: req.params.id,
      snippet
    }, { params: { part: 'snippet' } });
    res.json({ success: true, data: result.data });
  } catch (err) {
    await notifyError('update', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

module.exports = router;
