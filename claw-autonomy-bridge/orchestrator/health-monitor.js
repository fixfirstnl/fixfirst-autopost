'use strict';
const axios = require('axios');
const { sendMessage } = require('../modules/telegram/status-reporter');

const checks = {
  notion: () => axios.get('https://api.notion.com/v1/users/me', {
    headers: { Authorization: `Bearer ${process.env.NOTION_TOKEN}`, 'Notion-Version': '2022-06-28' },
    timeout: 10000
  }),
  mailerlite: () => axios.get('https://connect.mailerlite.com/api/subscribers', {
    headers: { Authorization: `Bearer ${process.env.MAILERLITE_API_KEY}` },
    params: { limit: 1 },
    timeout: 10000
  }),
  gumroad: () => axios.get('https://api.gumroad.com/v2/products', {
    params: { access_token: process.env.GUMROAD_ACCESS_TOKEN },
    timeout: 10000
  })
};

let lastHealth = {};

async function checkHealth() {
  const results = {};
  for (const [name, check] of Object.entries(checks)) {
    try {
      await check();
      results[name] = { status: 'ok', checkedAt: new Date().toISOString() };
    } catch (err) {
      const status = err.response ? err.response.status : 'network_error';
      results[name] = { status: 'error', code: status, message: err.message, checkedAt: new Date().toISOString() };
      const prevStatus = lastHealth[name] ? lastHealth[name].status : 'unknown';
      if (prevStatus === 'ok') {
        await sendMessage(`⚠️ Health alert: <b>${name}</b> is DOWN (${status})`).catch(() => {});
      }
    }
  }
  lastHealth = results;
  return results;
}

function getLastHealth() {
  return lastHealth;
}

module.exports = { checkHealth, getLastHealth };
