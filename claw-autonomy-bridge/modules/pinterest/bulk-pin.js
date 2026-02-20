'use strict';
const { createPin } = require('./create-pin');

async function bulkCreatePins(pins) {
  const results = [];
  for (const pin of pins) {
    try {
      const result = await createPin(pin);
      results.push({ success: true, pin, result });
      await new Promise(r => setTimeout(r, 1000));
    } catch (err) {
      results.push({ success: false, pin, error: err.message });
    }
  }
  return {
    total: pins.length,
    succeeded: results.filter(r => r.success).length,
    failed: results.filter(r => !r.success).length,
    results
  };
}

module.exports = { bulkCreatePins };
