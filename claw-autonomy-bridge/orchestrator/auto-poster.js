'use strict';
const { uploadVideo: tiktokUpload } = require('../modules/tiktok/upload-video');
const { publishReel } = require('../modules/instagram/publish-reel');
const { uploadShort } = require('../modules/youtube/upload-short');
const { createPin } = require('../modules/pinterest/create-pin');
const { sendMessage } = require('../modules/telegram/status-reporter');

async function postToAll({ videoPath, caption, imageUrl, title, hashtags = [], affiliateLink = '', boardId }) {
  const results = {};
  const tag = hashtags.map(h => `#${h}`).join(' ');
  const fullCaption = `${caption}\n\n${tag}\n\n${affiliateLink}`.trim();

  const tasks = [
    tiktokUpload({ videoPath, caption: fullCaption, hashtags }).then(r => { results.tiktok = { success: true, data: r }; }).catch(e => { results.tiktok = { success: false, error: e.message }; }),
    publishReel({ videoUrl: videoPath, caption: fullCaption }).then(r => { results.instagram = { success: true, data: r }; }).catch(e => { results.instagram = { success: false, error: e.message }; }),
    uploadShort({ videoPath, title, description: fullCaption, tags: hashtags }).then(r => { results.youtube = { success: true, data: r }; }).catch(e => { results.youtube = { success: false, error: e.message }; }),
    imageUrl ? createPin({ boardId, title, description: fullCaption, imageUrl, link: affiliateLink }).then(r => { results.pinterest = { success: true, data: r }; }).catch(e => { results.pinterest = { success: false, error: e.message }; }) : Promise.resolve()
  ];

  await Promise.allSettled(tasks);

  const successCount = Object.values(results).filter(r => r.success).length;
  await sendMessage(`✅ Auto-poster: ${successCount}/${Object.keys(results).length} platforms successful\nCaption: ${caption.slice(0, 100)}`).catch(() => {});

  return results;
}

module.exports = { postToAll };
