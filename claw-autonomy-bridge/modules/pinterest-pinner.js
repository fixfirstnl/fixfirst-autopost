'use strict';
const express = require('express');
const router = express.Router();
const { createPin } = require('./pinterest/create-pin');
const { createBoard, listBoards } = require('./pinterest/manage-boards');

async function notifyError(label, err) {
  try {
    const { sendMessage } = require('./telegram/status-reporter');
    await sendMessage(`❌ [pinterest-pinner] ${label}: ${err.message}`);
  } catch (_) {}
}

// POST /api/pinterest/pin
router.post('/pin', async (req, res) => {
  const { image_url, title, description, link, board_id } = req.body;
  if (!image_url || !board_id) {
    return res.status(400).json({ success: false, error: 'image_url and board_id are required' });
  }
  try {
    const result = await createPin({ imageUrl: image_url, title, description, link, boardId: board_id });
    res.json({ success: true, data: result });
  } catch (err) {
    await notifyError('pin', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

// POST /api/pinterest/board
router.post('/board', async (req, res) => {
  const { name, description } = req.body;
  if (!name) {
    return res.status(400).json({ success: false, error: 'name is required' });
  }
  try {
    const result = await createBoard({ name, description });
    res.json({ success: true, data: result });
  } catch (err) {
    await notifyError('board', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

// GET /api/pinterest/boards
router.get('/boards', async (req, res) => {
  try {
    const result = await listBoards();
    res.json({ success: true, data: result });
  } catch (err) {
    await notifyError('boards', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

module.exports = router;
