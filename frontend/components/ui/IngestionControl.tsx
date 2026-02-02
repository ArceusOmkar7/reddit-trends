"use client";

import { useEffect, useState } from "react";
import { formatLocalDateTime } from "@/lib/format";
import { usePollingContext } from "@/components/layout/PollingContext";

export default function IngestionControl() {
  const { state, refresh, setPollingState } = usePollingContext();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadState = async () => {
    try {
      await refresh();
      setError(null);
    } catch (err) {
      setError("Unable to load ingestion status.");
    }
  };

  useEffect(() => {
    void loadState();
  }, []);

  const toggle = async () => {
    if (!state) {
      return;
    }
    setLoading(true);
    try {
      const response = await fetch("/api/ingestion", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ enabled: !state.enabled })
      });
      if (!response.ok) {
        throw new Error("Failed to update ingestion");
      }
      const payload = (await response.json()) as {
        enabled: boolean;
        intervalSeconds: number;
        lastRun: string | null;
        nextRun: string | null;
      };
      setPollingState(payload);
      window.dispatchEvent(
        new CustomEvent("ingestion-state", { detail: payload })
      );
      window.dispatchEvent(new Event("polling-refresh"));
      setError(null);
    } catch (err) {
      setError("Unable to update ingestion state.");
    } finally {
      setLoading(false);
    }
  };

  const statusLabel = state?.enabled ? "Running" : "Paused";
  const statusTone = state?.enabled ? "text-emerald-600" : "text-amber-600";
  const intervalMinutes = state
    ? Math.max(Math.round(state.intervalSeconds / 60), 1)
    : 5;

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <div>
          <p className="metric-label">Ingestion</p>
          <p className={`mt-2 text-lg font-semibold ${statusTone}`}>{statusLabel}</p>
        </div>
        <button
          className="rounded-full border border-border-default px-4 py-2 text-sm font-semibold text-ink-secondary hover:text-brand-purple"
          type="button"
          onClick={toggle}
          disabled={loading}
        >
          {state?.enabled ? "Pause" : "Start"}
        </button>
      </div>
      <div className="text-sm text-ink-secondary">
        Polling every {intervalMinutes} minutes.
      </div>
      <div className="text-xs text-ink-muted">
        Last run: {state?.lastRun ? formatLocalDateTime(state.lastRun) : "—"}
      </div>
      <div className="text-xs text-ink-muted">
        Next run: {state?.nextRun ? formatLocalDateTime(state.nextRun) : "—"}
      </div>
      {error && <p className="text-xs text-accent-coral">{error}</p>}
    </div>
  );
}
