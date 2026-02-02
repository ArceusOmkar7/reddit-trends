"use client";

import { fetchEmergingTopics } from "@/lib/api/backend";
import { useAsyncData } from "@/lib/hooks/useAsyncData";
import type { EmergingTopicData } from "@/lib/types";

export function useEmergingTopicsData(window: string) {
  return useAsyncData<EmergingTopicData>(() => fetchEmergingTopics(window), [window]);
}
