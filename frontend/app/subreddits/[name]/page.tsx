"use client";

import { useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import SectionHeader from "@/components/ui/SectionHeader";
import Card from "@/components/ui/Card";
import Breadcrumbs from "@/components/layout/Breadcrumbs";
import SentimentLineChart from "@/components/charts/SentimentLineChart";
import { useSubredditData } from "@/lib/hooks/useSubredditData";
import TrendCard from "@/components/ui/TrendCard";
import { useRefreshContext } from "@/components/layout/RefreshContext";
import { useDashboardData } from "@/lib/hooks/useDashboardData";

export default function SubredditPage() {
  const params = useParams<{ name: string }>();
  const router = useRouter();
  const subreddit = params?.name ?? "";
  const { data, loading, error, refetch } = useSubredditData(subreddit);
  const { data: dashboard } = useDashboardData();
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

      <div className="card-surface flex flex-wrap items-center gap-3 p-4">
        <label className="text-sm font-semibold text-ink-secondary" htmlFor="subreddit-select">
          Choose subreddit
        </label>
        <select
          id="subreddit-select"
          className="rounded-full border border-border-default bg-white px-4 py-2 text-sm"
          value={subreddit}
          onChange={(event) => {
            const next = event.target.value;
            if (next) {
              router.push(`/subreddits/${next}`);
            }
          }}
        >
          {(dashboard?.activeSubreddits ?? ["r/technology", "r/science"]).map((item) => {
            const name = item.replace(/^r\//, "");
            return (
              <option key={name} value={name}>
                r/{name}
              </option>
            );
          })}
        </select>
      </div>

      {error && (
        <div className="card-surface p-4 text-sm text-accent-coral">
          {error}
        </div>
      )}

      {data?.kpis?.length ? (
        <div className="grid gap-6 lg:grid-cols-3">
          {data.kpis.map((kpi) => (
            <div key={kpi.label} className="card-surface p-4">
              <p className="metric-label">{kpi.label}</p>
              <p className="mt-2 text-2xl font-semibold text-ink-primary">
                {kpi.value}
              </p>
              <p className="mt-1 text-sm text-ink-secondary">{kpi.delta}</p>
            </div>
          ))}
        </div>
      ) : (
        <div className="card-surface p-4 text-sm text-ink-secondary">
          No subreddit metrics yet. Run ingestion to populate data.
        </div>
      )}

      <Card title="Sentiment trend" subtitle="Rolling average sentiment">
        {data?.sentimentTrend?.length ? (
          <SentimentLineChart data={data?.sentimentTrend ?? []} loading={loading} />
        ) : (
          <div className="text-sm text-ink-secondary">
            No sentiment points yet.
          </div>
        )}
      </Card>

      <Card title="Dominant topics" subtitle="Recurring themes in top posts">
        {data?.topics?.length ? (
          <div className="space-y-3">
            {data?.topics.map((topic, index) => (
              <TrendCard key={`${topic.keyword}-${index}`} {...topic} />
            ))}
          </div>
        ) : (
          <div className="text-sm text-ink-secondary">No topic data yet.</div>
        )}
      </Card>
    </div>
  );
}
