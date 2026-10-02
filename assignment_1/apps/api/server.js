const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const { v4: uuidv4 } = require('uuid');

dotenv.config();

const store = require('./data/store');
const OutreachService = require('./services/outreachService');
const OrchestrationService = require('./services/orchestrationService');

const app = express();
const PORT = process.env.PORT || process.env.PORT_GATEWAY || 5000;

app.use(cors());
app.use(express.json());

// Structured Request Logger Middleware
app.use((req, res, next) => {
  const traceId = uuidv4().substring(0, 8);
  req.traceId = traceId;
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(JSON.stringify({
      trace_id: traceId,
      method: req.method,
      url: req.originalUrl,
      status: res.statusCode,
      duration_ms: duration,
      timestamp: new Date().toISOString()
    }));
  });
  next();
});

// 1. Health Check
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'edxso-api-gateway',
    version: '1.0.0',
    dry_run_mode: process.env.DRY_RUN !== 'false',
    ai_service_url: process.env.AI_SERVICE_URL || 'http://localhost:8000'
  });
});

// 2. Campaign Management
app.get('/api/v1/campaigns', (req, res) => {
  res.json(store.getCampaigns());
});

app.post('/api/v1/campaigns', (req, res) => {
  const {
    campaign_name,
    brand,
    niche = 'Technology',
    sub_niches = ['AI & Productivity', 'Developer Tools'],
    target_platforms = ['Instagram', 'YouTube'],
    min_followers = 5000,
    max_followers = 100000,
    min_engagement_rate = 3.0,
    target_geography = 'India',
    target_audience = 'Students and software developers',
    preferred_content = ['AI tools', 'productivity', 'coding tutorials'],
    collaboration_type = 'Sponsored Content'
  } = req.body;

  if (!campaign_name || !brand) {
    return res.status(400).json({ error: 'campaign_name and brand are required fields.' });
  }

  const newCampaign = {
    campaign_id: `camp_${uuidv4().substring(0, 8)}`,
    campaign_name,
    brand,
    niche,
    sub_niches,
    target_platforms,
    min_followers: Number(min_followers),
    max_followers: Number(max_followers),
    min_engagement_rate: Number(min_engagement_rate),
    target_geography,
    target_audience,
    preferred_content,
    collaboration_type,
    created_at: new Date().toISOString(),
    status: 'ACTIVE',
    enriched_creators: []
  };

  store.saveCampaign(newCampaign);
  res.status(201).json(newCampaign);
});

app.get('/api/v1/campaigns/:id', (req, res) => {
  const campaign = store.getCampaignById(req.params.id);
  if (!campaign) {
    return res.status(404).json({ error: 'Campaign not found' });
  }
  res.json(campaign);
});

// 3. Discovery & Evaluation Pipeline Trigger
app.post('/api/v1/campaigns/:id/discover', async (req, res) => {
  try {
    const result = await OrchestrationService.discoverAndEvaluate(req.params.id);
    res.json(result);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 4. Creators Listing for a Campaign
app.get('/api/v1/campaigns/:id/creators', (req, res) => {
  const campaign = store.getCampaignById(req.params.id);
  if (!campaign) {
    return res.status(404).json({ error: 'Campaign not found' });
  }
  res.json(campaign.enriched_creators || []);
});

// 5. Human-in-the-Loop Review Update
app.patch('/api/v1/campaigns/:id/creators/:creatorId/review', (req, res) => {
  try {
    const updated = OrchestrationService.updateCreatorReview(
      req.params.id,
      req.params.creatorId,
      req.body
    );
    res.json(updated);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// 6. Outreach Dispatch (Single)
app.post('/api/v1/outreach/send', async (req, res) => {
  try {
    const result = await OutreachService.sendOutreach(req.body);
    res.json(result);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 7. Outreach Dispatch (Batch)
app.post('/api/v1/outreach/batch-send', async (req, res) => {
  try {
    const result = await OutreachService.batchSend(req.body);
    res.json(result);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 8. Outreach Tracker Logs
app.get('/api/v1/outreach', (req, res) => {
  const campaignId = req.query.campaign_id;
  const records = store.getOutreachRecords(campaignId);
  res.json(records);
});

// 9. Campaign Analytics Dashboard
app.get('/api/v1/campaigns/:id/analytics', (req, res) => {
  try {
    const analytics = OrchestrationService.getCampaignAnalytics(req.params.id);
    res.json(analytics);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`[EDXSO Gateway] API Gateway listening on port ${PORT}`);
  console.log(`[EDXSO Gateway] Dry-Run Mode: ${process.env.DRY_RUN !== 'false' ? 'ENABLED (Simulation)' : 'DISABLED (Live SMTP)'}`);
});

module.exports = app;
