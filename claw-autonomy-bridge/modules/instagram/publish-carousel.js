'use strict';
const { createClient } = require('./instagram-client');

async function publishCarousel({ mediaUrls, caption }) {
  const client = createClient();
  const accountId = process.env.INSTAGRAM_BUSINESS_ACCOUNT_ID;

  const children = await Promise.all(mediaUrls.map(url =>
    client.post(`/${accountId}/media`, { image_url: url, is_carousel_item: true })
      .then(r => r.data.id)
  ));

  const containerRes = await client.post(`/${accountId}/media`, {
    media_type: 'CAROUSEL',
    caption,
    children: children.join(',')
  });

  const publishRes = await client.post(`/${accountId}/media_publish`, {
    creation_id: containerRes.data.id
  });
  return publishRes.data;
}

module.exports = { publishCarousel };
