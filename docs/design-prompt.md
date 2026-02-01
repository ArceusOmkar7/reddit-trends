# Frontend Design Document

## Real-Time Social Media Intelligence Platform (Reddit)

---

## 1. Design Goals

* Provide a clear, data-first interface for sentiment and trend monitoring
* Enable fast navigation across analytics views
* Keep UI minimal, readable, and dashboard-oriented
* Ensure all components are reusable and scalable
* Avoid authentication and personalization complexity

---

## 2. Application Layout Overview

The frontend follows a **persistent layout structure**:

* **Left Sidebar**: Primary navigation
* **Top Header Bar**: Context and status information
* **Main Content Area**: Page-specific analytics and visualizations
* **Modals Layer**: Filters and detail views rendered as overlays

---

## 3. Pages and UI Structure

### 3.1 Dashboard

**Purpose**: High-level overview of platform activity

**Key UI Sections**

* Sentiment trend line chart (global or selected context)
* Discussion volume chart
* Top trending topics list
* Active subreddit and event summary cards

---

### 3.2 Trends Page

**Purpose**: Early detection of emerging topics

**Key UI Sections**

* Keyword frequency over time graph
* Trend spike indicators
* Time window selector
* Expandable trend cards

---

### 3.3 Sentiment Analysis Page

**Purpose**: Sentiment distribution and evolution

**Key UI Sections**

* Sentiment distribution chart
* Sentiment timeline
* Filters for subreddit and event
* Metric explanation tooltips

---

### 3.4 Subreddit View Page

**Purpose**: Subreddit-specific intelligence

**Key UI Sections**

* Subreddit selector
* Post and comment volume metrics
* Sentiment trend per subreddit
* Dominant topic list

Breadcrumbs enabled:

```
Dashboard → Subreddits → r/{subreddit_name}
```

---

### 3.5 Event Monitoring Page

**Purpose**: Track discussions around specific events or keywords

**Key UI Sections**

* Event selector or keyword input
* Discussion growth timeline
* Sentiment shift indicators
* Event-specific trending terms

Breadcrumbs enabled:

```
Dashboard → Events → {event_name}
```

---

### 3.6 System Info / About Page

**Purpose**: Transparency and documentation

**Key UI Sections**

* Data source description
* Update frequency
* Known limitations
* Ethical considerations

---

## 4. Shared UI Components

### 4.1 Navigation Sidebar

* Persistent across all pages
* Icons + labels
* Active route highlighting
* Collapsible for smaller screens

---

### 4.2 Header / Top Bar

Displays:

* Platform name
* Current context (selected subreddit or event)
* Last data refresh timestamp
* Optional theme toggle

---

### 4.3 Breadcrumbs

* Used only on hierarchical pages
* Improves navigation clarity
* Clickable path segments

---

### 4.4 Modals / Popups

**Filter Modal**

* Date range selector
* Subreddit selection
* Event keyword input

**Trend Detail Modal**

* Expanded keyword statistics
* Mini time-series charts

**Info Modal**

* Explains sentiment and trend metrics
* Non-technical descriptions

---

## 5. State and Data Handling

### Data Flow

* API services fetch processed analytics data
* Reusable hooks manage loading, error, and refresh states
* UI components consume normalized data objects

### Mock API Store

Used during development with:

* Unique IDs
* Timestamps
* Subreddit names
* Sentiment scores
* Keyword metrics
* Aggregated trend data

---

## 6. Routing Strategy

* URL-based routing for all pages
* Each page mapped to a dedicated route
* Context parameters handled via query params

Example:

```
/dashboard
/trends
/sentiment
/subreddits/:name
/events/:eventId
/about
```

---

## 7. Styling and Design System

* Utility-first styling approach
* Consistent spacing, typography, and color scales
* Chart components styled to match dashboard theme
* Dark mode support optional

---

## 8. Frontend Tech Stack

### Core Framework

* **React** for component-based UI development

### Styling

* **Tailwind CSS** for utility-first styling
* Optional component abstraction using custom UI primitives

### Routing

* **React Router** for URL-based navigation

### Data Visualization

* **Recharts** or **Chart.js** for charts and graphs

### State and Data Fetching

* Custom React hooks
* Fetch or Axios for API calls

### Mock Data

* Local mock API service
* JSON-based data store with realistic schemas

### Build and Tooling

* Vite for fast development and bundling
* ESLint for code quality
* Docker-ready frontend build

---

## 9. Out of Scope (Intentional)

* Authentication and authorization
* User profiles or preferences
* Consideration of multiple user roles
* Real-time websockets
* Mobile-first design

---
