# Project Creation Flow Todo

## 1. Foundations
- [ ] Confirm scope vs PRD goals (Phase 1 only)
- [x] Review tech constraints and lock stack
- [x] Define data scope: subreddits, events, keywords, polling interval
- [x] Draft API response schemas (raw vs aggregated)
- [x] Set data retention policy for raw vs aggregated metrics

## 2. Repository & Structure
- [x] Create repo structure: backend/, frontend/, docs/, infra/
- [x] Add base README with setup and run steps
- [x] Add .env.example for backend and frontend
- [x] Add Docker and docker-compose skeleton

## 3. Backend (FastAPI)
- [x] Scaffold FastAPI app structure
- [x] Configure settings management via environment variables
- [x] Implement Reddit API client (polling)
- [x] Implement ingestion scheduler (5-min default)
- [x] Define database models: posts, comments, sentiment, trends
- [x] Build persistence layer (single DB)
- [x] Seed keywords/events and map event_keywords
- [x] Implement first-class event analytics via event mappings
- [x] Create NLP pipeline: lightweight sentiment scoring
- [x] Implement trend analysis: keyword frequency + spike detection
- [x] Create REST endpoints for raw data
- [x] Create REST endpoints for aggregated analytics
- [x] Add health/status endpoint
- [x] Add tests for ingestion and analytics modules

## 4. Frontend (React + Vite + Tailwind)
- [x] Scaffold Next.js App Router app
- [x] Install and configure Tailwind CSS
- [x] Add Next.js routes:
  - [x] /dashboard
  - [x] /trends
  - [x] /sentiment
  - [x] /subreddits/:name
  - [x] /events/:eventId
  - [x] /about
- [x] Build shared layout: sidebar + top bar + content shell
- [x] Implement reusable cards, badges, and metric tiles
- [x] Implement breadcrumbs for hierarchical pages
- [x] Create mock API service with realistic schemas
- [x] Create custom hooks: fetching, loading, error, polling
- [x] Build charts using Recharts (no hardcoded data)
- [x] Implement dashboard page (sentiment + volume + trending)
- [x] Implement trends page (frequency + spikes)
- [x] Implement sentiment page (distribution + timeline)
- [x] Implement subreddit view page (per-subreddit metrics)
- [x] Implement event monitoring page (keyword tracking)
- [x] Implement system info/about page

## 5. Integration
- [x] Wire frontend to backend API endpoints
- [ ] Validate data schemas match UI expectations
- [ ] Add error and empty-state UI
- [ ] Add refresh timestamp and status in header

## 6. Deployment & Ops
- [x] Finalize Dockerfiles for backend and frontend
- [x] Add docker-compose for local dev
- [ ] Add production build instructions
- [ ] Configure environment variables for DigitalOcean
- [ ] Document deployment steps

## 7. QA & Review
- [x] Run backend smoke test
- [ ] Run end-to-end smoke test
- [ ] Run frontend smoke test
- [ ] Verify polling interval and data freshness
- [ ] Validate trend spikes against known events
- [ ] Check UI against design goals
- [ ] Confirm ethical constraints and data handling
