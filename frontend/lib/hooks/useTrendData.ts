"use client";

import { fetchTrendData } from "@/lib/api/backend";
import { useAsyncData } from "@/lib/hooks/useAsyncData";
import type { TrendData } from "@/lib/types";

export function useTrendData(window: string) {
  return useAsyncData<TrendData>(fetchTrendData, [window]);
}
