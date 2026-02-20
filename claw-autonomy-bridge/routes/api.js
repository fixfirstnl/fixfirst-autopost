'use strict';
const express = require('express');
const router = express.Router();

// ---- Later ----
const laterSchedule = require('../modules/later/schedule-posts');

router.post('/later/import-csv', async (req, res) => {
  try {
    const result = await laterSchedule.importCSV(req.body.posts || []);
    res.json({ success: true, ...result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.post('/later/schedule', async (req, res) => {
  try {
    const result = await laterSchedule.schedulePost(req.body);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.get('/later/calendar', async (req, res) => {
  try {
    const result = await laterSchedule.getCalendar(req.query.from, req.query.to);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.post('/later/bulk-schedule', async (req, res) => {
  try {
    const result = await laterSchedule.bulkSchedule(req.body.posts || []);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// ---- MailerLite ----
const { sendBlast } = require('../modules/mailerlite/send-blast');
const { addSubscriber, tagSubscribers, getStats } = require('../modules/mailerlite/manage-subscribers');
const { triggerAutomation } = require('../modules/mailerlite/automation-triggers');

router.post('/mailerlite/blast', async (req, res) => {
  try {
    const result = await sendBlast(req.body);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.post('/mailerlite/subscriber', async (req, res) => {
  try {
    const result = await addSubscriber(req.body);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.post('/mailerlite/tag', async (req, res) => {
  try {
    const result = await tagSubscribers(req.body);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.get('/mailerlite/stats', async (req, res) => {
  try {
    const result = await getStats();
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.post('/mailerlite/automation', async (req, res) => {
  try {
    const result = await triggerAutomation(req.body);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// ---- TikTok ----
const { uploadVideo: tiktokUpload, getUploadStatus } = require('../modules/tiktok/upload-video');
const { getVideoAnalytics, getAccountAnalytics } = require('../modules/tiktok/analytics');

router.post('/post/tiktok', async (req, res) => {
  try {
    const result = await tiktokUpload(req.body);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.get('/post/tiktok/status/:publishId', async (req, res) => {
  try {
    const result = await getUploadStatus(req.params.publishId);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// ---- Instagram ----
const { publishReel } = require('../modules/instagram/publish-reel');
const { publishStory } = require('../modules/instagram/publish-story');
const { publishCarousel } = require('../modules/instagram/publish-carousel');

router.post('/post/instagram/reel', async (req, res) => {
  try {
    const result = await publishReel(req.body);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.post('/post/instagram/story', async (req, res) => {
  try {
    const result = await publishStory(req.body);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.post('/post/instagram/carousel', async (req, res) => {
  try {
    const result = await publishCarousel(req.body);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// ---- YouTube ----
const { uploadShort } = require('../modules/youtube/upload-short');
const { uploadVideo: ytUpload } = require('../modules/youtube/upload-video');
const { addToPlaylist, createPlaylist } = require('../modules/youtube/manage-playlist');

router.post('/post/youtube/short', async (req, res) => {
  try {
    const result = await uploadShort(req.body);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.post('/post/youtube/video', async (req, res) => {
  try {
    const result = await ytUpload(req.body);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.post('/post/youtube/playlist', async (req, res) => {
  try {
    const result = await addToPlaylist(req.body);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// ---- Pinterest ----
const { createPin } = require('../modules/pinterest/create-pin');
const { createBoard, listBoards } = require('../modules/pinterest/manage-boards');
const { bulkCreatePins } = require('../modules/pinterest/bulk-pin');

router.post('/post/pinterest/pin', async (req, res) => {
  try {
    const result = await createPin(req.body);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.post('/pinterest/bulk-pins', async (req, res) => {
  try {
    const result = await bulkCreatePins(req.body.pins || []);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.post('/pinterest/board', async (req, res) => {
  try {
    const result = await createBoard(req.body);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.get('/pinterest/boards', async (req, res) => {
  try {
    const result = await listBoards();
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// ---- Gumroad ----
const { listProducts, getProduct } = require('../modules/gumroad/manage-products');
const { updateProduct } = require('../modules/gumroad/update-product');
const { createCoupon } = require('../modules/gumroad/create-coupon');
const { getSales, getRevenueSummary } = require('../modules/gumroad/sales-analytics');

router.get('/gumroad/products', async (req, res) => {
  try {
    const result = await listProducts();
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.put('/gumroad/product/:id', async (req, res) => {
  try {
    const result = await updateProduct(req.params.id, req.body);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.post('/gumroad/coupon', async (req, res) => {
  try {
    const result = await createCoupon(req.body);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.get('/gumroad/sales', async (req, res) => {
  try {
    const result = await getSales(req.query);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// ---- Digistore24 ----
const { getProductCatalog } = require('../modules/digistore24/product-catalog');
const { generateAffiliateLink, generateMultipleLinks } = require('../modules/digistore24/affiliate-links');
const { getCommissions, getConversionStats } = require('../modules/digistore24/commission-tracker');

router.get('/digistore/products', async (req, res) => {
  try {
    const result = await getProductCatalog();
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.post('/digistore/link', async (req, res) => {
  try {
    const result = generateAffiliateLink(req.body);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.get('/digistore/commissions', async (req, res) => {
  try {
    const result = await getCommissions(req.query);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.get('/digistore/stats', async (req, res) => {
  try {
    const result = await getConversionStats();
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// ---- Notion ----
const { updateContentHubItem, getContentQueue } = require('../modules/notion/update-content-hub');
const { updateTask, markTaskDone } = require('../modules/notion/update-tasks');
const { updateProduct: updateNotionProduct } = require('../modules/notion/update-products');
const { getDelegationQueue, completeTask } = require('../modules/notion/delegation-sync');

router.put('/notion/content-hub/:id', async (req, res) => {
  try {
    const result = await updateContentHubItem(req.params.id, req.body);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.put('/notion/task/:id', async (req, res) => {
  try {
    const result = await updateTask(req.params.id, req.body);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.put('/notion/product/:id', async (req, res) => {
  try {
    const result = await updateNotionProduct(req.params.id, req.body);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.get('/notion/queue', async (req, res) => {
  try {
    const result = await getDelegationQueue();
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.post('/notion/complete/:id', async (req, res) => {
  try {
    const result = await completeTask(req.params.id);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// ---- Cross-platform ----
const { postToAll } = require('../orchestrator/auto-poster');

router.post('/post/all', async (req, res) => {
  try {
    const result = await postToAll(req.body);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// ---- Orchestration ----
const { runContentPush } = require('../orchestrator/content-pipeline');
const { runAffiliatePush } = require('../orchestrator/affiliate-optimizer');
const { getStatus } = require('../orchestrator/task-queue');

router.post('/orchestrate/content-push', async (req, res) => {
  try {
    const result = await runContentPush(req.body);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.post('/orchestrate/affiliate-push', async (req, res) => {
  try {
    const result = await runAffiliatePush(req.body);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.post('/orchestrate/daily-routine', async (req, res) => {
  try {
    const contentResult = await runContentPush(req.body).catch(e => ({ error: e.message }));
    const affiliateResult = await runAffiliatePush(req.body).catch(e => ({ error: e.message }));
    res.json({ success: true, data: { content: contentResult, affiliate: affiliateResult } });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.get('/orchestrate/status', (req, res) => {
  const status = getStatus();
  res.json({ success: true, data: status });
});

// ---- Analytics ----
const { getUnifiedDashboard } = require('../modules/analytics/unified-dashboard');
const { getRevenueReport } = require('../modules/analytics/revenue-tracker');
const { getContentPerformance } = require('../modules/analytics/content-performance');

router.get('/analytics/revenue', async (req, res) => {
  try {
    const result = await getRevenueReport();
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.get('/analytics/content', async (req, res) => {
  try {
    const videoIds = req.query.ids ? req.query.ids.split(',') : [];
    const result = await getContentPerformance(videoIds);
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.get('/analytics/funnel', async (req, res) => {
  try {
    const result = await getUnifiedDashboard();
    res.json({ success: true, data: result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

router.post('/analytics/report', async (req, res) => {
  try {
    const report = await getRevenueReport();
    const { sendReport } = require('../modules/telegram/status-reporter');
    await sendReport({
      title: '📊 FixFirst Revenue Report',
      body: `Gumroad: €${report.gumroad.revenue} (${report.gumroad.sales} sales)\nDigistore24: €${report.digistore24.revenue} (${report.digistore24.conversions} conversions)\nTotal: €${report.total.revenue}`
    });
    res.json({ success: true, data: report });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// ---- Telegram webhook ----
const { processUpdate } = require('../modules/telegram/command-handler');

router.post('/telegram/webhook', async (req, res) => {
  try {
    await processUpdate(req.body);
    res.json({ ok: true });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

module.exports = router;
