# Reddit Trends Frontend

Next.js dashboard for sentiment, trend, subreddit, and event analytics.

## Requirements
- Node.js 20+
- npm

## Environment
Copy and edit frontend/.env.example:

- NEXT_PUBLIC_API_BASE_URL (default http://localhost:8000)

## Setup
1. Install dependencies:
   - npm install

## Run
- npm run dev

## Build
- npm run build
- npm run start

## Production
- Set NEXT_PUBLIC_API_BASE_URL to your backend URL.
- Serve with npm run start or a process manager (Docker or similar).

## Tests
- npm run test
- npm run test:watch

## Notes
- Charts are localized based on browser locale.
- For local development, ensure the backend is running on port 8000.
