import Card from "@/components/ui/Card";
import IngestionControl from "@/components/ui/IngestionControl";

export default function AboutPage() {
  return (
    <div className="space-y-8">
      <div className="card-surface p-6">
        <p className="metric-label">System info</p>
        <h1 className="mt-3 text-3xl font-semibold text-ink-primary">
          Reddit Trends Intelligence Platform
        </h1>
        <p className="mt-3 text-sm text-ink-secondary">
          A lightweight system for tracking sentiment and emerging discussions across
          targeted subreddits and event keywords. Built with a focus on transparency and
          ethical use of public data.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <Card title="Data source" subtitle="Reddit API polling">
          <p className="text-sm text-ink-secondary">
            The platform ingests public posts and comments from selected subreddits at a
            five-minute interval. No user-level profiling is performed.
          </p>
        </Card>
        <Card title="Ingestion control" subtitle="Pause or resume polling">
          <IngestionControl />
        </Card>
        <Card title="Update frequency" subtitle="Near real-time">
          <p className="text-sm text-ink-secondary">
            Polling-based updates occur every 5 minutes with aggregated metrics stored
            for fast retrieval and dashboard performance.
          </p>
        </Card>
        <Card title="Ethical considerations" subtitle="Transparency first">
          <p className="text-sm text-ink-secondary">
            Only public data is used. No attempts are made to identify individuals or
            infer private attributes.
          </p>
        </Card>
      </div>
    </div>
  );
}
