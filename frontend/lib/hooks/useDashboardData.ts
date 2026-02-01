"use client";

import { fetchDashboardData } from "@/lib/mock/api";
import { useAsyncData } from "@/lib/hooks/useAsyncData";
import type { DashboardData } from "@/lib/types";

export function useDashboardData() {
  return useAsyncData<DashboardData>(fetchDashboardData, []);
}
