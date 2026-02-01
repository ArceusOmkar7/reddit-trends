# Reddit Trends Backend

FastAPI service that ingests Reddit content, computes sentiment/trends, and exposes analytics endpoints backed by SQLite.

## Requirements
- Python 3.11+
- pip

## Environment
Copy and edit backend/.env.example:

- REDDIT_CLIENT_ID
- REDDIT_CLIENT_SECRET
- REDDIT_USER_AGENT
- POLL_INTERVAL_SECONDS (default 300)
- DATABASE_URL (default sqlite:///./data.db)
- ENABLE_INGESTION (true/false)
- SUBREDDITS (comma-separated)
- KEYWORDS (comma-separated)

## Setup
1. Create a virtual environment.
2. Install dependencies:
   - pip install -r requirements.txt
   - pip install -r requirements-dev.txt

## Run
- uvicorn app.main:app --host 0.0.0.0 --port 8000

## Tests
- pytest

## Notes
- The service runs a polling scheduler when ENABLE_INGESTION=true.
- SQLite file defaults to backend/data.db.
