'use strict';
const express = require('express');
const router = express.Router();
const { uploadVideo, getUploadStatus } = require('./tiktok/upload-video');

async function notifyError(label, err) {
  try {
    const { sendMessage } = require('./telegram/status-reporter');
    await sendMessage(`❌ [tiktok-poster] ${label}: ${err.message}`);
  } catch (_) {}
}

// POST /api/tiktok/upload
router.post('/upload', async (req, res) => {
  const { video_url, title, description, hashtags } = req.body;
  if (!video_url) {
    return res.status(400).json({ success: false, error: 'video_url is required' });
  }
  try {
    const result = await uploadVideo({
      videoPath: video_url,
      caption: [title, description].filter(Boolean).join(' '),
      hashtags: hashtags || []
    });
    res.json({ success: true, data: result });
  } catch (err) {
    await notifyError('upload', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

// GET /api/tiktok/status/:id
router.get('/status/:id', async (req, res) => {
  try {
    const result = await getUploadStatus(req.params.id);
    res.json({ success: true, data: result });
  } catch (err) {
    await notifyError('status', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

module.exports = router;
