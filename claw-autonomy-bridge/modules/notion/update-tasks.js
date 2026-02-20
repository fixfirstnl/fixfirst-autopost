'use strict';
const { createClient } = require('./notion-client');

async function updateTask(pageId, { status, completedAt }) {
  const client = createClient();
  const properties = {};
  if (status) properties['Status'] = { select: { name: status } };
  if (completedAt) properties['Completed At'] = { date: { start: completedAt } };
  const res = await client.patch(`/pages/${pageId}`, { properties });
  return res.data;
}

async function markTaskDone(pageId) {
  return updateTask(pageId, { status: 'Done', completedAt: new Date().toISOString() });
}

module.exports = { updateTask, markTaskDone };
