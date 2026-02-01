"use client";

import { useEffect } from "react";
import { useParams } from "next/navigation";
import SectionHeader from "@/components/ui/SectionHeader";
import Card from "@/components/ui/Card";
import Breadcrumbs from "@/components/layout/Breadcrumbs";
import VolumeAreaChart from "@/components/charts/VolumeAreaChart";
import SentimentLineChart from "@/components/charts/SentimentLineChart";
import TrendCard from "@/components/ui/TrendCard";
import { useEventData } from "@/lib/hooks/useEventData";
import { useRefreshContext } from "@/components/layout/RefreshContext";

export default function EventPage() {
  const params = useParams<{ eventId: string }>();
  const eventId = params?.eventId ?? "";
  const { data, loading, error, refetch } = useEventData(eventId);
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
          { label: "Events", href: "/dashboard" },
          { label: eventId }
        ]}
      />
      <SectionHeader
        title={`Event monitoring: ${eventId}`}
        accent="pulse"
        description="Real-time discussion growth and sentiment shifts." 
        actionLabel="Refresh"
        onAction={refetch}
      />

      {error && (
        <div className="card-surface p-4 text-sm text-accent-coral">
          {error}
        </div>
      )}

      <div className="grid gap-6 lg:grid-cols-2">
        <Card title="Discussion growth" subtitle="Mentions over time">
          <VolumeAreaChart data={data?.volumeTrend ?? []} loading={loading} />
        </Card>
        <Card title="Sentiment shift" subtitle="Event sentiment delta">
          <SentimentLineChart data={data?.sentimentTrend ?? []} loading={loading} />
        </Card>
      </div>

      <Card title="Event-specific trends" subtitle="Keywords driving the conversation">
        <div className="space-y-3">
          {data?.topicCards.map((topic) => (
            <TrendCard key={topic.keyword} {...topic} />
          ))}
        </div>
      </Card>
    </div>
  );
}
