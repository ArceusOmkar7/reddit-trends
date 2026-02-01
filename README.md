# Reddit Trends Intelligence

Near real-time Reddit sentiment and trend dashboard. Phase 1 uses a single-node, polling-based pipeline with a read-only UI and local SQLite storage.

## Features
- Polls Reddit via PRAW on a schedule
- Normalized SQLite schema (3NF)
- Sentiment scoring and trend detection
- Analytics endpoints for dashboard, subreddit, and event views
- Next.js dashboard with charts, filters, and live refresh context

## Repository structure
- backend/ — FastAPI service, ingestion pipeline, SQLite persistence
- frontend/ — Next.js App Router UI with Tailwind and Recharts
- docs/ — PRD, design prompt, and tech rules
- infra/ — infra support assets

## Quick start (Docker)
1. Ensure Docker is running.
2. Configure environment variables:
	- backend/.env (copy from backend/.env.example)
	- frontend/.env (copy from frontend/.env.example)
3. Start both services:
	- docker compose up --build
4. Open the UI at http://localhost:3000.

## Local development

### Backend
See [backend/README.md](backend/README.md) for setup, running, and tests.

### Frontend
See [frontend/README.md](frontend/README.md) for setup, running, and tests.

## Production build

### Docker (recommended)
1. Configure environment variables:
	 - backend/.env (copy from backend/.env.example)
	 - frontend/.env (copy from frontend/.env.example)
2. Build and run:
	 - docker compose up --build

### Local build (no Docker)
- Backend
	- pip install -r backend/requirements.txt
	- uvicorn app.main:app --host 0.0.0.0 --port 8000
- Frontend
	- npm install
	- npm run build
	- npm run start

## Deployment checklist
1. Set production environment variables (see backend/.env.example and frontend/.env.example).
2. Ensure Reddit API keys are present (REDDIT_CLIENT_ID/SECRET/USER_AGENT).
3. Set ENABLE_INGESTION=true for polling.
4. Confirm NEXT_PUBLIC_API_BASE_URL points to the deployed backend.
5. Open ports 8000 (backend) and 3000 (frontend) or use a reverse proxy.
6. Verify /health responds and dashboard loads.

## API overview
Base URL: http://localhost:8000

- GET /health
- GET /analytics/dashboard?hours=24
- GET /analytics/sentiment?hours=24
- GET /analytics/trends?hours=24
- GET /analytics/subreddits/{name}?hours=24
- GET /analytics/events/{event_id}?hours=24
- GET /raw/posts?limit=50

## Data flow
1. Scheduler polls Reddit using configured subreddits/keywords.
2. Posts and derived metrics are stored in SQLite.
3. Analytics endpoints query aggregated tables.
4. Frontend fetches analytics and renders charts.

## Troubleshooting
- If charts show empty data, verify ingestion is enabled in backend env.
- If CORS errors occur, ensure frontend is on http://localhost:3000.
- If data timestamps look incorrect, confirm system time and timezone.
