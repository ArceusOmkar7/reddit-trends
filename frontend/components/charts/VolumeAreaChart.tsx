"use client";

import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from "recharts";
import { chartTheme } from "@/lib/theme";
import ChartTooltip from "@/components/charts/ChartTooltip";

interface VolumePoint {
  time: string;
  value: number;
}

export default function VolumeAreaChart({
  data,
  loading
}: {
  data: VolumePoint[];
  loading?: boolean;
}) {
  if (loading) {
    return <div className="h-64 animate-pulse rounded-2xl bg-surface-lightGray" />;
  }

  if (!data.length) {
    return (
      <div className="flex h-64 items-center justify-center text-sm text-ink-secondary">
        No volume data yet.
      </div>
    );
  }

  return (
    <div
      className="h-64 w-full min-w-0"
      role="img"
      aria-label="Discussion volume chart"
    >
      <ResponsiveContainer width="100%" height={256} minWidth={0}>
        <AreaChart data={data} margin={{ top: 10, right: 16, bottom: 0, left: -4 }}>
          <defs>
            <linearGradient id="volumeFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor={chartTheme.accent} stopOpacity={0.3} />
              <stop offset="95%" stopColor={chartTheme.accent} stopOpacity={0.02} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="4 6" stroke={chartTheme.grid} />
          <XAxis
            dataKey="time"
            tick={{ fill: chartTheme.axis }}
            axisLine={false}
            tickLine={false}
            minTickGap={24}
            interval="preserveStartEnd"
          />
          <YAxis
            tick={{ fill: chartTheme.axis }}
            axisLine={false}
            tickLine={false}
            tickFormatter={(value) => new Intl.NumberFormat(undefined, { notation: "compact" }).format(value)}
          />
          <Tooltip content={<ChartTooltip />} />
          <Area
            type="monotone"
            dataKey="value"
            name="Mentions"
            stroke={chartTheme.accent}
            fill="url(#volumeFill)"
            strokeWidth={2.5}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
