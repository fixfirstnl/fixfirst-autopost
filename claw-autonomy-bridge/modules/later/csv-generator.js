'use strict';

function generateCSV(posts) {
  const header = 'Date,Time,Caption,Media URL,Platform';
  const rows = posts.map(p => {
    const caption = (p.caption || '').replace(/"/g, '""');
    return `"${p.date}","${p.time}","${caption}","${p.mediaUrl || ''}","${p.platform || 'instagram'}"`;
  });
  return [header, ...rows].join('\n');
}

module.exports = { generateCSV };
