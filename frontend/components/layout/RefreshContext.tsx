"use client";

import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { formatLocalDateTime } from "@/lib/format";

interface RefreshContextValue {
  lastRefreshed: string | null;
  setLastRefreshed: (value: string) => void;
}

const RefreshContext = createContext<RefreshContextValue | undefined>(undefined);

export function RefreshProvider({ children }: { children: React.ReactNode }) {
  const [lastRefreshed, setLastRefreshed] = useState<string | null>(null);

  useEffect(() => {
    const loadInitial = async () => {
      try {
        const response = await fetch("/api/polling", { cache: "no-store" });
        if (!response.ok) {
          return;
        }
        const payload = (await response.json()) as { lastRun?: string | null };
        if (payload.lastRun) {
          setLastRefreshed(formatLocalDateTime(payload.lastRun));
        }
      } catch (error) {
        // ignore
      }
    };
    void loadInitial();
  }, []);

  useEffect(() => {
    const handleIngestionEvent = (event: Event) => {
      const detail = (event as CustomEvent).detail as
        | { lastRun?: string | null }
        | undefined;
      if (detail?.lastRun) {
        setLastRefreshed(formatLocalDateTime(detail.lastRun));
      }
    };
    window.addEventListener("ingestion-state", handleIngestionEvent);
    return () => window.removeEventListener("ingestion-state", handleIngestionEvent);
  }, []);

  const value = useMemo(
    () => ({ lastRefreshed, setLastRefreshed }),
    [lastRefreshed]
  );

  return <RefreshContext.Provider value={value}>{children}</RefreshContext.Provider>;
}

export function useRefreshContext() {
  const context = useContext(RefreshContext);
  if (!context) {
    throw new Error("useRefreshContext must be used within RefreshProvider");
  }
  return context;
}
