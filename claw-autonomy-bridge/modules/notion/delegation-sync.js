'use strict';
const { createClient } = require('./notion-client');

async function getDelegationQueue() {
  const client = createClient();
  const res = await client.post(`/databases/${process.env.NOTION_DELEGATIONS_DB}/query`, {
    filter: { property: 'Status', select: { equals: 'Pending' } },
    sorts: [{ property: 'Priority', direction: 'ascending' }]
  });
  return res.data.results;
}

async function completeTask(pageId) {
  const client = createClient();
  const res = await client.patch(`/pages/${pageId}`, {
    properties: {
      Status: { select: { name: 'Completed' } },
      'Completed At': { date: { start: new Date().toISOString() } }
    }
  });
  return res.data;
}

module.exports = { getDelegationQueue, completeTask };
