import {
  dashboardData,
  trendData,
  sentimentData,
  subredditData,
  eventData
} from "@/lib/mock/data";
import type {
  DashboardData,
  EventData,
  SentimentData,
  SubredditData,
  TrendData
} from "@/lib/types";

const wait = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export async function fetchDashboardData(): Promise<DashboardData> {
  await wait(300);
  return dashboardData;
}

export async function fetchTrendData(): Promise<TrendData> {
  await wait(300);
  return trendData;
}

export async function fetchSentimentData(): Promise<SentimentData> {
  await wait(300);
  return sentimentData;
}

export async function fetchSubredditData(): Promise<SubredditData> {
  await wait(300);
  return subredditData;
}

export async function fetchEventData(): Promise<EventData> {
  await wait(300);
  return eventData;
}
