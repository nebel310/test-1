from fastapi import FastAPI
import uvicorn
from config import settings
from api import router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

app.include_router(router, prefix=settings.API_PREFIX)

@app.get("/")
async def root():
    return {
        "message": "Behavioral & Structural Patterns API",
        "patterns": ["Strategy", "Chain of Responsibility", "Iterator", "Proxy", "Bridge", "Adapter"],
        "docs": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True
    )