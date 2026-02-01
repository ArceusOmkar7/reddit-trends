"use client";

interface ChartTooltipProps {
  active?: boolean;
  payload?: Array<{ value: number; name?: string }>; 
  label?: string;
}

export default function ChartTooltip({ active, payload, label }: ChartTooltipProps) {
  if (!active || !payload || payload.length === 0) {
    return null;
  }

  return (
    <div className="rounded-xl border border-border-default bg-white px-3 py-2 text-xs text-ink-secondary shadow-card">
      <p className="text-ink-primary">{label}</p>
      {payload.map((item, index) => (
        <p key={`${item.name ?? "value"}-${index}`}>{item.value}</p>
      ))}
    </div>
  );
}
