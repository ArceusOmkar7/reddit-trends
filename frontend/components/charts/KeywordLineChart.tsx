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

  return (
    <div className="h-64">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart margin={{ top: 10, right: 20, bottom: 0, left: -10 }}>
          <XAxis dataKey="time" tick={{ fill: chartTheme.axis }} />
          <YAxis tick={{ fill: chartTheme.axis }} />
          <Tooltip content={<ChartTooltip />} />
          {data.map((series, index) => (
            <Line
              key={series.keyword}
              data={series.data}
              dataKey="value"
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
