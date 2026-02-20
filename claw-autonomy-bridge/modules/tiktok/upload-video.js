'use strict';
const { createClient } = require('./tiktok-client');
const fs = require('fs');
const path = require('path');

async function initUpload({ videoSize, chunkSize, totalChunkCount }) {
  const client = createClient();
  const res = await client.post('/post/publish/video/init/', {
    post_info: {
      title: '',
      privacy_level: 'PUBLIC_TO_EVERYONE',
      disable_duet: false,
      disable_comment: false,
      disable_stitch: false
    },
    source_info: {
      source: 'FILE_UPLOAD',
      video_size: videoSize,
      chunk_size: chunkSize,
      total_chunk_count: totalChunkCount
    }
  });
  return res.data;
}

async function uploadVideo({ videoPath, caption, hashtags = [] }) {
  const stats = fs.statSync(videoPath);
  const videoSize = stats.size;
  const chunkSize = Math.min(10 * 1024 * 1024, videoSize);
  const totalChunkCount = Math.ceil(videoSize / chunkSize);

  const initResult = await initUpload({ videoSize, chunkSize, totalChunkCount });
  const { upload_url, publish_id } = initResult.data;

  const fileBuffer = fs.readFileSync(videoPath);
  const axios = require('axios');
  await axios.put(upload_url, fileBuffer, {
    headers: {
      'Content-Type': 'video/mp4',
      'Content-Range': `bytes 0-${videoSize - 1}/${videoSize}`,
      'Content-Length': videoSize
    }
  });

  return { publishId: publish_id, caption, hashtags };
}

async function getUploadStatus(publishId) {
  const client = createClient();
  const res = await client.post('/post/publish/status/fetch/', { publish_id: publishId });
  return res.data;
}

module.exports = { uploadVideo, getUploadStatus };
