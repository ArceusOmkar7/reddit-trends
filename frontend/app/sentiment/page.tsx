"use client";

import { useEffect } from "react";
import SectionHeader from "@/components/ui/SectionHeader";
import Card from "@/components/ui/Card";
import SentimentDistributionChart from "@/components/charts/SentimentDistributionChart";
import SentimentLineChart from "@/components/charts/SentimentLineChart";
import { useSentimentData } from "@/lib/hooks/useSentimentData";
import { useRefreshContext } from "@/components/layout/RefreshContext";

export default function SentimentPage() {
  const { data, loading, error, refetch } = useSentimentData();
  const { setLastRefreshed } = useRefreshContext();

  useEffect(() => {
    if (data?.lastUpdated) {
      setLastRefreshed(data.lastUpdated);
    }
  }, [data?.lastUpdated, setLastRefreshed]);

  return (
    <div className="space-y-8">
      <SectionHeader
        title="Sentiment"
        accent="analysis"
        description="Understand distribution and shifts across subreddits." 
        actionLabel="Refresh"
        onAction={refetch}
      />

      {error && (
        <div className="card-surface p-4 text-sm text-accent-coral">
          {error}
        </div>
      )}

      <div className="grid gap-6 lg:grid-cols-2">
        <Card title="Sentiment mix" subtitle="Positive, neutral, negative ratio">
          <SentimentDistributionChart data={data?.distribution ?? []} loading={loading} />
        </Card>
        <Card title="Sentiment timeline" subtitle="Rolling average over 24 hours">
          <SentimentLineChart data={data?.timeline ?? []} loading={loading} />
        </Card>
      </div>
    </div>
  );
}
