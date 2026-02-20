'use strict';
const { createClient } = require('./later-client');
const { generateCSV } = require('./csv-generator');
const FormData = require('form-data');

async function schedulePost(post) {
  const client = createClient();
  const payload = {
    social_profile_id: process.env.LATER_SOCIAL_SET_ID,
    caption: post.caption,
    media_url: post.mediaUrl,
    scheduled_at: post.scheduledAt
  };
  const res = await client.post('/posts', payload);
  return res.data;
}

async function bulkSchedule(posts) {
  const results = [];
  for (const post of posts) {
    try {
      const result = await schedulePost(post);
      results.push({ success: true, post, result });
    } catch (err) {
      results.push({ success: false, post, error: err.message });
    }
  }
  return results;
}

async function getCalendar(from, to) {
  const client = createClient();
  const res = await client.get('/posts', { params: { from, to, social_profile_id: process.env.LATER_SOCIAL_SET_ID } });
  return res.data;
}

async function importCSV(posts) {
  const csv = generateCSV(posts);
  return { csv, message: 'CSV generated for Later import', rowCount: posts.length };
}

module.exports = { schedulePost, bulkSchedule, getCalendar, importCSV };
