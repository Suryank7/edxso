from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.endpoints import router
from backend.app.db.database import init_db

app = FastAPI(
    title="Scholarship Intelligence Crawler API",
    description="Backend AI-powered intelligence engine for discovering, crawling, verifying, scoring, and tracking scholarship opportunities for Indian students.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_db_check():
    init_db()

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
