const assert = require('assert');
const store = require('../data/store');
const OutreachService = require('../services/outreachService');
const OrchestrationService = require('../services/orchestrationService');

async function runTests() {
  console.log('🚀 Running EDXSO API Gateway Unit & Integration Tests...');

  // Test 1: Store loads seed creators
  const seed = store.getSeedCreators();
  assert(seed.length >= 50, `Expected at least 50 seed creators, found ${seed.length}`);
  console.log(`✓ Seed Creators Verified: ${seed.length} creators loaded`);

  // Reset outreach records for clean test run
  store.clearOutreachRecords('camp_default_001');

  // Test 2: Local fallback evaluation
  const campaign = store.getCampaignById('camp_default_001');
  assert(campaign, 'Default campaign should exist');
  
  const evalResult = OrchestrationService._fallbackLocalEvaluation(campaign);
  assert(evalResult.length >= 50, 'Evaluation should process all seed creators');
  const passed = evalResult.filter(c => c.filter_evaluation.status === 'PASS');
  const failed = evalResult.filter(c => c.filter_evaluation.status === 'FAIL');
  assert(passed.length > 0, 'Some creators must qualify');
  assert(failed.length > 0, 'Some creators must fail filters for explainability');
  console.log(`✓ Filtering Logic Verified: ${passed.length} PASS, ${failed.length} FAIL`);

  // Test 3: Human Review Update
  campaign.enriched_creators = evalResult;
  store.saveCampaign(campaign);

  const testCreator = passed[0];
  const updatedCreator = OrchestrationService.updateCreatorReview(
    campaign.campaign_id,
    testCreator.profile.creator_id,
    {
      reviewStatus: 'Human Approved',
      editedEmail: 'Hi there, this is a custom edited email pitch for testing.'
    }
  );
  assert.strictEqual(updatedCreator.review_status, 'Edited');
  assert.strictEqual(updatedCreator.personalization.email_body, 'Hi there, this is a custom edited email pitch for testing.');
  console.log('✓ Human-in-the-Loop Review Verified: Status and content updated');

  // Test 4: Outreach Simulation (DRY_RUN)
  process.env.DRY_RUN = 'true';
  const outreachRes = await OutreachService.sendOutreach({
    campaignId: campaign.campaign_id,
    creatorId: testCreator.profile.creator_id,
    creatorName: testCreator.profile.name,
    channel: 'Email',
    recipient: testCreator.profile.contact_email,
    subject: 'Collab Test',
    messageBody: 'Test Message Body'
  });
  assert(outreachRes.success === true, 'Outreach simulation should succeed');
  assert.strictEqual(outreachRes.status, 'SIMULATED');
  console.log('✓ Outreach Dispatch Verified: Dry-Run simulated successfully');

  // Test 5: Duplicate Prevention Enforcement
  const duplicateAttempt = await OutreachService.sendOutreach({
    campaignId: campaign.campaign_id,
    creatorId: testCreator.profile.creator_id,
    creatorName: testCreator.profile.name,
    channel: 'Email',
    recipient: testCreator.profile.contact_email,
    subject: 'Collab Test 2',
    messageBody: 'Duplicate Body'
  });
  assert(duplicateAttempt.success === false, 'Duplicate outreach must be blocked');
  assert.strictEqual(duplicateAttempt.duplicate_prevented, true, 'duplicate_prevented flag must be true');
  console.log('✓ Duplicate Prevention Verified: Duplicate attempt successfully blocked');

  // Test 6: Campaign Analytics Calculation
  const analytics = OrchestrationService.getCampaignAnalytics(campaign.campaign_id);
  assert(analytics.funnel.discovered >= 50, 'Discovered count >= 50');
  assert(analytics.funnel.outreach_simulated >= 1, 'Simulated count >= 1');
  assert(analytics.brand_fit_distribution.elite >= 0, 'Brand fit distribution present');
  console.log('✓ Campaign Analytics Verified: Funnel metrics accurately aggregated');

  console.log('\n🎉 ALL API GATEWAY & ORCHESTRATION TESTS PASSED!');
}

runTests().catch(err => {
  console.error('❌ Test failed:', err);
  process.exit(1);
});
