'use strict';
const axios = require('axios');

function createClient() {
  const token = process.env.TELEGRAM_BOT_TOKEN;
  return axios.create({
    baseURL: `https://api.telegram.org/bot${token}`,
    timeout: 15000
  });
}

module.exports = { createClient };
