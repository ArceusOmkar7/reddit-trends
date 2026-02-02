"use client";

import { useEffect, useState } from "react";
import SectionHeader from "@/components/ui/SectionHeader";
import Card from "@/components/ui/Card";
import KeywordLineChart from "@/components/charts/KeywordLineChart";
import TrendCard from "@/components/ui/TrendCard";
import Badge from "@/components/ui/Badge";
import { useTrendData } from "@/lib/hooks/useTrendData";
import { useEmergingTopicsData } from "@/lib/hooks/useEmergingTopicsData";
import { useRefreshContext } from "@/components/layout/RefreshContext";
import { formatLocalDateTime, formatLocalTime } from "@/lib/format";

const timeWindows = ["1h", "6h", "24h", "7d"] as const;

export default function TrendsPage() {
  const [window, setWindow] = useState<(typeof timeWindows)[number]>("24h");
  const { data, loading, error, refetch } = useTrendData(window);
  const {
    data: emergingData,
    loading: emergingLoading,
    error: emergingError,
    refetch: refetchEmerging
  } = useEmergingTopicsData(window);
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
        description="Monitor term velocity and surface emerging topics across Reddit." 
        actionLabel="Refresh"
        onAction={() => {
          refetch();
          refetchEmerging();
        }}
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

      {(error || emergingError) && (
        <div className="card-surface p-4 text-sm text-accent-coral">
          {error ?? emergingError}
        </div>
      )}

      <Card title="Term velocity" subtitle="Acceleration within the selected window">
        <KeywordLineChart
          data={data?.keywordSeries ?? []}
          loading={loading}
          formatTick={window === "7d" ? formatLocalDateTime : formatLocalTime}
        />
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

      <Card title="Emerging topics" subtitle="New themes crossing quality thresholds">
        {emergingLoading ? (
          <div className="h-40 animate-pulse rounded-2xl bg-surface-lightGray" />
        ) : emergingData?.topics?.length ? (
          <div className="space-y-3">
            {emergingData.topics.map((topic, index) => (
              <div
                key={`${topic.topic}-${index}`}
                className="flex flex-wrap items-center justify-between gap-4 rounded-2xl border border-border-default bg-surface-lightGray/60 px-5 py-4"
              >
                <div>
                  <p className="text-base font-semibold text-ink-primary">
                    {topic.topic}
                  </p>
                  {topic.first_seen && (
                    <p className="text-xs text-ink-secondary">
                      First seen {topic.first_seen}
                    </p>
                  )}
                </div>
                <div className="flex flex-wrap items-center gap-2 text-sm">
                  <Badge
                    label={`${topic.velocity * 100 >= 0 ? "+" : ""}${Math.round(
                      topic.velocity * 100
                    )}%`}
                    variant="green"
                  />
                  <Badge label={`Mentions ${topic.raw_mentions}`} variant="purple" />
                  <Badge label={`Posts ${topic.unique_posts}`} variant="orange" />
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-sm text-ink-secondary">No emerging topics yet.</div>
        )}
      </Card>
    </div>
  );
}
