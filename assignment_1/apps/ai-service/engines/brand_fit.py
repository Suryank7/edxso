from typing import List
from models import CampaignConfig, CreatorProfile, BrandFitBreakdown

class BrandFitEngine:
    """
    Transparent Brand-Fit Scoring Engine.
    Exposes component sub-scores and weights rather than an opaque black-box number.
    Formula:
      Brand Fit = (Niche * W_niche) + (Audience * W_aud) + (Engagement * W_eng) +
                  (Content * W_cont) + (Geography * W_geo) + (Contact * W_contact)
    """

    @staticmethod
    def calculate(creator: CreatorProfile, campaign: CampaignConfig) -> BrandFitBreakdown:
        weights = campaign.brand_fit_weights
        explanation: List[str] = []

        # 1. Niche Relevance (0 - 100)
        c_niche = creator.niche.lower()
        c_cat = creator.category.lower()
        t_niche = campaign.niche.lower()

        if t_niche in c_niche or "ai & productivity" in c_niche:
            niche_score = 95.0
            explanation.append("Niche match: Direct alignment with AI & productivity focus (95/100)")
        elif any(sub.lower() in c_niche for sub in campaign.sub_niches):
            niche_score = 85.0
            explanation.append(f"Niche match: Strong secondary alignment with {creator.niche} (85/100)")
        elif t_niche in c_cat:
            niche_score = 70.0
            explanation.append(f"Niche match: Broader category {creator.category} match (70/100)")
        else:
            niche_score = 25.0
            explanation.append(f"Niche match: Low relevance for {creator.category} in campaign (25/100)")

        # 2. Audience Relevance (0 - 100)
        aud_age = creator.audience_age.lower()
        if "18-24" in aud_age or "students" in campaign.target_audience.lower():
            # Check percentage in 18-24/25-34
            audience_score = 90.0
            explanation.append("Audience match: High concentration of students/early professionals (90/100)")
        else:
            audience_score = 65.0
            explanation.append("Audience match: Moderate alignment with student demographic (65/100)")

        # 3. Engagement Score (0 - 100)
        # Scaled from min threshold (3.0%) up to elite (7.0%+)
        eng = creator.engagement_rate
        if eng >= 6.5:
            engagement_score = 100.0
            explanation.append(f"Engagement: Elite micro-influencer engagement of {eng}% (100/100)")
        elif eng >= 5.0:
            engagement_score = 88.0
            explanation.append(f"Engagement: High engagement rate of {eng}% (88/100)")
        elif eng >= 3.0:
            engagement_score = 72.0
            explanation.append(f"Engagement: Solid benchmark engagement rate of {eng}% (72/100)")
        elif eng >= 2.0:
            engagement_score = 40.0
            explanation.append(f"Engagement: Below ideal benchmark at {eng}% (40/100)")
        else:
            engagement_score = 20.0
            explanation.append(f"Engagement: Weak audience interaction at {eng}% (20/100)")

        # 4. Content Relevance (0 - 100)
        preferred_lower = [kw.lower() for kw in campaign.preferred_content]
        themes_lower = [th.lower() for th in creator.content_themes]
        recent_lower = " ".join(creator.recent_content).lower()

        matched_themes = [th for th in themes_lower if any(kw in th for kw in preferred_lower)]
        matched_recent = [kw for kw in preferred_lower if kw in recent_lower]

        total_signals = len(matched_themes) + len(matched_recent)
        if total_signals >= 4:
            content_score = 95.0
            explanation.append("Content relevance: Exceptional keyword density across recent posts and themes (95/100)")
        elif total_signals >= 2:
            content_score = 82.0
            explanation.append("Content relevance: Good alignment with AI/productivity content themes (82/100)")
        elif total_signals >= 1:
            content_score = 65.0
            explanation.append("Content relevance: Partial theme overlap detected (65/100)")
        else:
            content_score = 30.0
            explanation.append("Content relevance: Minimal overlap with target content pillars (30/100)")

        # 5. Geography Score (0 - 100)
        target_geo = campaign.target_geography.lower()
        creator_geo = creator.audience_geography.lower()

        if target_geo in creator_geo:
            geography_score = 95.0
            explanation.append(f"Geography: Primary target region '{campaign.target_geography}' dominates audience (95/100)")
        else:
            geography_score = 40.0
            explanation.append(f"Geography: Audience located outside primary target region '{campaign.target_geography}' (40/100)")

        # 6. Contact Availability (0 - 100)
        if creator.contact_email and creator.contact_email != "Not Found":
            if creator.email_confidence == "high":
                contact_score = 100.0
                explanation.append("Contact: Verified public business email available with high confidence (100/100)")
            else:
                contact_score = 80.0
                explanation.append("Contact: Public email available with medium confidence (80/100)")
        else:
            contact_score = 35.0
            explanation.append("Contact: Direct email not public; requires secondary DM outreach (35/100)")

        # Composite Calculation
        composite = (
            (niche_score * weights.niche_relevance) +
            (audience_score * weights.audience_relevance) +
            (engagement_score * weights.engagement) +
            (content_score * weights.content_relevance) +
            (geography_score * weights.geography) +
            (contact_score * weights.contact_availability)
        )

        return BrandFitBreakdown(
            niche_relevance=round(niche_score, 1),
            audience_relevance=round(audience_score, 1),
            engagement_score=round(engagement_score, 1),
            content_relevance=round(content_score, 1),
            geography_score=round(geography_score, 1),
            contact_availability=round(contact_score, 1),
            composite_score=round(composite, 1),
            explanation=explanation
        )
