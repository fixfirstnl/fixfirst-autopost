'use strict';
const { createClient } = require('./tiktok-client');

async function getVideoAnalytics(videoId) {
  const client = createClient();
  const res = await client.get('/video/query/', {
    params: {
      fields: 'id,title,cover_image_url,video_description,duration,height,width,title,embed_html,embed_link,like_count,comment_count,share_count,view_count',
      filters: JSON.stringify({ video_ids: [videoId] })
    }
  });
  return res.data;
}

async function getAccountAnalytics() {
  const client = createClient();
  const res = await client.get('/research/user/info/', {
    params: {
      open_id: process.env.TIKTOK_OPEN_ID,
      fields: 'display_name,bio_description,profile_deep_link,is_verified,follower_count,following_count,likes_count,video_count'
    }
  });
  return res.data;
}

module.exports = { getVideoAnalytics, getAccountAnalytics };
