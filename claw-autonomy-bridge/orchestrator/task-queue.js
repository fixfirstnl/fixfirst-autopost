'use strict';
const { v4: uuidv4 } = require('uuid');

const queue = [];
const running = new Map();

function enqueue(task) {
  const id = uuidv4();
  const item = { id, ...task, status: 'pending', createdAt: new Date().toISOString() };
  queue.push(item);
  queue.sort((a, b) => (a.priority || 5) - (b.priority || 5));
  return id;
}

function dequeue() {
  const item = queue.shift();
  if (item) {
    item.status = 'running';
    running.set(item.id, item);
  }
  return item;
}

function complete(id, result) {
  const item = running.get(id);
  if (item) {
    item.status = 'completed';
    item.result = result;
    item.completedAt = new Date().toISOString();
    running.delete(id);
  }
  return item;
}

function fail(id, error) {
  const item = running.get(id);
  if (item) {
    item.status = 'failed';
    item.error = error;
    item.failedAt = new Date().toISOString();
    running.delete(id);
  }
  return item;
}

function getStatus() {
  return {
    pending: queue.length,
    running: running.size,
    queue: queue.slice(0, 10),
    runningTasks: Array.from(running.values())
  };
}

module.exports = { enqueue, dequeue, complete, fail, getStatus };
