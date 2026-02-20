'use strict';
const { createClient } = require('./notion-client');

async function updateContentHubItem(pageId, { status, publishDate, platforms }) {
  const client = createClient();
  const properties = {};
  if (status) properties['Status'] = { select: { name: status } };
  if (publishDate) properties['Publish Date'] = { date: { start: publishDate } };
  if (platforms) properties['Platforms'] = { multi_select: platforms.map(p => ({ name: p })) };

  const res = await client.patch(`/pages/${pageId}`, { properties });
  return res.data;
}

async function getContentQueue() {
  const client = createClient();
  const res = await client.post(`/databases/${process.env.NOTION_CONTENT_HUB_DB}/query`, {
    filter: { property: 'Status', select: { equals: 'In productie' } },
    sorts: [{ property: 'Created', direction: 'ascending' }]
  });
  return res.data.results;
}

module.exports = { updateContentHubItem, getContentQueue };
