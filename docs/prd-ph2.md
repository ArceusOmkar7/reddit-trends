# Product Requirements Document (PRD)
## Phase 2 – Intelligence Upgrade & Signal Quality  
**Project:** Real-Time Reddit Social Media Intelligence Platform  
**Date:** 2026-02-02  
**Phase:** 2  
**Status:** Planned  

---

## 1. Overview

### 1.1 Background
Phase 1 successfully delivered an end-to-end Reddit intelligence platform with polling-based ingestion, normalized storage, basic sentiment scoring, keyword-based trend detection, analytics APIs, and a production-ready Next.js dashboard.

However, Phase 1 intelligence is intentionally baseline:
- Sentiment relies on hardcoded lexicon rules
- Trends rely on absolute keyword frequency
- No differentiation between noise and high-impact signals
- No detection of novel or emerging topics

Phase 2 focuses on **improving signal quality and interpretability**, without changing the core architecture.

---

## 2. Phase 2 Goals

### 2.1 Primary Goals
- Replace shallow sentiment heuristics with robust social sentiment analysis
- Detect trends based on **change over time**, not raw volume
- Weight signals by engagement to reduce noise
- Surface emerging topics beyond predefined keywords
- Improve event-level intelligence and explainability

### 2.2 Non-Goals
- No new social platforms
- No comment ingestion
- No streaming ingestion
- No LLM-based summarization
- No user personalization or authentication

---

## 3. Success Criteria

Phase 2 is considered successful when:
- Sentiment timelines show clear polarity shifts during real events
- Trends naturally rise, peak, and decay
- Emerging topics appear without manual keyword seeding
- Event views explain *why* a topic trended
- Outputs are visibly more meaningful than Phase 1

---

## 4. Scope

### 4.1 In Scope
- Sentiment model upgrade
- Time-aware trend detection
- Engagement-weighted analytics
- Emerging topic detection
- Event intelligence refinement
- Supporting backend APIs
- Incremental frontend UX enhancements

### 4.2 Out of Scope
- Comment ingestion
- Streaming APIs
- Multi-node architecture
- Cross-platform analytics
- Generative text output

---

## 5. User Personas

### 5.1 Primary User
**Analyst / Student / Researcher**
- Wants to understand public reaction to events
- Needs interpretable, explainable signals
- Values trend timing and sentiment direction

### 5.2 Secondary User
**Developer / Evaluator**
- Evaluates system design quality
- Looks for clean architecture and justified decisions

---

## 6. Functional Requirements

### 6.1 Sentiment Intelligence Upgrade

#### Description
Replace lexicon-based sentiment scoring with a social-media-aware sentiment model.

#### Requirements
- Compute sentiment per post using a pretrained model
- Output a continuous sentiment score
- Aggregate sentiment by subreddit and event
- Preserve existing API response formats

#### Acceptance Criteria
- Negative and positive events show distinguishable sentiment curves
- Neutral content does not artificially skew results

---

### 6.2 Time-Aware Trend Detection

#### Description
Detect trends based on temporal change rather than absolute keyword counts.

#### Requirements
- Introduce sliding time windows
- Compare current vs previous window
- Compute relative velocity and spike strength
- Decay stale keywords automatically

#### Acceptance Criteria
- Old keywords lose prominence without manual reset
- Newly active topics rise quickly

---

### 6.3 Engagement-Weighted Trends

#### Description
Weight trend signals by post engagement.

#### Requirements
- Incorporate score and comment count
- Apply logarithmic scaling to prevent domination
- Store both raw and weighted metrics

#### Acceptance Criteria
- High-impact posts influence trends more than low-engagement posts
- Noise-heavy keywords lose ranking

---

### 6.4 Emerging Topic Detection

#### Description
Identify trending topics not present in predefined keyword lists.

#### Requirements
- Extract candidate unigrams and bigrams
- Filter stopwords and existing keywords
- Track first-seen timestamp
- Promote topics crossing frequency and velocity thresholds

#### Acceptance Criteria
- New discussion themes appear automatically
- Topics are not dominated by generic terms

---

### 6.5 Event Intelligence Enhancement

#### Description
Improve event pages to explain causal drivers.

#### Requirements
- Rank event-related posts by engagement
- Identify dominant sentiment direction
- Identify leading subreddits
- Detect lifecycle phases (rise, peak, decay)

#### Acceptance Criteria
- Event pages summarize *why* activity occurred
- Event timelines align with real-world timing

---

## 7. API Requirements

### 7.1 New or Extended Endpoints
- `/analytics/emerging-topics`
- Extended trend payloads including baseline and delta
- Extended sentiment payloads with richer scores

### 7.2 Backward Compatibility
- Existing Phase 1 endpoints must continue to function
- Schema changes must be additive

---

## 8. Data Requirements

### 8.1 Storage
- Post-level sentiment scores
- Windowed trend metrics
- Emerging topic metadata
- Event analytics metadata

### 8.2 Retention
- Raw posts: unchanged from Phase 1
- Aggregates: unchanged from Phase 1
- No increase in long-term raw storage

### 8.3 Data Migration and Backward Compatibility

All Phase 2 schema changes must preserve and migrate existing Phase 1 data.

#### Requirements
- Previously ingested posts, sentiment records, trends, and event analytics must remain usable
- New fields introduced in Phase 2 must be additive and nullable
- Existing records must be backfilled or reprocessed where feasible
- No destructive schema changes are allowed

#### Migration Strategy
- Database migrations must run automatically at application startup
- Historical posts must be re-scored using the new sentiment model where possible
- Trend metrics must be recomputed using stored raw data or preserved aggregates
- Phase 1 data must continue to be accessible via existing APIs

#### Acceptance Criteria
- No loss of historical data after Phase 2 deployment
- Phase 1 dashboards continue to render without errors
- Phase 2 analytics include both historical and newly ingested data


---

## 9. Frontend Requirements

### 9.1 Visualization Enhancements
- Trend direction indicators
- Sentiment shift annotations
- Separation of tracked vs emerging topics
- Tooltips explaining metrics

### 9.2 UX Constraints
- No redesign of navigation
- Incremental improvements only
- Maintain dashboard-first layout

---

## 10. Non-Functional Requirements

- Single-node performance maintained
- No GPU dependency
- Low-latency analytics queries
- Deterministic and explainable outputs
- Clear logging and debuggability

---

## 11. Risks and Mitigations

### Risk: Increased noise from emerging topics  
**Mitigation:** Thresholding, stopword filtering, velocity constraints

### Risk: Overfitting to engagement  
**Mitigation:** Log scaling and caps

### Risk: Sentiment model bias  
**Mitigation:** Use interpretable scores and document limitations

---

## 12. Validation Plan

- Compare Phase 1 vs Phase 2 outputs on known events
- Qualitative inspection of trend timelines
- Manual verification against real news timelines
- Regression testing of existing endpoints

---

## 13. Phase 2 Exit Criteria

Phase 2 is complete when:
- Sentiment outputs are clearly improved
- Trends represent temporal dynamics
- Emerging topics are visible and relevant
- Event pages provide explanatory insight
- System remains stable and performant

---

## 14. Future Considerations (Post Phase 2)

- Comment ingestion (sampling-based)
- Topic clustering via embeddings
- Cross-platform data ingestion
- LLM-assisted summaries (optional)

---

## 15. Phase 2 Approval

Phase 2 is approved for implementation upon completion of this PRD and stakeholder review.

---

## 16. Technology and Package Constraints (Phase 2)

### Backend – NLP and Analytics
- Sentiment analysis must use `vaderSentiment`
- Tokenization and stopword filtering must use `nltk`
- Trend computation must use deterministic, window-based logic
- No embedding models or LLMs are permitted in Phase 2

### Backend – Data and Migration
- SQLite remains the primary datastore
- Schema changes must be additive and nullable
- Migrations must preserve all Phase 1 data
- Heavy migration frameworks (e.g., Alembic) are explicitly excluded

### Backend – Testing
- All new intelligence modules must include unit tests
- Existing tests must continue to pass without modification

### Frontend
- No new frontend frameworks or state libraries
- Existing Next.js and Recharts stack must be reused
- UI changes must be incremental and non-breaking

---