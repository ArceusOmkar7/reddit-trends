"use client";

import clsx from "clsx";

interface SectionHeaderProps {
  title: string;
  accent: string;
  description: string;
  actionLabel?: string;
  onAction?: () => void;
}

export default function SectionHeader({
  title,
  accent,
  description,
  actionLabel,
  onAction
}: SectionHeaderProps) {
  return (
    <div className="flex flex-wrap items-center justify-between gap-4">
      <div className="max-w-2xl">
        <p className="metric-label">Live analytics</p>
        <h2 className="mt-2 text-3xl font-semibold text-ink-primary">
          {title}{" "}
          <span className="text-brand-purple italic">{accent}</span>
        </h2>
        <p className="mt-3 text-sm text-ink-secondary">{description}</p>
      </div>
      {actionLabel && onAction && (
        <button
          onClick={onAction}
          className={clsx(
            "rounded-full bg-brand-purple px-6 py-2 text-sm font-semibold text-white shadow-button transition",
            "hover:-translate-y-0.5 hover:shadow-lg"
          )}
        >
          {actionLabel}
        </button>
      )}
    </div>
  );
}
