'use strict';
const { createClient } = require('./mailerlite-client');

async function triggerAutomation({ automationId, email }) {
  const client = createClient();
  const res = await client.post(`/automations/${automationId}/trigger`, { email });
  return res.data;
}

async function listAutomations() {
  const client = createClient();
  const res = await client.get('/automations');
  return res.data;
}

module.exports = { triggerAutomation, listAutomations };
