"use client";

import { fetchSubredditData } from "@/lib/api/backend";
import { useAsyncData } from "@/lib/hooks/useAsyncData";
import type { SubredditData } from "@/lib/types";

export function useSubredditData(subreddit: string) {
  return useAsyncData<SubredditData>(() => fetchSubredditData(subreddit), [subreddit]);
}
