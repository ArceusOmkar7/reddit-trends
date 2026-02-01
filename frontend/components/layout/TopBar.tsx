"use client";

import { usePathname } from "next/navigation";
import { Bell, CalendarRange } from "lucide-react";
import { useRefreshContext } from "@/components/layout/RefreshContext";

const routeLabels: Record<string, string> = {
  "/dashboard": "Dashboard",
  "/trends": "Trends",
  "/sentiment": "Sentiment",
  "/about": "System Info"
};

function getRouteContext(pathname: string) {
  if (pathname.startsWith("/subreddits/")) {
    return `Subreddit: r/${pathname.split("/")[2]}`;
  }
  if (pathname.startsWith("/events/")) {
    return `Event: ${pathname.split("/")[2]}`;
  }
  return routeLabels[pathname] ?? "Overview";
}

export default function TopBar() {
  const pathname = usePathname();
  const { lastRefreshed } = useRefreshContext();

  return (
    <header className="sticky top-0 z-20 border-b border-border-default bg-white/80 px-6 py-4 backdrop-blur lg:px-10">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-ink-muted">
            {getRouteContext(pathname)}
          </p>
          <h1 className="mt-1 text-xl font-semibold text-ink-primary">
            Reddit Intelligence Dashboard
          </h1>
        </div>

        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 rounded-full border border-border-default bg-white px-4 py-2 text-sm text-ink-secondary">
            <CalendarRange size={16} />
            <span>{lastRefreshed ?? "Awaiting refresh"}</span>
          </div>
          <button className="flex h-10 w-10 items-center justify-center rounded-full border border-border-default text-ink-secondary hover:text-brand-purple">
            <Bell size={18} />
          </button>
        </div>
      </div>
    </header>
  );
}
