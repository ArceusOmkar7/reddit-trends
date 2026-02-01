import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.db.database import init_db
from app.services.ingestion import poll_reddit
from app.services.scheduler import run_interval

@asynccontextmanager
async def lifespan(_: FastAPI):
	init_db()
	if settings.enable_ingestion:
		async def task() -> None:
			await poll_reddit()

		asyncio.create_task(run_interval(task, settings.poll_interval_seconds))
		yield
	else:
		yield


app = FastAPI(title=settings.app_name, version=settings.app_version, lifespan=lifespan)
app.include_router(api_router)
