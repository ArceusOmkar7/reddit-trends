from fastapi import APIRouter

from app.api.routes.analytics import router as analytics_router
from app.api.routes.health import router as health_router
from app.api.routes.raw import router as raw_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(raw_router, tags=["raw"])
api_router.include_router(analytics_router, tags=["analytics"])
