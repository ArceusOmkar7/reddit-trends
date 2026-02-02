"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Legend
} from "recharts";
import { chartTheme } from "@/lib/theme";
import ChartTooltip from "@/components/charts/ChartTooltip";

interface KeywordPoint {
  time: string;
  value: number;
}

interface KeywordSeries {
  keyword: string;
  data: KeywordPoint[];
}

export default function KeywordLineChart({
  data,
  loading
}: {
  data: KeywordSeries[];
  loading?: boolean;
}) {
  if (loading) {
    return <div className="h-64 animate-pulse rounded-2xl bg-surface-lightGray" />;
  }

  const hasSeries = data.some((series) => series.data?.length);
  if (!hasSeries) {
    return (
      <div className="flex h-64 items-center justify-center text-sm text-ink-secondary">
        No keyword trends yet.
      </div>
    );
  }

  return (
    <div className="h-64 w-full min-w-0">
      <ResponsiveContainer width="100%" height={256} minWidth={0}>
        <LineChart margin={{ top: 10, right: 16, bottom: 0, left: -4 }}>
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
          <Legend
            verticalAlign="top"
            height={32}
            iconType="circle"
            formatter={(value) => <span className="text-xs text-ink-secondary">{value}</span>}
          />
          {data.map((series, index) => (
            <Line
              key={series.keyword}
              data={series.data}
              dataKey="value"
              name={series.keyword}
              stroke={chartTheme.series[index % chartTheme.series.length]}
              strokeWidth={2.5}
              dot={false}
              type="monotone"
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
