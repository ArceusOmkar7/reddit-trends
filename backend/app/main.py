import asyncio
import logging
import sys
from datetime import datetime, timedelta, timezone
from logging.handlers import RotatingFileHandler
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.db.database import init_db
from app.services.ingestion import poll_reddit
from app.services.nlp import ensure_nltk_resources
from app.services.sentiment import backfill_post_sentiment
from app.services.trends import (
	fetch_posts_since,
	detect_trends,
	detect_emerging_topics,
	detect_trends_for_window,
	detect_emerging_topics_for_window,
)
from app.repositories.trends import store_trends
from app.repositories.emerging_topics import store_emerging_topic_snapshots
from app.services.scheduler import run_interval, set_ingestion_enabled

@asynccontextmanager
async def lifespan(_: FastAPI):
	log_format = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
	root_logger = logging.getLogger()
	root_logger.setLevel(logging.INFO)

	if not any(isinstance(handler, RotatingFileHandler) for handler in root_logger.handlers):
		log_path = Path("/app/logs")
		log_path.mkdir(parents=True, exist_ok=True)
		file_handler = RotatingFileHandler(
			log_path / "app.log",
			maxBytes=5 * 1024 * 1024,
			backupCount=5,
		)
		file_handler.setFormatter(logging.Formatter(log_format))
		root_logger.addHandler(file_handler)

	if not any(
		isinstance(handler, logging.StreamHandler)
		and getattr(handler, "stream", None) is sys.stdout
		for handler in root_logger.handlers
	):
		stream_handler = logging.StreamHandler(sys.stdout)
		stream_handler.setFormatter(logging.Formatter(log_format))
		root_logger.addHandler(stream_handler)
	init_db()
	ensure_nltk_resources()
	while True:
		updated = backfill_post_sentiment()
		if updated == 0:
			break
	try:
		recent_posts = fetch_posts_since(2)
		if recent_posts:
			trend_records = detect_trends(recent_posts)
			if trend_records:
				store_trends(trend_records)
		emerging_records = detect_emerging_topics()
		if emerging_records:
			store_emerging_topic_snapshots(emerging_records)

		backfill_hours = max(settings.backfill_trends_hours, 0)
		if backfill_hours:
			end = datetime.now(tz=timezone.utc)
			for offset in range(backfill_hours):
				window_end = end - timedelta(hours=offset)
				trend_records = detect_trends_for_window(window_end)
				if trend_records:
					store_trends(trend_records)
				emerging_records = detect_emerging_topics_for_window(window_end)
				if emerging_records:
					store_emerging_topic_snapshots(emerging_records)
	except Exception:
		logging.getLogger("reddit_trends.startup").exception("Startup recompute failed")
	set_ingestion_enabled(settings.enable_ingestion)

	async def task() -> None:
		await poll_reddit()

	asyncio.create_task(run_interval(task, settings.poll_interval_seconds))
	yield


app = FastAPI(title=settings.app_name, version=settings.app_version, lifespan=lifespan)

allowed_origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]

app.add_middleware(
	CORSMiddleware,
	allow_origins=allowed_origins or ["http://localhost:3000"],
	allow_credentials=True,
	allow_methods=["*"] ,
	allow_headers=["*"],
)
app.include_router(api_router)
