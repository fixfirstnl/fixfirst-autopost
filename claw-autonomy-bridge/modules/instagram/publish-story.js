'use strict';
const { createClient } = require('./instagram-client');

async function publishStory({ imageUrl, videoUrl }) {
  const client = createClient();
  const accountId = process.env.INSTAGRAM_BUSINESS_ACCOUNT_ID;

  const payload = imageUrl
    ? { image_url: imageUrl, media_type: 'IMAGE' }
    : { video_url: videoUrl, media_type: 'VIDEO' };

  const containerRes = await client.post(`/${accountId}/media`, payload);
  const publishRes = await client.post(`/${accountId}/media_publish`, {
    creation_id: containerRes.data.id
  });
  return publishRes.data;
}

module.exports = { publishStory };
