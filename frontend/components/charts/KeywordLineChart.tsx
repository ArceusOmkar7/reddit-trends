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
  loading,
  formatTick
}: {
  data: KeywordSeries[];
  loading?: boolean;
  formatTick?: (value: string) => string;
}) {
  if (loading) {
    return <div className="h-64 animate-pulse rounded-2xl bg-surface-lightGray" />;
  }

  const hasSeries = data.some((series) => series.data?.length);
  if (!hasSeries) {
    return (
      <div className="flex h-64 items-center justify-center text-sm text-ink-secondary">
        No term trends yet.
      </div>
    );
  }

  const merged = new Map<string, Record<string, number | string>>();
  const values: number[] = [];
  data.forEach((series) => {
    series.data.forEach((point) => {
      const existing = merged.get(point.time) ?? { time: point.time };
      existing[series.keyword] = point.value;
      merged.set(point.time, existing);
      values.push(point.value);
    });
  });

  const mergedData = Array.from(merged.values()).sort((a, b) =>
    String(a.time).localeCompare(String(b.time))
  );
  const min = values.length ? Math.min(...values) : 0;
  const max = values.length ? Math.max(...values) : 0;
  const pad = Math.max(5, (max - min) * 0.1);

  return (
    <div className="h-64 w-full min-w-0">
      <ResponsiveContainer width="100%" height={256} minWidth={0}>
        <LineChart data={mergedData} margin={{ top: 10, right: 16, bottom: 0, left: -4 }}>
          <CartesianGrid strokeDasharray="4 6" stroke={chartTheme.grid} />
          <XAxis
            dataKey="time"
            tick={{ fill: chartTheme.axis }}
            axisLine={false}
            tickLine={false}
            minTickGap={24}
            interval="preserveStartEnd"
            tickFormatter={(value) =>
              formatTick ? formatTick(String(value)) : String(value)
            }
          />
          <YAxis
            tick={{ fill: chartTheme.axis }}
            axisLine={false}
            tickLine={false}
            tickFormatter={(value) => new Intl.NumberFormat(undefined, { notation: "compact" }).format(value)}
            domain={[min - pad, max + pad]}
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
              dataKey={series.keyword}
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
