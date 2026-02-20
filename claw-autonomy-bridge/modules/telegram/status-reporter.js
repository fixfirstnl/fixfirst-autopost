'use strict';
const { createClient } = require('./telegram-client');

async function sendMessage(text, chatId) {
  const client = createClient();
  const res = await client.post('/sendMessage', {
    chat_id: chatId || process.env.TELEGRAM_CHAT_ID,
    text,
    parse_mode: 'HTML'
  });
  return res.data;
}

async function sendReport({ title, body }) {
  const text = `<b>${title}</b>\n\n${body}`;
  return sendMessage(text);
}

module.exports = { sendMessage, sendReport };
