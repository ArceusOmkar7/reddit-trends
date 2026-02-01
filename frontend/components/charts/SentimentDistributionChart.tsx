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

  return (
    <div className="h-64" role="img" aria-label="Sentiment distribution chart">
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
  );
}
