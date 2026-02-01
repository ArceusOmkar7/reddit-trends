"use client";

import { usePathname } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { CalendarRange } from "lucide-react";
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
  const [isOpen, setIsOpen] = useState(false);
  const [healthStatus, setHealthStatus] = useState<string | null>(null);
  const [backendStatus, setBackendStatus] = useState<string | null>(null);
  const [healthError, setHealthError] = useState<string | null>(null);
  const [isChecking, setIsChecking] = useState(false);
  const [lastChecked, setLastChecked] = useState<string | null>(null);
  const popoverRef = useRef<HTMLDivElement>(null);
  const statusLabel = backendStatus ?? healthStatus ?? "unknown";
  const statusColor =
    statusLabel === "ok"
      ? "bg-emerald-500"
      : statusLabel === "degraded"
        ? "bg-amber-500"
        : statusLabel === "unreachable"
          ? "bg-rose-500"
          : "bg-slate-300";

  useEffect(() => {
    if (!isOpen) {
      return;
    }
    const handleClick = (event: MouseEvent) => {
      if (!popoverRef.current?.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, [isOpen]);

  useEffect(() => {
    void checkHealth();
  }, []);

  const checkHealth = async () => {
    setIsChecking(true);
    setHealthError(null);
    try {
      const response = await fetch("/api/health", { cache: "no-store" });
      const payload = (await response.json()) as {
        status?: string;
        backend?: string;
      };
      setHealthStatus(payload.status ?? (response.ok ? "ok" : "degraded"));
      setBackendStatus(payload.backend ?? null);
      setLastChecked(new Date().toLocaleString());
    } catch (error) {
      setHealthStatus("degraded");
      setBackendStatus(null);
      setHealthError("Unable to reach health endpoint.");
    } finally {
      setIsChecking(false);
    }
  };

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
            <span>
              {lastRefreshed
                ? `Last refreshed ${lastRefreshed}`
                : "Awaiting refresh"}
            </span>
          </div>
          <div className="relative" ref={popoverRef}>
            <button
              className="flex items-center gap-2 rounded-full border border-border-default px-4 py-2 text-xs font-semibold uppercase tracking-[0.2em] text-ink-secondary hover:text-brand-purple"
              type="button"
              aria-label="Notifications"
              aria-expanded={isOpen}
              onClick={() => {
                const nextOpen = !isOpen;
                setIsOpen(nextOpen);
                if (nextOpen && !healthStatus && !isChecking) {
                  void checkHealth();
                }
              }}
            >
              <span className={`h-2.5 w-2.5 rounded-full ${statusColor}`} />
              Health
            </button>
            {isOpen && (
              <div className="absolute right-0 mt-3 w-72 rounded-2xl border border-border-default bg-white p-4 text-sm shadow-lg">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold uppercase tracking-[0.2em] text-ink-muted">
                    System health
                  </span>
                  <button
                    type="button"
                    onClick={() => void checkHealth()}
                    className="text-xs font-semibold text-brand-purple"
                    disabled={isChecking}
                  >
                    {isChecking ? "Checking..." : "Check now"}
                  </button>
                </div>
                <div className="mt-3 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-ink-secondary">Frontend</span>
                    <span className="font-semibold text-ink-primary">
                      {healthStatus ?? "Unknown"}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-ink-secondary">Backend</span>
                    <span className="font-semibold text-ink-primary">
                      {backendStatus ?? "Unknown"}
                    </span>
                  </div>
                  {healthError && (
                    <p className="text-xs text-accent-coral">{healthError}</p>
                  )}
                  <p className="text-xs text-ink-muted">
                    {lastChecked ? `Last checked ${lastChecked}` : "Not checked yet"}
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
