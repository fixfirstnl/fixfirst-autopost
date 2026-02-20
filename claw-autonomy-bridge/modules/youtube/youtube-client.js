'use strict';
const axios = require('axios');

const TOKEN_URL = 'https://oauth2.googleapis.com/token';
let cachedToken = null;
let tokenExpiry = 0;

async function getAccessToken() {
  if (cachedToken && Date.now() < tokenExpiry - 60000) return cachedToken;

  const res = await axios.post(TOKEN_URL, {
    client_id: process.env.YOUTUBE_CLIENT_ID,
    client_secret: process.env.YOUTUBE_CLIENT_SECRET,
    refresh_token: process.env.YOUTUBE_REFRESH_TOKEN,
    grant_type: 'refresh_token'
  });

  cachedToken = res.data.access_token;
  tokenExpiry = Date.now() + (res.data.expires_in || 3600) * 1000;
  return cachedToken;
}

async function createClient() {
  const token = await getAccessToken();
  return axios.create({
    baseURL: 'https://www.googleapis.com/youtube/v3',
    headers: { Authorization: `Bearer ${token}` },
    timeout: 60000
  });
}

module.exports = { createClient, getAccessToken };
