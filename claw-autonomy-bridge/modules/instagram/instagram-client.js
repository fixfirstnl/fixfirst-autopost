'use strict';
const axios = require('axios');

const BASE_URL = 'https://graph.facebook.com/v19.0';

function createClient() {
  return axios.create({
    baseURL: BASE_URL,
    params: { access_token: process.env.INSTAGRAM_ACCESS_TOKEN },
    timeout: 60000
  });
}

module.exports = { createClient };
