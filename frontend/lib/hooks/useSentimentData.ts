"use client";

import { fetchSentimentData } from "@/lib/mock/api";
import { useAsyncData } from "@/lib/hooks/useAsyncData";
import type { SentimentData } from "@/lib/types";

export function useSentimentData() {
  return useAsyncData<SentimentData>(fetchSentimentData, []);
}
