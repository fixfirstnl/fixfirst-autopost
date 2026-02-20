'use strict';
const axios = require('axios');

const BASE_URL = 'https://open.tiktokapis.com/v2';

function createClient() {
  const client = axios.create({
    baseURL: BASE_URL,
    headers: {
      'Authorization': `Bearer ${process.env.TIKTOK_ACCESS_TOKEN}`,
      'Content-Type': 'application/json; charset=UTF-8'
    },
    timeout: 60000
  });

  client.interceptors.response.use(
    res => res,
    (err) => {
      const status = err.response ? err.response.status : null;
      const retryCount = (err.config.__retryCount || 0);
      if (status === 429 && retryCount < 3) {
        err.config.__retryCount = retryCount + 1;
        return new Promise(r => setTimeout(r, 30000)).then(() => client.request(err.config));
      }
      return Promise.reject(err);
    }
  );

  return client;
}

module.exports = { createClient };
