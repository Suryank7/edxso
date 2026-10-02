import os
import json
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from models import (
    CampaignConfig, CreatorProfile, FilterEvaluation,
    BrandFitBreakdown, PersonalizationResult, EnrichedCreator,
    FilterRequest, PersonalizationRequest, BatchPersonalizationRequest
)
from engines import FilteringEngine, BrandFitEngine, PersonalizationEngine

app = FastAPI(
    title="EDXSO Influencer AI Service",
    description="Micro-Influencer Discovery, Filtering, Brand-Fit & AI Personalization Engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SEED_FILE_PATH = os.path.join(os.path.dirname(__file__), "data", "creators_seed.json")

def load_seed_creators() -> List[CreatorProfile]:
    if not os.path.exists(SEED_FILE_PATH):
        raise FileNotFoundError(f"Seed file not found at {SEED_FILE_PATH}")
    with open(SEED_FILE_PATH, "r", encoding="utf-8") as f:
        raw_list = json.load(f)
    return [CreatorProfile(**item) for item in raw_list]

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "edxso-ai-service",
        "version": "1.0.0",
        "llm_gemini_active": bool(os.getenv("GEMINI_API_KEY")),
        "llm_openai_active": bool(os.getenv("OPENAI_API_KEY"))
    }

@app.get("/api/v1/creators", response_model=List[CreatorProfile])
def get_all_creators(limit: int = Query(60, ge=1, le=100)):
    creators = load_seed_creators()
    return creators[:limit]

@app.post("/api/v1/filter")
def filter_creators(req: FilterRequest):
    creators = req.creators or load_seed_creators()
    results = []
    for creator in creators:
        eval_res = FilteringEngine.evaluate(creator, req.campaign)
        results.append({
            "creator_id": creator.creator_id,
            "name": creator.name,
            "status": eval_res.status,
            "reasons": eval_res.reasons,
            "criteria_passed": eval_res.criteria_passed,
            "criteria_total": eval_res.criteria_total
        })
    return {"campaign_id": req.campaign.campaign_id, "evaluations": results}

@app.post("/api/v1/brand-fit")
def calculate_brand_fit(creator: CreatorProfile, campaign: CampaignConfig):
    fit = BrandFitEngine.calculate(creator, campaign)
    return fit

@app.post("/api/v1/personalize", response_model=PersonalizationResult)
def personalize_single(req: PersonalizationRequest):
    return PersonalizationEngine.generate(req.creator, req.campaign)

@app.post("/api/v1/personalize/batch")
def personalize_batch(req: BatchPersonalizationRequest):
    results = {}
    for creator in req.creators:
        results[creator.creator_id] = PersonalizationEngine.generate(creator, req.campaign)
    return results

@app.post("/api/v1/pipeline/evaluate", response_model=List[EnrichedCreator])
def run_full_pipeline(campaign: CampaignConfig):
    """
    Executes the complete AI discovery & qualification pipeline:
    1. Ingestion: Reads all 50+ micro-influencer profiles
    2. Filtering: Applies follower, engagement, niche, and content filters with explainable pass/fail
    3. Brand-Fit: Computes transparent 6-factor weighted brand fit score
    4. Personalization: Generates grounded 60-90 word email and 15-30 word DM for qualified creators
    """
    creators = load_seed_creators()
    enriched_results: List[EnrichedCreator] = []

    for c in creators:
        filter_eval = FilteringEngine.evaluate(c, campaign)
        brand_fit = BrandFitEngine.calculate(c, campaign)
        
        # Only personalize qualified or high-scoring creators to optimize resources
        personalization = None
        if filter_eval.status == "PASS":
            personalization = PersonalizationEngine.generate(c, campaign)

        enriched_results.append(EnrichedCreator(
            profile=c,
            filter_evaluation=filter_eval,
            brand_fit=brand_fit,
            personalization=personalization,
            review_status="Auto-generated",
            outreach_status="Pending"
        ))

    return enriched_results

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT_AI_SERVICE", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
