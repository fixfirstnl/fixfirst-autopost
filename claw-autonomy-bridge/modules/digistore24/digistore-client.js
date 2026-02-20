'use strict';
const axios = require('axios');

const BASE_URL = 'https://www.digistore24.com/api/call';

function createClient() {
  return axios.create({
    baseURL: BASE_URL,
    headers: { 'Content-Type': 'application/json' },
    timeout: 30000,
    params: {
      api_key: process.env.DIGISTORE24_API_KEY,
      affiliate_id: process.env.DIGISTORE24_AFFILIATE_ID
    }
  });
}

module.exports = { createClient };
