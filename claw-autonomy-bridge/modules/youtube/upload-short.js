'use strict';
const { getAccessToken } = require('./youtube-client');
const axios = require('axios');
const fs = require('fs');
const { execSync } = require('child_process');

const MIN_DURATION = 30; // minimum 30 seconds for quality Shorts
const MAX_DURATION = 59; // maximum 59 seconds for YouTube Shorts

const DEFAULT_DESCRIPTION_FOOTER = [
  '',
  '━━━━━━━━━━━━━━━━━━━━━━━━━━━━',
  '📧 FREE 72-HOUR SURVIVAL CHECKLIST:',
  '👉 Get it free: https://linktr.ee/fixfirstnl',
  '━━━━━━━━━━━━━━━━━━━━━━━━━━━━',
  '🔥 RECOMMENDED SURVIVAL RESOURCES:',
  '👉 Water Independence Guide: https://uswaterrevolution.com/#aff=fixfirstnl8890',
  '👉 Emergency Survival Binder ($19.99): https://fixfirst.gumroad.com/l/cpwvj',
  '👉 Self-Sufficient Backyard: https://independentbackyard.com/my-book/#aff=fixfirstnl8890',
  '━━━━━━━━━━━━━━━━━━━━━━━━━━━━',
  '🛒 OUR SURVIVAL GUIDE SHOP:',
  '📕 Gumroad (digital PDFs): https://fixfirst.gumroad.com/',
  '🏪 Etsy (printable guides): https://www.etsy.com/shop/FixFirstNL',
  '━━━━━━━━━━━━━━━━━━━━━━━━━━━━',
  '📺 FOLLOW FIXFIRST:',
  '▶️ YouTube: https://youtube.com/@fixfirstnl',
  '📱 TikTok: https://tiktok.com/@fixfirstnl',
  '📸 Instagram: https://instagram.com/fixfirstnl',
  '🔗 All links: https://linktr.ee/fixfirstnl',
  '━━━━━━━━━━━━━━━━━━━━━━━━━━━━',
].join('\n');

function getVideoDuration(videoPath) {
  try {
    const result = execSync(
      `ffprobe -v error -show_entries format=duration -of csv=p=0 "${videoPath}"`,
      { encoding: 'utf8', timeout: 10000 }
    );
    return parseFloat(result.trim());
  } catch {
    return null;
  }
}

function buildDescription(description) {
  if (description && description.includes('━━━━━━━━━━━━━━━━━━━━━━━━━━━━')) {
    return description; // Already has the full template
  }
  return `${description || ''}${DEFAULT_DESCRIPTION_FOOTER}`;
}

async function uploadShort({ videoPath, title, description = '', tags = [], privacyStatus = 'public' }) {
  // Validate video duration
  const duration = getVideoDuration(videoPath);
  if (duration !== null) {
    if (duration < MIN_DURATION) {
      console.warn(`[upload-short] WARNING: Video is ${duration}s, below minimum ${MIN_DURATION}s`);
    }
    if (duration > MAX_DURATION) {
      console.warn(`[upload-short] WARNING: Video is ${duration}s, exceeds maximum ${MAX_DURATION}s`);
    }
  }

  const token = await getAccessToken();
  const fullDescription = buildDescription(description);

  const metadataRes = await axios.post(
    'https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status',
    {
      snippet: { title: `${title} #Shorts`, description: fullDescription, tags: [...tags, 'Shorts'] },
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
