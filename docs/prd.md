# Product Requirements Document (PRD)

## Real-Time Social Media Intelligence Platform (Reddit-based)

---

## 1. Overview

### Product Vision

Build a lightweight, near real-time intelligence platform that analyzes Reddit discussions to track **public sentiment** and **detect emerging trends early** across selected subreddits and events.

### Problem Statement

Reddit discussions react quickly to real-world events, but insights are buried in high-volume, unstructured text. There is no simple system that continuously monitors targeted subreddits and converts discussions into actionable sentiment and trend signals.

### Solution

A web-based platform that ingests Reddit posts and comments in near real-time, processes them using NLP techniques, and presents sentiment trends and emerging topics through an interactive dashboard.

---

## 2. Goals and Objectives

### Primary Goals

* Track sentiment changes around events or topics
* Detect trending keywords and discussion spikes early
* Provide visual, interpretable insights via a dashboard

### Non-Goals (Phase 1)

* No user-level profiling
* No predictive modeling
* No multi-platform support outside Reddit
* No heavy LLM-based reasoning

---

## 3. Target Users

### Primary Users

* Students and researchers
* Analysts exploring online discourse
* Developers experimenting with social intelligence systems

### User Needs

* Quick understanding of public mood
* Early awareness of trending discussions
* Clean visual summaries instead of raw Reddit feeds

---

## 4. Data Scope

### Source

* Reddit API

### Coverage

* Predefined list of subreddits
* Event or keyword-based tracking
* Posts and comments
* Metadata: timestamps, score, number of comments

### Update Frequency

* Near real-time polling every **5 minutes**

---

## 5. Core Features (Functional Requirements)

### 5.1 Data Ingestion

* Periodic polling of Reddit API
* Filter by subreddit and keywords
* Store raw posts and comments

### 5.2 Sentiment Analysis

* Sentence or document-level sentiment scoring
* Aggregate sentiment over time
* Subreddit-wise sentiment comparison

### 5.3 Trend Detection

* Keyword frequency tracking
* Sudden spike detection
* Time-window based trend analysis

### 5.4 Dashboard

* Sentiment timeline graphs
* Trending topics list
* Volume of discussion over time
* Filters by subreddit and event

---

## 6. Non-Functional Requirements

* Near real-time updates with minimal latency
* Scalable to tens of thousands of posts
* Single-node deployment
* Modular design for future ML upgrades
* Ethical handling of public data

---

## 7. Technical Constraints (Locked)

* Infrastructure: **DigitalOcean small VM**
* Architecture: **Single-node**
* Update model: **Polling-based**
* Budget: Covered by existing credits
* Deployment: Docker-based
* Timeline: Short-term side project

---

## 8. High-Level Architecture

### Backend

* Reddit data ingestion service
* NLP processing pipeline
* Trend analysis module
* REST API for dashboard

### Storage

* Database for raw and processed data
* Aggregated metrics storage for fast queries

### Frontend

* Web dashboard
* Interactive charts and filters

---

## 9. Evaluation Criteria

### Quantitative

* Sentiment consistency across time windows
* Detection of known event spikes

### Qualitative

* Case studies of real-world events
* Interpretability of insights

---

## 10. Future Enhancements (Out of Scope for v1)

* LLM-based summarization
* Cross-platform social data
* Alerting and notifications
* Advanced topic modeling

---
