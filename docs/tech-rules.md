
---

# Tech Stack Rules Document

## Real-Time Social Media Intelligence Platform (Reddit)

---

## 1. Purpose of This Document

This document defines the **approved technology stack**, **usage rules**, and **constraints** for the project.
The goal is to ensure consistency, simplicity, and feasibility for a single-developer, side-project implementation.

---

## 2. High-Level Architecture Rule

* Single-node architecture
* Polling-based near real-time system
* Backend-first intelligence pipeline
* Read-only frontend dashboard
* No authentication or user management

---

## 3. Frontend Technology Rules

### 3.1 Framework

* **React** is mandatory for frontend development
* Functional components only
* Hooks-based state management

### 3.2 Styling

* **Tailwind CSS** must be used for all styling
* No inline styles
* No external UI frameworks like Material UI or Ant Design
* Common styles extracted into reusable utility components

### 3.3 Routing

* **React Router** required for navigation
* URL-based routing for every page
* Context like subreddit or event passed via route params or query params
* No hash-based routing

### 3.4 Data Visualization

* Use **Recharts** or **Chart.js**
* Charts must be reusable components
* No hardcoded data inside chart components
* All chart data must come from API or mock services

### 3.5 State and Data Handling

* Custom React hooks for:

  * Data fetching
  * Loading and error states
  * Periodic refresh
* No global state libraries unless absolutely necessary
* Mock API store required during early development

---

## 4. Backend Technology Rules

### 4.1 Language and Framework

* **Python** is mandatory
* **FastAPI** for backend services
* REST-style APIs only

### 4.2 Data Ingestion

* Reddit API as the sole live data source
* Polling-based ingestion
* Configurable polling interval with a default of 5 minutes
* No streaming or websocket ingestion

### 4.3 NLP and Analytics

* Simple and interpretable models only
* Rule-based or lightweight ML techniques
* No LLM dependency in Phase 1
* Deterministic outputs preferred over black-box models

### 4.4 API Design

* Clear separation between:

  * Raw data endpoints
  * Aggregated analytics endpoints
* Consistent response schemas
* IDs and timestamps mandatory in all responses

---

## 5. Database and Storage Rules

### 5.1 Database

* Single database instance
* Structured storage for:

  * Posts
  * Comments
  * Sentiment scores
  * Trend metrics
* Avoid distributed databases

### 5.2 Data Retention

* Store limited historical data
* Aggregated metrics preferred over raw text for long-term storage
* No personal user profiling data stored

---

## 6. Infrastructure Rules

### 6.1 Hosting

* **DigitalOcean VM** as the primary deployment target
* Small VM with limited but stable resources
* Single-region deployment

### 6.2 Deployment

* **Docker** required for backend and frontend
* Docker Compose allowed for local development
* No Kubernetes or orchestration platforms

### 6.3 Environment Management

* Environment variables for configuration
* No secrets committed to version control
* Separate configs for local and production

---

## 7. Development Rules

### 7.1 Code Quality

* Modular code structure
* Clear separation of concerns
* Descriptive naming for files and functions
* Minimal comments, but clear intent

### 7.2 Version Control

* Git-based workflow
* Small, logical commits
* Clear commit messages

---

## 8. Security and Ethics Rules

* Only public Reddit data used
* No scraping beyond API limits
* No user identity tracking
* No sentiment analysis at individual user level
* Transparency provided via System Info page

---

## 9. Explicitly Out of Scope Technologies

* Authentication systems
* OAuth or login flows
* WebSockets or streaming pipelines
* Multi-cloud deployments
* Microservices architecture
* Heavy LLM-based processing

---

## 10. Future Stack Extension Rules

* Any new technology must:

  * Serve a clear intelligence goal
  * Be justified in terms of complexity vs benefit
  * Not break single-node architecture
* LLMs allowed only as optional enhancement modules
* Additional platforms allowed only after Reddit pipeline is stable

---
