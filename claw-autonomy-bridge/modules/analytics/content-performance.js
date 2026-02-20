'use strict';
const { getVideoAnalytics } = require('../tiktok/analytics');

async function getContentPerformance(videoIds = []) {
  const results = await Promise.allSettled(videoIds.map(id => getVideoAnalytics(id)));
  return {
    videos: results.map((r, i) => ({
      videoId: videoIds[i],
      data: r.status === 'fulfilled' ? r.value : null,
      error: r.status === 'rejected' ? r.reason.message : null
    })),
    timestamp: new Date().toISOString()
  };
}

module.exports = { getContentPerformance };
