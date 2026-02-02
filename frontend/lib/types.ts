export interface KpiTile {
  label: string;
  value: string;
  delta: string;
  trend: "up" | "down" | "neutral";
}

export interface TrendTopic {
  keyword: string;
  velocity: string;
  context?: string;
  sentiment?: string;
  spike?: string;
}

export interface TimeSeriesPoint {
  time: string;
  value: number;
}

export interface KeywordSeries {
  keyword: string;
  data: TimeSeriesPoint[];
}

export interface DistributionSlice {
  label: string;
  value: number;
}

export interface DashboardData {
  lastUpdated: string;
  kpis: KpiTile[];
  sentimentTrend: TimeSeriesPoint[];
  volumeTrend: TimeSeriesPoint[];
  trendingTopics: TrendTopic[];
  activeSubreddits: string[];
  activeEvents: string[];
}

export interface TrendData {
  lastUpdated: string;
  keywordSeries: KeywordSeries[];
  trendCards: TrendTopic[];
}

export interface EmergingTopic {
  topic: string;
  raw_mentions: number;
  unique_posts: number;
  velocity: number;
  first_seen?: string;
}

export interface EmergingTopicData {
  lastUpdated: string;
  topics: EmergingTopic[];
}

export interface SentimentData {
  lastUpdated: string;
  distribution: DistributionSlice[];
  timeline: TimeSeriesPoint[];
}

export interface SubredditData {
  lastUpdated: string;
  kpis: Array<Omit<KpiTile, "trend">>;
  sentimentTrend: TimeSeriesPoint[];
  topics: TrendTopic[];
}

export interface EventData {
  lastUpdated: string;
  volumeTrend: TimeSeriesPoint[];
  sentimentTrend: TimeSeriesPoint[];
  topicCards: TrendTopic[];
  topPosts: EventTopPost[];
  leadingSubreddits: EventLeadingSubreddit[];
  lifecycle?: EventLifecycle | null;
}

export interface EventTopPost {
  id: string;
  timestamp: string;
  title: string;
  subreddit: string;
  score: number;
  comment_count: number;
  weight: number;
}

export interface EventLeadingSubreddit {
  subreddit: string;
  weight: number;
  posts: number;
}

export interface EventLifecycle {
  phase: "rise" | "peak" | "decay" | "stable";
  weighted_velocity: number;
  weighted_mentions: number;
  previous_weighted_mentions: number;
  window_start: string;
  window_end: string;
  percentile_75: number;
}
