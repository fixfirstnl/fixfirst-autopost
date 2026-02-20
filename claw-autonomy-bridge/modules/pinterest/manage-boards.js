'use strict';
const { createClient } = require('./pinterest-client');

async function createBoard({ name, description, privacy = 'PUBLIC' }) {
  const client = createClient();
  const res = await client.post('/boards', { name, description, privacy });
  return res.data;
}

async function listBoards() {
  const client = createClient();
  const res = await client.get('/boards');
  return res.data;
}

async function getBoard(boardId) {
  const client = createClient();
  const res = await client.get(`/boards/${boardId}`);
  return res.data;
}

module.exports = { createBoard, listBoards, getBoard };
