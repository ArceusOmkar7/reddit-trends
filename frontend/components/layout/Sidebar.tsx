"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import {
  Activity,
  BarChart4,
  LineChart,
  Radar,
  Layers,
  Info
} from "lucide-react";
import clsx from "clsx";
import { usePollingContext } from "@/components/layout/PollingContext";

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: Activity, match: "/dashboard" },
  { href: "/trends", label: "Trends", icon: LineChart, match: "/trends" },
  { href: "/sentiment", label: "Sentiment", icon: BarChart4, match: "/sentiment" },
  { href: "/subreddits/worldnews", label: "Subreddits", icon: Layers, match: "/subreddits" },
  { href: "/events/elections", label: "Events", icon: Radar, match: "/events" },
  { href: "/about", label: "About", icon: Info, match: "/about" }
];

export default function Sidebar() {
  const pathname = usePathname();
  const pollIntervalSeconds = Number(
    process.env.NEXT_PUBLIC_POLL_INTERVAL_SECONDS ?? 300
  );
  const { state } = usePollingContext();
  const [pollIntervalMs, setPollIntervalMs] = useState(
    Math.max(pollIntervalSeconds, 30) * 1000
  );
  const [nextPollAt, setNextPollAt] = useState<number | null>(null);
  const [now, setNow] = useState<number | null>(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    const start = Date.now();
    setNow(start);
    setNextPollAt(start + pollIntervalMs);
    setMounted(true);
    const tick = () => setNow(Date.now());
    const interval = setInterval(tick, 1000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (!state) {
      return;
    }
    setPollIntervalMs(Math.max(state.intervalSeconds ?? pollIntervalSeconds, 30) * 1000);
    if (state.nextRun) {
      setNextPollAt(new Date(state.nextRun).getTime());
    } else if (state.enabled === false) {
      setNextPollAt(null);
    }
  }, [state, pollIntervalSeconds]);

  useEffect(() => {
    if (now !== null && nextPollAt !== null && now >= nextPollAt) {
      setNextPollAt(Date.now() + pollIntervalMs);
    }
  }, [now, nextPollAt, pollIntervalMs]);

  const countdown = useMemo(() => {
    if (state?.enabled === false) {
      return "Paused";
    }
    if (now === null || nextPollAt === null) {
      return "--:--";
    }
    const remainingMs = Math.max(nextPollAt - now, 0);
    const remainingSeconds = Math.ceil(remainingMs / 1000);
    const minutes = Math.floor(remainingSeconds / 60)
      .toString()
      .padStart(2, "0");
    const seconds = (remainingSeconds % 60).toString().padStart(2, "0");
    return `${minutes}:${seconds}`;
  }, [nextPollAt, now]);

  const nextPollLabel =
    mounted && nextPollAt !== null
      ? new Intl.DateTimeFormat(undefined, {
          hour: "2-digit",
          minute: "2-digit"
        }).format(new Date(nextPollAt))
      : state?.enabled === false
        ? "—"
        : "--:--";

  return (
    <aside className="sticky top-0 hidden h-screen w-64 flex-col border-r border-border-default bg-white px-5 py-6 lg:flex">
      <div className="mb-10 flex items-center gap-2">
        <div className="flex h-9 w-9 items-center justify-center rounded-full bg-brand-purple text-white shadow-button">
          <span className="text-sm font-semibold">rt</span>
        </div>
        <div>
          <p className="text-sm font-semibold text-ink-primary">reddit trends</p>
          <p className="text-xs text-ink-muted">intelligence</p>
        </div>
      </div>

      <nav className="space-y-2">
        {navItems.map(({ href, label, icon: Icon, match }) => {
          const isActive = pathname === match || pathname.startsWith(`${match}/`);
          return (
            <Link
              key={href}
              href={href}
              className={clsx(
                "flex items-center gap-3 rounded-full px-4 py-2 text-sm font-semibold transition",
                isActive
                  ? "bg-brand-purple text-white shadow-button"
                  : "text-ink-secondary hover:text-brand-purple"
              )}
            >
              <Icon size={18} />
              {label}
            </Link>
          );
        })}
      </nav>

      <div className="mt-auto rounded-2xl bg-surface-peachTint p-4">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-accent-orange">
          Live polling
        </p>
        <p className="mt-2 text-sm text-ink-secondary">
          Reddit API ingestion every {Math.round(pollIntervalMs / 60000)} minutes.
        </p>
        <div className="mt-3 text-sm text-ink-secondary">
          <span className="font-semibold text-ink-primary">Next poll</span> in {countdown}
        </div>
        <p className="text-xs text-ink-muted">
          {state?.enabled === false ? "Polling paused" : `Scheduled at ${nextPollLabel}`}
        </p>
      </div>
    </aside>
  );
}
