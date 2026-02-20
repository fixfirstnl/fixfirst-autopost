'use strict';
const { getAccessToken } = require('./youtube-client');
const axios = require('axios');
const fs = require('fs');

async function uploadShort({ videoPath, title, description = '', tags = [], privacyStatus = 'public' }) {
  const token = await getAccessToken();

  const metadataRes = await axios.post(
    'https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status',
    {
      snippet: { title: `${title} #Shorts`, description, tags: [...tags, 'Shorts'] },
      status: { privacyStatus }
    },
    {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
        'X-Upload-Content-Type': 'video/mp4',
        'X-Upload-Content-Length': fs.statSync(videoPath).size
      }
    }
  );

  const uploadUrl = metadataRes.headers.location;
  const fileStream = fs.createReadStream(videoPath);
  const fileSize = fs.statSync(videoPath).size;

  const uploadRes = await axios.put(uploadUrl, fileStream, {
    headers: {
      'Content-Type': 'video/mp4',
      'Content-Length': fileSize
    },
    maxContentLength: Infinity,
    maxBodyLength: Infinity
  });

  return uploadRes.data;
}

module.exports = { uploadShort };
