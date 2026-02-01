"use client";

import { useEffect } from "react";
import SectionHeader from "@/components/ui/SectionHeader";
import StatTile from "@/components/ui/StatTile";
import Card from "@/components/ui/Card";
import TrendCard from "@/components/ui/TrendCard";
import SentimentLineChart from "@/components/charts/SentimentLineChart";
import VolumeAreaChart from "@/components/charts/VolumeAreaChart";
import { useDashboardData } from "@/lib/hooks/useDashboardData";
import { useRefreshContext } from "@/components/layout/RefreshContext";

export default function DashboardPage() {
  const { data, loading, error, refetch } = useDashboardData();
  const { setLastRefreshed } = useRefreshContext();

  useEffect(() => {
    if (data?.lastUpdated) {
      setLastRefreshed(data.lastUpdated);
    }
  }, [data?.lastUpdated, setLastRefreshed]);

  return (
    <div className="space-y-8">
      <SectionHeader
        title="Real-time sentiment & trend"
        accent="overview"
        description="Live signals from selected subreddits and event keywords." 
        actionLabel="Refresh"
        onAction={refetch}
      />

      {error && (
        <div className="card-surface p-4 text-sm text-accent-coral">
          {error}
        </div>
      )}

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {data?.kpis?.length ? (
          data.kpis.map((kpi) => <StatTile key={kpi.label} {...kpi} />)
        ) : (
          <div className="card-surface p-4 text-sm text-ink-secondary md:col-span-2 xl:col-span-4">
            No KPI data yet. Run ingestion to populate metrics.
          </div>
        )}
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card
          title="Sentiment timeline"
          subtitle="Aggregate sentiment across tracked subreddits"
        >
          <SentimentLineChart data={data?.sentimentTrend ?? []} loading={loading} />
        </Card>
        <Card
          title="Discussion volume"
          subtitle="Post + comment velocity in the last 24 hours"
        >
          <VolumeAreaChart data={data?.volumeTrend ?? []} loading={loading} />
        </Card>
      </div>

      <div className="grid gap-6 lg:grid-cols-[1.4fr_1fr]">
        <Card
          title="Trending topics"
          subtitle="Keywords with the sharpest acceleration"
        >
          {data?.trendingTopics?.length ? (
            <div className="space-y-3">
              {data.trendingTopics.map((topic, index) => (
                <TrendCard key={`${topic.keyword}-${index}`} {...topic} />
              ))}
            </div>
          ) : (
            <div className="text-sm text-ink-secondary">No trending topics yet.</div>
          )}
        </Card>
        <Card
          title="Active focus"
          subtitle="Subreddits and events currently monitored"
        >
          <div className="space-y-4">
            <div className="rounded-2xl bg-surface-purpleTint p-4">
              <p className="metric-label">Subreddits</p>
              <p className="mt-2 text-lg font-semibold text-ink-primary">
                {data?.activeSubreddits?.length
                  ? data.activeSubreddits.join(", ")
                  : "No active subreddits yet."}
              </p>
            </div>
            <div className="rounded-2xl bg-surface-peachTint p-4">
              <p className="metric-label">Events</p>
              <p className="mt-2 text-lg font-semibold text-ink-primary">
                {data?.activeEvents?.length
                  ? data.activeEvents.join(", ")
                  : "No active events yet."}
              </p>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
