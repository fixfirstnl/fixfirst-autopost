'use strict';
const { getContentQueue, updateContentHubItem } = require('../modules/notion/update-content-hub');
const { postToAll } = require('./auto-poster');
const { sendMessage } = require('../modules/telegram/status-reporter');

async function runContentPush({ videoPath } = {}) {
  const queue = await getContentQueue();
  if (!queue.length) return { message: 'No content in queue', processed: 0 };

  const item = queue[0];
  const title = item.properties.Name?.title?.[0]?.plain_text || 'FixFirst Content';
  const caption = item.properties.Caption?.rich_text?.[0]?.plain_text || title;
  const hashtags = (item.properties.Hashtags?.multi_select || []).map(h => h.name);
  const affiliateLink = item.properties['Affiliate Link']?.url || '';
  const resolvedVideoPath = videoPath || item.properties['Video Path']?.rich_text?.[0]?.plain_text || '';

  const postResults = await postToAll({ videoPath: resolvedVideoPath, caption, title, hashtags, affiliateLink });

  await updateContentHubItem(item.id, { status: 'Published', publishDate: new Date().toISOString().split('T')[0] });
  await sendMessage(`📢 Content published: <b>${title}</b>`).catch(() => {});

  return { item: item.id, title, results: postResults };
}

module.exports = { runContentPush };
