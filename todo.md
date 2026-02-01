# Project Creation Flow Todo

## 1. Foundations
- [ ] Confirm scope vs PRD goals (Phase 1 only)
- [ ] Review tech constraints and lock stack
- [ ] Define data scope: subreddits, events, keywords, polling interval
- [ ] Draft API response schemas (raw vs aggregated)
- [ ] Set data retention policy for raw vs aggregated metrics

## 2. Repository & Structure
- [ ] Create repo structure: backend/, frontend/, docs/, infra/
- [ ] Add base README with setup and run steps
- [ ] Add .env.example for backend and frontend
- [ ] Add Docker and docker-compose skeleton

## 3. Backend (FastAPI)
- [ ] Scaffold FastAPI app structure
- [ ] Configure settings management via environment variables
- [ ] Implement Reddit API client (polling)
- [ ] Implement ingestion scheduler (5-min default)
- [ ] Define database models: posts, comments, sentiment, trends
- [ ] Build persistence layer (single DB)
- [ ] Create NLP pipeline: lightweight sentiment scoring
- [ ] Implement trend analysis: keyword frequency + spike detection
- [ ] Create REST endpoints for raw data
- [ ] Create REST endpoints for aggregated analytics
- [ ] Add health/status endpoint
- [ ] Add tests for ingestion and analytics modules

## 4. Frontend (React + Vite + Tailwind)
- [ ] Scaffold Vite React app
- [ ] Install and configure Tailwind CSS
- [ ] Add React Router routes:
  - [ ] /dashboard
  - [ ] /trends
  - [ ] /sentiment
  - [ ] /subreddits/:name
  - [ ] /events/:eventId
  - [ ] /about
- [ ] Build shared layout: sidebar + top bar + content shell
- [ ] Implement reusable cards, badges, and metric tiles
- [ ] Implement breadcrumbs for hierarchical pages
- [ ] Create mock API service with realistic schemas
- [ ] Create custom hooks: fetching, loading, error, polling
- [ ] Build charts using Recharts or Chart.js (no hardcoded data)
- [ ] Implement dashboard page (sentiment + volume + trending)
- [ ] Implement trends page (frequency + spikes)
- [ ] Implement sentiment page (distribution + timeline)
- [ ] Implement subreddit view page (per-subreddit metrics)
- [ ] Implement event monitoring page (keyword tracking)
- [ ] Implement system info/about page

## 5. Integration
- [ ] Wire frontend to backend API endpoints
- [ ] Validate data schemas match UI expectations
- [ ] Add error and empty-state UI
- [ ] Add refresh timestamp and status in header

## 6. Deployment & Ops
- [ ] Finalize Dockerfiles for backend and frontend
- [ ] Add docker-compose for local dev
- [ ] Add production build instructions
- [ ] Configure environment variables for DigitalOcean
- [ ] Document deployment steps

## 7. QA & Review
- [ ] Run end-to-end smoke test
- [ ] Verify polling interval and data freshness
- [ ] Validate trend spikes against known events
- [ ] Check UI against design goals
- [ ] Confirm ethical constraints and data handling
