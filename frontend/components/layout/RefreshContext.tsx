"use client";

import { createContext, useContext, useMemo, useState } from "react";

interface RefreshContextValue {
  lastRefreshed: string | null;
  setLastRefreshed: (value: string) => void;
}

const RefreshContext = createContext<RefreshContextValue | undefined>(undefined);

export function RefreshProvider({ children }: { children: React.ReactNode }) {
  const [lastRefreshed, setLastRefreshed] = useState<string | null>(null);

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
