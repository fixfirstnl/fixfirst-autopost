'use strict';
const { createClient } = require('./mailerlite-client');

async function addSubscriber({ email, name, fields = {}, groups = [] }) {
  const client = createClient();
  const res = await client.post('/subscribers', {
    email,
    fields: { name, ...fields },
    groups: groups.length ? groups : [process.env.MAILERLITE_GROUP_ID]
  });
  return res.data;
}

async function tagSubscribers({ groupId, emails }) {
  const client = createClient();
  const results = [];
  for (const email of emails) {
    try {
      const res = await client.post(`/groups/${groupId}/subscribers/import`, {
        subscribers: [{ email }]
      });
      results.push({ email, success: true, data: res.data });
    } catch (err) {
      results.push({ email, success: false, error: err.message });
    }
  }
  return results;
}

async function getStats() {
  const client = createClient();
  const res = await client.get('/campaigns', { params: { limit: 10, sort: 'created_at', order: 'DESC' } });
  return res.data;
}

module.exports = { addSubscriber, tagSubscribers, getStats };
