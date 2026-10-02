export interface CreatorProfile {
  creator_id: string;
  name: string;
  username: string;
  platform: 'Instagram' | 'YouTube' | string;
  profile_url: string;
  follower_count: number;
  engagement_rate: number;
  category: string;
  niche: string;
  content_themes: string[];
  contact_email: string;
  email_source: string;
  email_confidence: 'high' | 'medium' | 'unverified' | 'not_found';
  website: string;
  audience_age: string;
  audience_gender: string;
  audience_geography: string;
  recent_content: string[];
  discovery_source: string;
  posting_frequency: string;
  brand_collaborations?: string[];
}

export interface FilterEvaluation {
  status: 'PASS' | 'FAIL';
  reasons: string[];
  criteria_passed: number;
  criteria_total: number;
}

export interface BrandFitBreakdown {
  niche_relevance: number;
  audience_relevance: number;
  engagement_score: number;
  content_relevance: number;
  geography_score: number;
  contact_availability: number;
  composite_score: number;
  explanation: string[];
}

export interface GuardrailReport {
  email_word_count_compliant: boolean;
  email_word_count: number;
  dm_word_count_compliant: boolean;
  dm_word_count: number;
  zero_fabrication_checked: boolean;
  no_guessed_email_checked: boolean;
  safety_passed: boolean;
}

export interface PersonalizationResult {
  email_subject: string;
  email_body: string;
  email_word_count: number;
  dm_body: string;
  dm_word_count: number;
  personalization_signals_used: string[];
  guardrails: GuardrailReport;
}

export interface EnrichedCreator {
  profile: CreatorProfile;
  filter_evaluation: FilterEvaluation;
  brand_fit: BrandFitBreakdown;
  personalization: PersonalizationResult | null;
  review_status: 'Auto-generated' | 'Human Approved' | 'Edited' | 'Rejected' | 'Skipped';
  outreach_status: 'Pending' | 'Simulated' | 'Sent' | 'Failed' | 'Skipped';
}

export interface Campaign {
  campaign_id: string;
  campaign_name: string;
  brand: string;
  niche: string;
  sub_niches: string[];
  target_platforms: string[];
  min_followers: number;
  max_followers: number;
  min_engagement_rate: number;
  target_geography: string;
  target_audience: string;
  preferred_content: string[];
  collaboration_type: string;
  status: string;
  created_at: string;
  enriched_creators?: EnrichedCreator[];
}

export interface OutreachRecord {
  outreach_id: string;
  campaign_id: string;
  creator_id: string;
  creator_name: string;
  recipient: string;
  channel: 'Email' | 'Instagram_DM';
  subject: string;
  message_body: string;
  status: 'SIMULATED' | 'SENT' | 'FAILED' | 'SENT_MANUAL';
  sent_at: string | null;
  error?: string | null;
  retry_count: number;
  is_dry_run: boolean;
  notes?: string;
}

export interface CampaignAnalytics {
  campaign_id: string;
  campaign_name: string;
  brand: string;
  funnel: {
    discovered: number;
    qualified: number;
    rejected: number;
    enriched: number;
    messages_generated: number;
    outreach_simulated: number;
    outreach_sent: number;
    outreach_failed: number;
    duplicates_prevented: number;
  };
  brand_fit_distribution: {
    elite: number;
    high: number;
    moderate: number;
    low: number;
  };
  platform_breakdown: {
    Instagram: number;
    YouTube: number;
  };
  qualification_rate_percent: number;
  average_qualified_engagement: number;
  active_creators_count: number;
}
