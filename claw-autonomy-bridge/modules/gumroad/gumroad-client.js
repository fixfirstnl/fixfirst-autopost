'use strict';
const axios = require('axios');

const BASE_URL = 'https://api.gumroad.com/v2';

function createClient() {
  return axios.create({
    baseURL: BASE_URL,
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    timeout: 30000
  });
}

function getParams(extra = {}) {
  return { access_token: process.env.GUMROAD_ACCESS_TOKEN, ...extra };
}

module.exports = { createClient, getParams };
