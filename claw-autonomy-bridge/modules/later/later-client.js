'use strict';
const axios = require('axios');

const BASE_URL = 'https://api.later.com/v1';

function createClient() {
  const client = axios.create({
    baseURL: BASE_URL,
    headers: {
      'Authorization': `Bearer ${process.env.LATER_API_KEY}`,
      'Content-Type': 'application/json'
    },
    timeout: 30000
  });

  client.interceptors.response.use(
    res => res,
    async err => {
      const status = err.response ? err.response.status : null;
      if (status === 429) {
        const delay = parseInt(err.response.headers['retry-after'] || '60', 10) * 1000;
        await new Promise(r => setTimeout(r, delay));
        return client.request(err.config);
      }
      return Promise.reject(err);
    }
  );

  return client;
}

module.exports = { createClient };
