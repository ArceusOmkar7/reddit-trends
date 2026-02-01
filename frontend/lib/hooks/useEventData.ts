"use client";

import { fetchEventData } from "@/lib/api/backend";
import { useAsyncData } from "@/lib/hooks/useAsyncData";
import type { EventData } from "@/lib/types";

export function useEventData(eventId: string) {
  return useAsyncData<EventData>(() => fetchEventData(eventId), [eventId]);
}
