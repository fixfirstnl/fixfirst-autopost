'use strict';
const { createClient } = require('./telegram-client');
const { sendMessage } = require('./status-reporter');

const commands = {};

function registerCommand(command, handler) {
  commands[command] = handler;
}

async function processUpdate(update) {
  const message = update.message;
  if (!message || !message.text) return;
  const text = message.text.trim();
  const command = text.split(' ')[0].toLowerCase();
  const handler = commands[command];
  if (handler) {
    const response = await handler(message, text.slice(command.length).trim());
    if (response) await sendMessage(response, message.chat.id);
  }
}

async function setWebhook(webhookUrl) {
  const client = createClient();
  const res = await client.post('/setWebhook', { url: webhookUrl });
  return res.data;
}

module.exports = { registerCommand, processUpdate, setWebhook };
