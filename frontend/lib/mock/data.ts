import type {
  DashboardData,
  EventData,
  SentimentData,
  SubredditData,
  TrendData
} from "@/lib/types";

export const dashboardData: DashboardData = {
  lastUpdated: "Just now",
  kpis: [
    { label: "Sentiment", value: "+0.42", delta: "+8%", trend: "up" },
    { label: "Mentions", value: "18.4k", delta: "+12%", trend: "up" },
    { label: "Active subs", value: "14", delta: "Stable", trend: "neutral" },
    { label: "Spikes", value: "6", delta: "+2", trend: "up" }
  ],
  sentimentTrend: [
    { time: "00:00", value: 0.1 },
    { time: "04:00", value: 0.18 },
    { time: "08:00", value: 0.32 },
    { time: "12:00", value: 0.28 },
    { time: "16:00", value: 0.4 },
    { time: "20:00", value: 0.42 }
  ],
  volumeTrend: [
    { time: "00:00", value: 1200 },
    { time: "04:00", value: 2200 },
    { time: "08:00", value: 4600 },
    { time: "12:00", value: 5200 },
    { time: "16:00", value: 6100 },
    { time: "20:00", value: 8300 }
  ],
  trendingTopics: [
    {
      keyword: "AI policy",
      velocity: "+68%",
      context: "r/technology, r/politics",
      sentiment: "Neutral",
      spike: "Spike x2.4"
    },
    {
      keyword: "earnings call",
      velocity: "+41%",
      context: "r/stocks, r/investing",
      sentiment: "Positive",
      spike: "Spike x1.9"
    },
    {
      keyword: "product recall",
      velocity: "+33%",
      context: "r/news, r/worldnews",
      sentiment: "Negative",
      spike: "Spike x1.6"
    }
  ],
  activeSubreddits: ["r/technology", "r/news", "r/stocks", "r/politics"],
  activeEvents: ["Launch Week", "Earnings Season", "Policy Review"]
};

export const trendData: TrendData = {
  lastUpdated: "Moments ago",
  keywordSeries: [
    {
      keyword: "AI policy",
      data: [
        { time: "00:00", value: 12 },
        { time: "06:00", value: 24 },
        { time: "12:00", value: 42 },
        { time: "18:00", value: 65 }
      ]
    },
    {
      keyword: "supply chain",
      data: [
        { time: "00:00", value: 8 },
        { time: "06:00", value: 18 },
        { time: "12:00", value: 28 },
        { time: "18:00", value: 39 }
      ]
    },
    {
      keyword: "rate cuts",
      data: [
        { time: "00:00", value: 10 },
        { time: "06:00", value: 20 },
        { time: "12:00", value: 31 },
        { time: "18:00", value: 55 }
      ]
    }
  ],
  trendCards: [
    {
      keyword: "AI policy",
      velocity: "+74%",
      context: "r/technology, r/politics",
      sentiment: "Neutral",
      spike: "Spike x2.6"
    },
    {
      keyword: "rate cuts",
      velocity: "+49%",
      context: "r/investing, r/finance",
      sentiment: "Positive",
      spike: "Spike x2.1"
    }
  ]
};

export const sentimentData: SentimentData = {
  lastUpdated: "Just now",
  distribution: [
    { label: "Positive", value: 46 },
    { label: "Neutral", value: 34 },
    { label: "Negative", value: 20 }
  ],
  timeline: [
    { time: "00:00", value: 0.08 },
    { time: "06:00", value: 0.22 },
    { time: "12:00", value: 0.35 },
    { time: "18:00", value: 0.28 },
    { time: "22:00", value: 0.41 }
  ]
};

export const subredditData: SubredditData = {
  lastUpdated: "Just now",
  kpis: [
    { label: "Posts", value: "1.9k", delta: "+6%" },
    { label: "Comments", value: "12.4k", delta: "+11%" },
    { label: "Sentiment", value: "+0.38", delta: "+4%" }
  ],
  sentimentTrend: [
    { time: "00:00", value: 0.12 },
    { time: "06:00", value: 0.3 },
    { time: "12:00", value: 0.28 },
    { time: "18:00", value: 0.4 }
  ],
  topics: [
    {
      keyword: "regulation",
      velocity: "+32%",
      context: "Top posts",
      sentiment: "Neutral",
      spike: "Spike x1.5"
    },
    {
      keyword: "hardware",
      velocity: "+22%",
      context: "Hot threads",
      sentiment: "Positive",
      spike: "Spike x1.3"
    }
  ]
};

export const eventData: EventData = {
  lastUpdated: "Just now",
  volumeTrend: [
    { time: "00:00", value: 420 },
    { time: "06:00", value: 720 },
    { time: "12:00", value: 1280 },
    { time: "18:00", value: 1640 }
  ],
  sentimentTrend: [
    { time: "00:00", value: 0.15 },
    { time: "06:00", value: 0.2 },
    { time: "12:00", value: 0.31 },
    { time: "18:00", value: 0.27 }
  ],
  topicCards: [
    {
      keyword: "launch readiness",
      velocity: "+58%",
      context: "r/startups, r/technology",
      sentiment: "Positive",
      spike: "Spike x2.0"
    },
    {
      keyword: "pricing",
      velocity: "+28%",
      context: "r/business",
      sentiment: "Neutral",
      spike: "Spike x1.4"
    }
  ]
};
