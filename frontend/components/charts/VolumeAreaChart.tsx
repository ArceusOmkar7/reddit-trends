"use client";

import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
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

  return (
    <div className="h-64" role="img" aria-label="Discussion volume chart">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{ top: 10, right: 20, bottom: 0, left: -10 }}>
          <XAxis dataKey="time" tick={{ fill: chartTheme.axis }} />
          <YAxis tick={{ fill: chartTheme.axis }} />
          <Tooltip content={<ChartTooltip />} />
          <Area
            type="monotone"
            dataKey="value"
            stroke={chartTheme.accent}
            fill={chartTheme.accentSoft}
            strokeWidth={2.5}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
