'use strict';
const express = require('express');
const router = express.Router();
const { publishReel } = require('./instagram/publish-reel');
const { publishStory } = require('./instagram/publish-story');
const { publishCarousel } = require('./instagram/publish-carousel');
const { createClient } = require('./instagram/instagram-client');

async function notifyError(label, err) {
  try {
    const { sendMessage } = require('./telegram/status-reporter');
    await sendMessage(`❌ [instagram-poster] ${label}: ${err.message}`);
  } catch (_) {}
}

// POST /api/instagram/post  (image or reel)
router.post('/post', async (req, res) => {
  const { image_url, video_url, caption, hashtags, type } = req.body;
  if (!image_url && !video_url) {
    return res.status(400).json({ success: false, error: 'image_url or video_url is required' });
  }
  try {
    const fullCaption = [caption, ...(hashtags || []).map(h => (h.startsWith('#') ? h : `#${h}`))].filter(Boolean).join(' ');
    let result;
    if (video_url && type !== 'carousel') {
      result = await publishReel({ videoUrl: video_url, caption: fullCaption });
    } else if (image_url) {
      const client = createClient();
      const accountId = process.env.INSTAGRAM_BUSINESS_ACCOUNT_ID;
      const containerRes = await client.post(`/${accountId}/media`, {
        image_url,
        caption: fullCaption
      });
      const publishRes = await client.post(`/${accountId}/media_publish`, {
        creation_id: containerRes.data.id
      });
      result = publishRes.data;
    } else {
      return res.status(400).json({ success: false, error: 'Unsupported post type' });
    }
    res.json({ success: true, data: result });
  } catch (err) {
    await notifyError('post', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

// POST /api/instagram/story
router.post('/story', async (req, res) => {
  const { image_url, video_url } = req.body;
  if (!image_url && !video_url) {
    return res.status(400).json({ success: false, error: 'image_url or video_url is required' });
  }
  try {
    const result = await publishStory({ imageUrl: image_url, videoUrl: video_url });
    res.json({ success: true, data: result });
  } catch (err) {
    await notifyError('story', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

// GET /api/instagram/insights
router.get('/insights', async (req, res) => {
  const { media_id } = req.query;
  if (!media_id) {
    return res.status(400).json({ success: false, error: 'media_id query param is required' });
  }
  try {
    const client = createClient();
    const metrics = 'impressions,reach,likes,comments,shares,saved';
    const result = await client.get(`/${media_id}/insights`, {
      params: { metric: metrics }
    });
    res.json({ success: true, data: result.data });
  } catch (err) {
    await notifyError('insights', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

module.exports = router;
