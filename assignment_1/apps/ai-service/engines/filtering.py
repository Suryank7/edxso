from typing import List, Tuple
from models import CampaignConfig, CreatorProfile, FilterEvaluation

class FilteringEngine:
    """
    Configurable filtering and qualification engine.
    Evaluates creator profiles against campaign rules and produces
    transparent, human-readable PASS/FAIL explanations.
    """

    @staticmethod
    def evaluate(creator: CreatorProfile, campaign: CampaignConfig) -> FilterEvaluation:
        reasons: List[str] = []
        passed_count = 0
        total_criteria = 5 # Followers, Engagement, Niche, Platform, Content Relevance

        # 1. Follower count criterion
        if campaign.min_followers <= creator.follower_count <= campaign.max_followers:
            reasons.append(f"✓ {creator.follower_count:,} followers within target micro-influencer range ({campaign.min_followers:,} - {campaign.max_followers:,})")
            passed_count += 1
            follower_pass = True
        elif creator.follower_count < campaign.min_followers:
            reasons.append(f"✗ {creator.follower_count:,} followers below minimum threshold of {campaign.min_followers:,} (Nano influencer)")
            follower_pass = False
        else:
            reasons.append(f"✗ {creator.follower_count:,} followers exceeds maximum ceiling of {campaign.max_followers:,} (Macro influencer)")
            follower_pass = False

        # 2. Engagement rate criterion
        if creator.engagement_rate >= campaign.min_engagement_rate:
            reasons.append(f"✓ {creator.engagement_rate}% engagement rate satisfies minimum {campaign.min_engagement_rate}% benchmark")
            passed_count += 1
            engagement_pass = True
        else:
            reasons.append(f"✗ {creator.engagement_rate}% engagement rate falls below required {campaign.min_engagement_rate}% threshold")
            engagement_pass = False

        # 3. Niche / Category criterion
        campaign_niche_lower = campaign.niche.lower()
        creator_cat_lower = creator.category.lower()
        creator_niche_lower = creator.niche.lower()
        
        niche_matches = (
            campaign_niche_lower in creator_cat_lower or
            campaign_niche_lower in creator_niche_lower or
            any(sub.lower() in creator_niche_lower for sub in campaign.sub_niches)
        )
        
        if niche_matches:
            reasons.append(f"✓ Category '{creator.category}' and niche '{creator.niche}' match target niche '{campaign.niche}'")
            passed_count += 1
            niche_pass = True
        else:
            reasons.append(f"✗ Niche '{creator.niche}' ({creator.category}) is unrelated to target campaign niche '{campaign.niche}'")
            niche_pass = False

        # 4. Platform criterion
        platform_matches = any(p.lower() == creator.platform.lower() for p in campaign.target_platforms)
        if platform_matches:
            reasons.append(f"✓ Platform '{creator.platform}' matches designated campaign channels")
            passed_count += 1
            platform_pass = True
        else:
            reasons.append(f"✗ Platform '{creator.platform}' not in targeted campaign channels ({', '.join(campaign.target_platforms)})")
            platform_pass = False

        # 5. Content relevance signals
        preferred_lower = [kw.lower() for kw in campaign.preferred_content]
        creator_content_blob = " ".join(creator.content_themes + creator.recent_content).lower()
        matching_signals = [kw for kw in preferred_lower if kw in creator_content_blob]

        if matching_signals:
            reasons.append(f"✓ Relevant content signals detected: {', '.join(matching_signals[:3])}")
            passed_count += 1
            content_pass = True
        else:
            reasons.append("✗ No matching keywords found in recent content or content themes")
            content_pass = False

        # Informational checks (Geography & Contact Email)
        if campaign.target_geography.lower() in creator.audience_geography.lower():
            reasons.append(f"ℹ Target geography '{campaign.target_geography}' confirmed in audience demographics ({creator.audience_geography})")
        else:
            reasons.append(f"ℹ Geography '{creator.audience_geography}' differs from primary target '{campaign.target_geography}'")

        if creator.contact_email and creator.contact_email != "Not Found":
            reasons.append(f"ℹ Public business email available ({creator.contact_email}) with {creator.email_confidence} confidence")
        else:
            reasons.append("ℹ Public business email not listed; social DM required for primary contact")

        # Mandatory hard qualifications: Follower count, Engagement rate, and Niche must pass
        status = "PASS" if (follower_pass and engagement_pass and niche_pass and platform_pass) else "FAIL"

        return FilterEvaluation(
            status=status,
            reasons=reasons,
            criteria_passed=passed_count,
            criteria_total=total_criteria
        )
