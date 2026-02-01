import Badge from "@/components/ui/Badge";

interface StatTileProps {
  label: string;
  value: string;
  delta: string;
  trend: "up" | "down" | "neutral";
}

export default function StatTile({ label, value, delta, trend }: StatTileProps) {
  const variant = trend === "up" ? "green" : trend === "down" ? "orange" : "purple";

  return (
    <div className="card-surface p-5">
      <div className="flex items-center justify-between">
        <p className="metric-label">{label}</p>
        <Badge label={delta} variant={variant} />
      </div>
      <p className="mt-3 text-3xl font-semibold text-ink-primary">{value}</p>
    </div>
  );
}
