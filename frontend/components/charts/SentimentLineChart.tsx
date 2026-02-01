"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
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

  return (
    <div
      className="h-64 w-full min-w-0"
      role="img"
      aria-label="Sentiment line chart"
    >
      <ResponsiveContainer width="100%" height={256} minWidth={0}>
        <LineChart data={data} margin={{ top: 10, right: 20, bottom: 0, left: -10 }}>
          <XAxis dataKey="time" tick={{ fill: chartTheme.axis }} />
          <YAxis tick={{ fill: chartTheme.axis }} domain={[-1, 1]} />
          <Tooltip content={<ChartTooltip />} />
          <Line
            type="monotone"
            dataKey="value"
            stroke={chartTheme.primary}
            strokeWidth={3}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
