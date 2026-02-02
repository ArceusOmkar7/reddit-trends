import Badge from "@/components/ui/Badge";

interface TrendCardProps {
  keyword: string;
  velocity: string;
  context?: string;
  sentiment?: string;
  spike?: string;
}

export default function TrendCard({
  keyword,
  velocity,
  context,
  sentiment,
  spike
}: TrendCardProps) {
  return (
    <div className="flex flex-wrap items-center justify-between gap-4 rounded-2xl border border-border-default bg-surface-lightGray/60 px-5 py-4">
      <div>
        <p className="text-base font-semibold text-ink-primary">{keyword}</p>
        {context && <p className="text-sm text-ink-secondary">{context}</p>}
      </div>
      <div className="flex flex-wrap items-center gap-2 text-sm">
        <Badge label={velocity} variant="green" />
        {sentiment && <Badge label={sentiment} variant="purple" />}
        {spike && <Badge label={spike} variant="orange" />}
      </div>
    </div>
  );
}
