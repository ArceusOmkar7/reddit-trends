"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Activity,
  BarChart4,
  LineChart,
  Radar,
  Layers,
  Info
} from "lucide-react";
import clsx from "clsx";

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: Activity, match: "/dashboard" },
  { href: "/trends", label: "Trends", icon: LineChart, match: "/trends" },
  { href: "/sentiment", label: "Sentiment", icon: BarChart4, match: "/sentiment" },
  { href: "/subreddits/news", label: "Subreddits", icon: Layers, match: "/subreddits" },
  { href: "/events/launch-week", label: "Events", icon: Radar, match: "/events" },
  { href: "/about", label: "About", icon: Info, match: "/about" }
];

export default function Sidebar() {
  const pathname = usePathname();

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
          Reddit API ingestion every 5 minutes.
        </p>
      </div>
    </aside>
  );
}
