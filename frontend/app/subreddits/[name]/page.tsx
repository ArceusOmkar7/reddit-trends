"use client";

import { useEffect } from "react";
import { useParams } from "next/navigation";
import SectionHeader from "@/components/ui/SectionHeader";
import Card from "@/components/ui/Card";
import Breadcrumbs from "@/components/layout/Breadcrumbs";
import SentimentLineChart from "@/components/charts/SentimentLineChart";
import { useSubredditData } from "@/lib/hooks/useSubredditData";
import TrendCard from "@/components/ui/TrendCard";
import { useRefreshContext } from "@/components/layout/RefreshContext";

export default function SubredditPage() {
  const params = useParams<{ name: string }>();
  const subreddit = params?.name ?? "";
  const { data, loading, error, refetch } = useSubredditData(subreddit);
  const { setLastRefreshed } = useRefreshContext();

  useEffect(() => {
    if (data?.lastUpdated) {
      setLastRefreshed(data.lastUpdated);
    }
  }, [data?.lastUpdated, setLastRefreshed]);

  return (
    <div className="space-y-8">
      <Breadcrumbs
        items={[
          { label: "Dashboard", href: "/dashboard" },
          { label: "Subreddits", href: "/dashboard" },
          { label: `r/${subreddit}` }
        ]}
      />
      <SectionHeader
        title={`Subreddit focus: r/${subreddit}`}
        accent="insights"
        description="Track sentiment shifts and dominant topics for this community." 
        actionLabel="Refresh"
        onAction={refetch}
      />

      {error && (
        <div className="card-surface p-4 text-sm text-accent-coral">
          {error}
        </div>
      )}

      <div className="grid gap-6 lg:grid-cols-3">
        {data?.kpis.map((kpi) => (
          <div key={kpi.label} className="card-surface p-4">
            <p className="metric-label">{kpi.label}</p>
            <p className="mt-2 text-2xl font-semibold text-ink-primary">
              {kpi.value}
            </p>
            <p className="mt-1 text-sm text-ink-secondary">{kpi.delta}</p>
          </div>
        ))}
      </div>

      <Card title="Sentiment trend" subtitle="Rolling average sentiment">
        <SentimentLineChart data={data?.sentimentTrend ?? []} loading={loading} />
      </Card>

      <Card title="Dominant topics" subtitle="Recurring themes in top posts">
        <div className="space-y-3">
          {data?.topics.map((topic, index) => (
            <TrendCard key={`${topic.keyword}-${index}`} {...topic} />
          ))}
        </div>
      </Card>
    </div>
  );
}
