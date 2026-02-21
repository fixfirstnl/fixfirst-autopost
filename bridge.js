'use strict';
require('dotenv').config();
const express = require('express');
const fetch = require('node-fetch');

const app = express();
const PORT = parseInt(process.env.PORT || '3001', 10);

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Count how many API keys are loaded from environment
function countLoadedKeys() {
  const apiKeyVars = [
    'TELEGRAM_BOT_TOKEN',
    'TELEGRAM_CHAT_ID',
    'MAILERLITE_API_TOKEN',
    'DIGISTORE24_API_KEY',
    'YOUTUBE_CLIENT_ID',
    'YOUTUBE_CLIENT_SECRET',
    'ETSY_API_KEY',
    'ETSY_SHARED_SECRET',
    'GUMROAD_APP_ID',
    'GUMROAD_APP_SECRET',
    'GUMROAD_ACCESS_TOKEN',
    'GUMROAD_SELLER_ID',
    'VPS_HOST',
  ];
  return apiKeyVars.filter(k => !!process.env[k]).length;
}

// GET /health
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    service: 'fixfirst-autopost-bridge',
    port: PORT,
    uptime: process.uptime(),
    loadedApiKeys: countLoadedKeys(),
    timestamp: new Date().toISOString(),
  });
});

// POST /webhook/gumroad
app.post('/webhook/gumroad', (req, res) => {
  const event = req.body;
  // Log only non-sensitive identifiers to avoid exposing customer data
  console.log('[gumroad webhook] Sale event received. type:', event.resource_name, 'sale_id:', event.sale_id);
  res.json({ received: true });
});

// GET /callback/gumroad
app.get('/callback/gumroad', (req, res) => {
  const { code, state } = req.query;
  // Log state for debugging; do not log the authorization code
  console.log('[gumroad oauth] Callback received. state:', state);
  res.json({ status: 'callback_received' });
});

// Send Telegram startup notification
async function notifyTelegram(message) {
  const token = process.env.TELEGRAM_BOT_TOKEN;
  const chatId = process.env.TELEGRAM_CHAT_ID;
  if (!token || !chatId) return;
  try {
    await fetch(
      `https://api.telegram.org/bot${token}/sendMessage`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chat_id: chatId, text: message, parse_mode: 'Markdown' }),
      }
    );
  } catch (err) {
    console.error('[telegram] Failed to send notification:', err.message);
  }
}

app.listen(PORT, async () => {
  console.log(`[fixfirst-autopost-bridge] Running on port ${PORT}`);

  const loadedKeys = countLoadedKeys();
  const services = [
    process.env.TELEGRAM_BOT_TOKEN ? 'Telegram' : null,
    process.env.MAILERLITE_API_TOKEN ? 'MailerLite' : null,
    process.env.DIGISTORE24_API_KEY ? 'Digistore24' : null,
    process.env.YOUTUBE_CLIENT_ID ? 'YouTube' : null,
    process.env.ETSY_API_KEY ? 'Etsy' : null,
    process.env.GUMROAD_ACCESS_TOKEN ? 'Gumroad' : null,
  ].filter(Boolean);

  const message =
    `🚀 *fixfirst-autopost-bridge started*\n` +
    `Port: ${PORT}\n` +
    `Loaded API keys: ${loadedKeys}\n` +
    `Services: ${services.length > 0 ? services.join(', ') : 'none'}`;

  await notifyTelegram(message);
});
