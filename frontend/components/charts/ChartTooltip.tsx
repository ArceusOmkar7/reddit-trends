"use client";

interface ChartTooltipProps {
  active?: boolean;
  payload?: Array<{ value: number; name?: string; payload?: { label?: string } }>;
  label?: string;
}

export default function ChartTooltip({ active, payload, label }: ChartTooltipProps) {
  if (!active || !payload || payload.length === 0) {
    return null;
  }

  const headline = label || payload[0]?.name || payload[0]?.payload?.label;

  return (
    <div className="rounded-xl border border-border-default bg-white px-3 py-2 text-xs text-ink-secondary shadow-card">
      {headline && <p className="text-ink-primary">{headline}</p>}
      {payload.map((item, index) => (
        <p key={`${item.name ?? item.payload?.label ?? "value"}-${index}`}>
          {item.name || item.payload?.label ? `${item.name ?? item.payload?.label}: ` : ""}
          {item.value}
        </p>
      ))}
    </div>
  );
}
