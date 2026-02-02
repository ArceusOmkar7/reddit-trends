"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  ReferenceLine
} from "recharts";
import { chartTheme } from "@/lib/theme";
import ChartTooltip from "@/components/charts/ChartTooltip";

interface SentimentPoint {
  time: string;
  value: number;
}

export default function SentimentLineChart({
  data,
  loading
}: {
  data: SentimentPoint[];
  loading?: boolean;
}) {
  if (loading) {
    return <div className="h-64 animate-pulse rounded-2xl bg-surface-lightGray" />;
  }

  if (!data.length) {
    return (
      <div className="flex h-64 items-center justify-center text-sm text-ink-secondary">
        No sentiment data yet.
      </div>
    );
  }

  return (
    <div
      className="h-64 w-full min-w-0"
      role="img"
      aria-label="Sentiment line chart"
    >
      <ResponsiveContainer width="100%" height={256} minWidth={0}>
        <LineChart data={data} margin={{ top: 10, right: 16, bottom: 0, left: -4 }}>
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
            domain={[-1, 1]}
            axisLine={false}
            tickLine={false}
            tickFormatter={(value) => value.toFixed(2)}
          />
          <ReferenceLine y={0} stroke={chartTheme.axis} strokeDasharray="3 6" />
          <Tooltip content={<ChartTooltip />} />
          <Line
            type="monotone"
            dataKey="value"
            name="Sentiment"
            stroke={chartTheme.primary}
            strokeWidth={3}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
