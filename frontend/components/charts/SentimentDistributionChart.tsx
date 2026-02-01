"use client";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer
} from "recharts";
import { chartTheme } from "@/lib/theme";
import ChartTooltip from "@/components/charts/ChartTooltip";

interface DistributionSlice {
  label: string;
  value: number;
}

export default function SentimentDistributionChart({
  data,
  loading
}: {
  data: DistributionSlice[];
  loading?: boolean;
}) {
  if (loading) {
    return <div className="h-64 animate-pulse rounded-2xl bg-surface-lightGray" />;
  }

  const total = data.reduce((sum, slice) => sum + slice.value, 0) || 1;
  if (!data.length || total === 0) {
    return (
      <div className="flex h-64 items-center justify-center text-sm text-ink-secondary">
        No sentiment mix yet.
      </div>
    );
  }

  return (
    <div className="space-y-4" role="img" aria-label="Sentiment distribution chart">
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              dataKey="value"
              nameKey="label"
              innerRadius={55}
              outerRadius={90}
              paddingAngle={4}
            >
              {data.map((slice, index) => (
                <Cell
                  key={slice.label}
                  fill={chartTheme.series[index % chartTheme.series.length]}
                />
              ))}
            </Pie>
            <Tooltip content={<ChartTooltip />} />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div className="grid gap-3 sm:grid-cols-3">
        {data.map((slice, index) => {
          const percent = Math.round((slice.value / total) * 100);
          return (
            <div key={slice.label} className="flex items-center justify-between rounded-xl border border-border-default px-3 py-2">
              <div className="flex items-center gap-2">
                <span
                  className="h-2.5 w-2.5 rounded-full"
                  style={{
                    backgroundColor:
                      chartTheme.series[index % chartTheme.series.length]
                  }}
                />
                <span className="text-sm font-semibold text-ink-primary">
                  {slice.label}
                </span>
              </div>
              <span className="text-sm text-ink-secondary">{percent}%</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
