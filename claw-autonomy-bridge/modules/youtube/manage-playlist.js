'use strict';
const { createClient } = require('./youtube-client');

async function addToPlaylist({ videoId, playlistId }) {
  const client = await createClient();
  const res = await client.post('/playlistItems?part=snippet', {
    snippet: { playlistId, resourceId: { kind: 'youtube#video', videoId } }
  });
  return res.data;
}

async function createPlaylist({ title, description, privacyStatus = 'public' }) {
  const client = await createClient();
  const res = await client.post('/playlists?part=snippet,status', {
    snippet: { title, description },
    status: { privacyStatus }
  });
  return res.data;
}

module.exports = { addToPlaylist, createPlaylist };
