# Phase 2 Project Flow Todo

## 1. Foundations
- [ ] Confirm Phase 2 scope vs PRD goals
- [ ] Reconfirm tech stack constraints (vaderSentiment, nltk, SQLite)
- [ ] Define success metrics for signal quality
- [ ] Review Phase 1 data schema and migration needs

## 2. Backend – Intelligence Upgrade
- [ ] Add vaderSentiment and nltk dependencies
- [ ] Add NLP resource initialization (tokenizer + stopwords)
- [ ] Implement post-level sentiment scoring with vaderSentiment
- [ ] Store post-level sentiment in SQLite (additive columns/tables)
- [ ] Update sentiment aggregation to use new scores
- [ ] Build time-window trend detection (current vs previous window)
- [ ] Add engagement-weighted trend metrics
- [ ] Add emerging topic detection (unigrams/bigrams + filtering)
- [ ] Add event intelligence metrics (top posts, leading subs, lifecycle)
- [ ] Add/extend analytics endpoints (emerging topics, trend deltas)
- [ ] Add migrations/backfill logic at startup (no Alembic)

## 3. Backend – Testing
- [ ] Unit tests for sentiment scoring
- [ ] Unit tests for trend windowing and weighting
- [ ] Unit tests for emerging topic detection
- [ ] Regression tests for Phase 1 endpoints

## 4. Frontend – UX Enhancements
- [ ] Add trend direction indicators
- [ ] Add sentiment shift annotations
- [ ] Separate tracked vs emerging topics
- [ ] Add tooltips explaining trend metrics
- [ ] Improve event page explainability (top posts, leading subs)

## 5. Data Migration & Compatibility
- [ ] Verify additive schema changes
- [ ] Ensure Phase 1 dashboards still render
- [ ] Backfill post-level sentiment where possible
- [ ] Recompute trends from stored posts

## 6. QA & Validation
- [ ] Compare Phase 1 vs Phase 2 outputs on known events
- [ ] Manual inspection of trend timelines
- [ ] Verify emerging topics are relevant
- [ ] Validate event intelligence explanations
- [ ] Performance check (single-node)

## Phase 2
- [ ] Phase 2 complete and documented
