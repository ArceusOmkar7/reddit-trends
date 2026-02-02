"use client";

import { createContext, useContext, useEffect, useMemo, useState } from "react";

export interface PollingState {
  enabled: boolean;
  intervalSeconds: number;
  lastRun: string | null;
  nextRun: string | null;
}

interface PollingContextValue {
  state: PollingState | null;
  loading: boolean;
  refresh: () => Promise<void>;
  setPollingState: (state: PollingState) => void;
}

const PollingContext = createContext<PollingContextValue | undefined>(undefined);

const fallbackState: PollingState = {
  enabled: false,
  intervalSeconds: 300,
  lastRun: null,
  nextRun: null
};

export function PollingProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<PollingState | null>(null);
  const [loading, setLoading] = useState(false);

  const refresh = async () => {
    setLoading(true);
    try {
      const response = await fetch("/api/polling", { cache: "no-store" });
      if (!response.ok) {
        setState((prev) => prev ?? fallbackState);
        return;
      }
      const payload = (await response.json()) as PollingState;
      setState(payload);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void refresh();
    const interval = setInterval(() => void refresh(), 30000);
    const handleIngestionEvent = (event: Event) => {
      const detail = (event as CustomEvent).detail as PollingState | undefined;
      if (!detail) {
        return;
      }
      setState(detail);
    };
    const handlePollingRefresh = () => {
      void refresh();
    };
    window.addEventListener("ingestion-state", handleIngestionEvent);
    window.addEventListener("polling-refresh", handlePollingRefresh);
    return () => {
      clearInterval(interval);
      window.removeEventListener("ingestion-state", handleIngestionEvent);
      window.removeEventListener("polling-refresh", handlePollingRefresh);
    };
  }, []);

  const value = useMemo(
    () => ({
      state,
      loading,
      refresh,
      setPollingState: setState
    }),
    [state, loading]
  );

  return (
    <PollingContext.Provider value={value}>{children}</PollingContext.Provider>
  );
}

export function usePollingContext() {
  const context = useContext(PollingContext);
  if (!context) {
    throw new Error("usePollingContext must be used within PollingProvider");
  }
  return context;
}
