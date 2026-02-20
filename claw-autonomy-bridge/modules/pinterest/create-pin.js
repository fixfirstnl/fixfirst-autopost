'use strict';
const { createClient } = require('./pinterest-client');

async function createPin({ boardId, title, description, imageUrl, link, altText = '' }) {
  const client = createClient();
  const res = await client.post('/pins', {
    board_id: boardId || process.env.PINTEREST_BOARD_ID,
    title,
    description,
    link,
    alt_text: altText,
    media_source: { source_type: 'image_url', url: imageUrl }
  });
  return res.data;
}

module.exports = { createPin };
