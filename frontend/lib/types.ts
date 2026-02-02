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
}
