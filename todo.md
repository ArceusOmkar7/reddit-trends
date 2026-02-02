# Phase 2 Project Flow Todo

## 1. Foundations
- [x] Confirm Phase 2 scope vs PRD goals
- [x] Reconfirm tech stack constraints (vaderSentiment, nltk, SQLite)
- [x] Define success metrics for signal quality
- [x] Review Phase 1 data schema and migration needs

## 2. Backend – Intelligence Upgrade
- [x] Add vaderSentiment and nltk dependencies
- [x] Add NLP resource initialization (tokenizer + stopwords)
- [x] Implement post-level sentiment scoring with vaderSentiment
- [x] Store post-level sentiment in SQLite (additive columns/tables)
- [x] Update sentiment aggregation to use new scores
- [x] Build time-window trend detection (current vs previous window)
- [x] Add engagement-weighted trend metrics
- [x] Add emerging topic detection (unigrams/bigrams + filtering)
- [x] Add event intelligence metrics (top posts, leading subs, lifecycle)
- [x] Add/extend analytics endpoints (emerging topics, trend deltas)
- [x] Add migrations/backfill logic at startup (no Alembic)

## 3. Backend – Testing
- [x] Unit tests for sentiment scoring
- [x] Unit tests for trend windowing and weighting
- [x] Unit tests for emerging topic detection
- [x] Regression tests for Phase 1 endpoints

## 4. Frontend – UX Enhancements
- [ ] Add trend direction indicators
- [ ] Add sentiment shift annotations
- [ ] Separate tracked vs emerging topics
- [ ] Add tooltips explaining trend metrics
- [ ] Improve event page explainability (top posts, leading subs)

## 5. Data Migration & Compatibility
- [x] Verify additive schema changes
- [ ] Ensure Phase 1 dashboards still render
- [x] Backfill post-level sentiment where possible
- [x] Recompute trends from stored posts

## 6. QA & Validation
- [ ] Compare Phase 1 vs Phase 2 outputs on known events
- [ ] Manual inspection of trend timelines
- [ ] Verify emerging topics are relevant
- [ ] Validate event intelligence explanations
- [ ] Performance check (single-node)

## Phase 2
- [ ] Phase 2 complete and documented
