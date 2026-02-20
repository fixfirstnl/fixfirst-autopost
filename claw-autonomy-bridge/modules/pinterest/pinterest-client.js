'use strict';
const axios = require('axios');

const BASE_URL = 'https://api.pinterest.com/v5';

function createClient() {
  const client = axios.create({
    baseURL: BASE_URL,
    headers: {
      Authorization: `Bearer ${process.env.PINTEREST_ACCESS_TOKEN}`,
      'Content-Type': 'application/json'
    },
    timeout: 30000
  });

  client.interceptors.response.use(
    res => res,
    async err => {
      if (err.response && err.response.status === 429) {
        await new Promise(r => setTimeout(r, 60000));
        return client.request(err.config);
      }
      return Promise.reject(err);
    }
  );

  return client;
}

module.exports = { createClient };
