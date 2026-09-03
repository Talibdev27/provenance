from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import documents

settings = get_settings()

app = FastAPI(title="Provenance API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router)


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "provenance-api"}
