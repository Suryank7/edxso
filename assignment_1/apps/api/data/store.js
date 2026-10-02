const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, '../../data');
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

const CAMPAIGNS_FILE = path.join(DATA_DIR, 'campaigns.json');
const OUTREACH_FILE = path.join(DATA_DIR, 'outreach_records.json');
const SEED_FILE = path.join(__dirname, 'creators_seed.json');

// Initialize store files
function readJSON(file, defaultVal = []) {
  try {
    if (fs.existsSync(file)) {
      return JSON.parse(fs.readFileSync(file, 'utf-8'));
    }
  } catch (err) {
    console.error(`Error reading ${file}:`, err);
  }
  return defaultVal;
}

function writeJSON(file, data) {
  try {
    fs.writeFileSync(file, JSON.stringify(data, null, 2), 'utf-8');
  } catch (err) {
    console.error(`Error writing ${file}:`, err);
  }
}

// In-memory cache for ultra-fast access
let campaigns = readJSON(CAMPAIGNS_FILE, [
  {
    campaign_id: 'camp_default_001',
    campaign_name: 'AI Productivity SaaS Launch',
    brand: 'EDXSO AI',
    niche: 'Technology',
    sub_niches: ['AI & Productivity', 'Web Development', 'Student Productivity', 'Developer Tools'],
    target_platforms: ['Instagram', 'YouTube'],
    min_followers: 5000,
    max_followers: 100000,
    min_engagement_rate: 3.0,
    target_geography: 'India',
    target_audience: 'Students and software developers',
    preferred_content: ['AI tools', 'productivity', 'coding tutorials', 'workflow hacks'],
    collaboration_type: 'Sponsored Content / Dedicated Video',
    created_at: new Date().toISOString(),
    status: 'ACTIVE',
    enriched_creators: [] // Holds enriched creator records for this campaign
  }
]);

let outreachRecords = readJSON(OUTREACH_FILE, []);

module.exports = {
  getCampaigns: () => campaigns,
  getCampaignById: (id) => campaigns.find(c => c.campaign_id === id),
  saveCampaign: (campaign) => {
    const idx = campaigns.findIndex(c => c.campaign_id === campaign.campaign_id);
    if (idx >= 0) {
      campaigns[idx] = { ...campaigns[idx], ...campaign, updated_at: new Date().toISOString() };
    } else {
      campaigns.push({ ...campaign, created_at: new Date().toISOString(), updated_at: new Date().toISOString() });
    }
    writeJSON(CAMPAIGNS_FILE, campaigns);
    return campaign;
  },
  getOutreachRecords: (campaignId) => {
    if (campaignId) {
      return outreachRecords.filter(r => r.campaign_id === campaignId);
    }
    return outreachRecords;
  },
  saveOutreachRecord: (record) => {
    const idx = outreachRecords.findIndex(r => r.outreach_id === record.outreach_id);
    if (idx >= 0) {
      outreachRecords[idx] = { ...outreachRecords[idx], ...record };
    } else {
      outreachRecords.unshift(record);
    }
    writeJSON(OUTREACH_FILE, outreachRecords);
    return record;
  },
  getSeedCreators: () => {
    return readJSON(SEED_FILE, []);
  },
  clearOutreachRecords: (campaignId) => {
    if (campaignId) {
      outreachRecords = outreachRecords.filter(r => r.campaign_id !== campaignId);
    } else {
      outreachRecords = [];
    }
    writeJSON(OUTREACH_FILE, outreachRecords);
  }
};
