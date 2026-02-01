import asyncio

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.db.database import init_db
from app.services.ingestion import poll_reddit
from app.services.scheduler import run_interval

app = FastAPI(title=settings.app_name, version=settings.app_version)
app.include_router(api_router)


@app.on_event("startup")
async def start_ingestion() -> None:
	init_db()
	if not settings.enable_ingestion:
		return

	async def task() -> None:
		await poll_reddit()

	asyncio.create_task(run_interval(task, settings.poll_interval_seconds))
