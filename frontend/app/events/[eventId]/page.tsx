"use client";

import { useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import SectionHeader from "@/components/ui/SectionHeader";
import Card from "@/components/ui/Card";
import Breadcrumbs from "@/components/layout/Breadcrumbs";
import VolumeAreaChart from "@/components/charts/VolumeAreaChart";
import SentimentLineChart from "@/components/charts/SentimentLineChart";
import TrendCard from "@/components/ui/TrendCard";
import { useEventData } from "@/lib/hooks/useEventData";
import { useRefreshContext } from "@/components/layout/RefreshContext";
import { useDashboardData } from "@/lib/hooks/useDashboardData";

export default function EventPage() {
  const params = useParams<{ eventId: string }>();
  const router = useRouter();
  const eventId = params?.eventId
    ? decodeURIComponent(params.eventId)
    : "";
  const { data, loading, error, refetch } = useEventData(eventId);
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
          { label: "Events", href: `/events/${encodeURIComponent(eventId)}` },
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

      <div className="card-surface flex flex-wrap items-center gap-3 p-4">
        <label className="text-sm font-semibold text-ink-secondary" htmlFor="event-select">
          Choose event
        </label>
        <select
          id="event-select"
          className="rounded-full border border-border-default bg-white px-4 py-2 text-sm"
          value={eventId}
          onChange={(event) => {
            const next = event.target.value;
            if (next) {
              router.push(`/events/${encodeURIComponent(next)}`);
            }
          }}
        >
          {(() => {
            const list = dashboard?.activeEvents ?? ["elections", "ai releases"];
            const options = list.includes(eventId)
              ? list
              : [eventId || list[0], ...list];
            return options.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ));
          })()}
        </select>
      </div>

      {error && (
        <div className="card-surface p-4 text-sm text-accent-coral">
          {error}
        </div>
      )}

      <div className="grid gap-6 lg:grid-cols-2">
        <Card title="Discussion growth" subtitle="Mentions over time">
          {data?.volumeTrend?.length ? (
            <VolumeAreaChart data={data?.volumeTrend ?? []} loading={loading} />
          ) : (
            <div className="text-sm text-ink-secondary">No event volume yet.</div>
          )}
        </Card>
        <Card title="Sentiment shift" subtitle="Event sentiment delta">
          {data?.sentimentTrend?.length ? (
            <SentimentLineChart data={data?.sentimentTrend ?? []} loading={loading} />
          ) : (
            <div className="text-sm text-ink-secondary">No sentiment points yet.</div>
          )}
        </Card>
      </div>

      <Card title="Event-specific trends" subtitle="Keywords driving the conversation">
        {data?.topicCards?.length ? (
          <div className="space-y-3">
            {data?.topicCards.map((topic, index) => (
              <TrendCard key={`${topic.keyword}-${index}`} {...topic} />
            ))}
          </div>
        ) : (
          <div className="text-sm text-ink-secondary">No event topics yet.</div>
        )}
      </Card>
    </div>
  );
}
