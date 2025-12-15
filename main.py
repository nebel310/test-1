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
        "message": "Design Patterns API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True
    )