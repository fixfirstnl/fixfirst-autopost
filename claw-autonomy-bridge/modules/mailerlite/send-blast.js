'use strict';
const { createClient } = require('./mailerlite-client');

async function sendBlast({ subject, htmlContent, groupIds, fromName, fromEmail }) {
  const client = createClient();
  const campaign = await client.post('/campaigns', {
    name: subject,
    type: 'regular',
    emails: [{
      subject,
      from_name: fromName || 'FixFirst',
      from: fromEmail || 'hello@fixfirst.nl',
      content: htmlContent
    }],
    groups: (groupIds || [process.env.MAILERLITE_GROUP_ID]).map(id => ({ id }))
  });
  const campaignId = campaign.data.data.id;
  const result = await client.post(`/campaigns/${campaignId}/schedule`, { delivery: 'instant' });
  return { campaignId, ...result.data };
}

module.exports = { sendBlast };
