"use client";

import { useEffect, useState } from "react";
import SectionHeader from "@/components/ui/SectionHeader";
import Card from "@/components/ui/Card";
import KeywordLineChart from "@/components/charts/KeywordLineChart";
import TrendCard from "@/components/ui/TrendCard";
import { useTrendData } from "@/lib/hooks/useTrendData";
import { useRefreshContext } from "@/components/layout/RefreshContext";

const timeWindows = ["1h", "6h", "24h", "7d"] as const;

export default function TrendsPage() {
  const [window, setWindow] = useState<(typeof timeWindows)[number]>("24h");
  const { data, loading, error, refetch } = useTrendData(window);
  const { setLastRefreshed } = useRefreshContext();

  useEffect(() => {
    if (data?.lastUpdated) {
      setLastRefreshed(data.lastUpdated);
    }
  }, [data?.lastUpdated, setLastRefreshed]);

  return (
    <div className="space-y-8">
      <SectionHeader
        title="Trend detection"
        accent="signals"
        description="Capture keywords and events that are accelerating across Reddit." 
        actionLabel="Refresh"
        onAction={refetch}
      />

      <div className="flex flex-wrap gap-2">
        {timeWindows.map((range) => (
          <button
            key={range}
            onClick={() => setWindow(range)}
            className={`rounded-full border px-4 py-2 text-sm font-semibold transition ${
              window === range
                ? "border-brand-purple bg-brand-purple text-white shadow-button"
                : "border-border-default bg-white text-ink-secondary hover:border-brand-purple"
            }`}
          >
            {range}
          </button>
        ))}
      </div>

      {error && (
        <div className="card-surface p-4 text-sm text-accent-coral">
          {error}
        </div>
      )}

      <Card title="Keyword velocity" subtitle="Frequency spikes within selected window">
        <KeywordLineChart data={data?.keywordSeries ?? []} loading={loading} />
      </Card>

      <Card title="Accelerating topics" subtitle="Top terms with strongest momentum">
        {data?.trendCards?.length ? (
          <div className="space-y-3">
            {data.trendCards.map((topic, index) => (
              <TrendCard key={`${topic.keyword}-${index}`} {...topic} />
            ))}
          </div>
        ) : (
          <div className="text-sm text-ink-secondary">No accelerating topics yet.</div>
        )}
      </Card>
    </div>
  );
}
