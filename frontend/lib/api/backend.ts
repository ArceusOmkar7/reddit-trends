import type {
  DashboardData,
  EventData,
  SentimentData,
  TimeSeriesPoint,
  TrendData,
  TrendTopic,
  SubredditData
} from "@/lib/types";

type BackendTrendItem = {
  timestamp: string;
  keyword: string;
  velocity: number;
  spike: number;
};

type BackendSentimentItem = {
  timestamp: string;
  label: string;
  sentiment: number;
};

const baseUrl =
  process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/$/, "") ||
  "http://localhost:8000";

async function apiGet<T>(path: string): Promise<T> {
  const response = await fetch(`${baseUrl}${path}`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

const formatTime = (timestamp: string) =>
  new Date(timestamp).toISOString().slice(11, 16);

export async function fetchDashboardData(): Promise<DashboardData> {
  return apiGet<DashboardData>("/analytics/dashboard?hours=24");
}

export async function fetchTrendData(): Promise<TrendData> {
  const data = await apiGet<BackendTrendItem[]>("/analytics/trends?hours=24");

  const grouped = new Map<string, TimeSeriesPoint[]>();
  data.forEach((item) => {
    const series = grouped.get(item.keyword) ?? [];
    series.push({ time: formatTime(item.timestamp), value: item.velocity });
    grouped.set(item.keyword, series);
  });

  const keywordSeries = Array.from(grouped.entries()).map(([keyword, series]) => ({
    keyword,
    data: series
  }));

  const trendCards: TrendTopic[] = data
    .slice(0, 5)
    .map((item) => ({
      keyword: item.keyword,
      velocity: `+${Math.round(item.velocity)}%`,
      context: "Global",
      sentiment: "Neutral",
      spike: `Spike x${item.spike.toFixed(1)}`
    }));

  return {
    lastUpdated: data[0]?.timestamp ?? "Just now",
    keywordSeries,
    trendCards
  };
}

export async function fetchSentimentData(): Promise<SentimentData> {
  const data = await apiGet<BackendSentimentItem[]>(
    "/analytics/sentiment?hours=24"
  );

  const timelineMap = new Map<string, number[]>();
  data.forEach((item) => {
    const timeKey = formatTime(item.timestamp);
    const bucket = timelineMap.get(timeKey) ?? [];
    bucket.push(item.sentiment);
    timelineMap.set(timeKey, bucket);
  });

  const timeline = Array.from(timelineMap.entries()).map(([time, values]) => ({
    time,
    value: values.reduce((sum, value) => sum + value, 0) / values.length
  }));

  const latestTimestamp = data[0]?.timestamp;
  const latestValues = latestTimestamp
    ? data.filter((item) => item.timestamp === latestTimestamp)
    : data;

  const totals = { positive: 0, neutral: 0, negative: 0 };
  latestValues.forEach((item) => {
    if (item.sentiment > 0.1) {
      totals.positive += 1;
    } else if (item.sentiment < -0.1) {
      totals.negative += 1;
    } else {
      totals.neutral += 1;
    }
  });

  const sum = totals.positive + totals.neutral + totals.negative || 1;

  return {
    lastUpdated: latestTimestamp ?? "Just now",
    distribution: [
      { label: "Positive", value: Math.round((totals.positive / sum) * 100) },
      { label: "Neutral", value: Math.round((totals.neutral / sum) * 100) },
      { label: "Negative", value: Math.round((totals.negative / sum) * 100) }
    ],
    timeline
  };
}

export async function fetchSubredditData(subreddit: string): Promise<SubredditData> {
  const data = await apiGet<SubredditData>(
    `/analytics/subreddits/${encodeURIComponent(subreddit)}?hours=24`
  );
  return data;
}

export async function fetchEventData(eventId: string): Promise<EventData> {
  const data = await apiGet<EventData>(
    `/analytics/events/${encodeURIComponent(eventId)}?hours=24`
  );
  return data;
}
