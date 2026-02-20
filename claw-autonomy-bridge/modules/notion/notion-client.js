'use strict';
const axios = require('axios');

const BASE_URL = 'https://api.notion.com/v1';

function createClient() {
  return axios.create({
    baseURL: BASE_URL,
    headers: {
      Authorization: `Bearer ${process.env.NOTION_TOKEN}`,
      'Notion-Version': '2022-06-28',
      'Content-Type': 'application/json'
    },
    timeout: 30000
  });
}

module.exports = { createClient };
