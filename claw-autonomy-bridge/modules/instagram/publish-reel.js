'use strict';
const { createClient } = require('./instagram-client');

async function publishReel({ videoUrl, caption }) {
  const client = createClient();
  const accountId = process.env.INSTAGRAM_BUSINESS_ACCOUNT_ID;

  const containerRes = await client.post(`/${accountId}/media`, {
    media_type: 'REELS',
    video_url: videoUrl,
    caption
  });
  const containerId = containerRes.data.id;

  await waitForContainer(client, accountId, containerId);

  const publishRes = await client.post(`/${accountId}/media_publish`, {
    creation_id: containerId
  });
  return publishRes.data;
}

async function waitForContainer(client, accountId, containerId, maxAttempts = 20) {
  for (let i = 0; i < maxAttempts; i++) {
    const res = await client.get(`/${containerId}`, { params: { fields: 'status_code,status' } });
    if (res.data.status_code === 'FINISHED') return;
    if (res.data.status_code === 'ERROR') throw new Error('Media container processing failed');
    await new Promise(r => setTimeout(r, 15000));
  }
  throw new Error('Media container processing timeout');
}

module.exports = { publishReel };
