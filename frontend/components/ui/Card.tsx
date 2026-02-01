interface CardProps {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
}

export default function Card({ title, subtitle, children }: CardProps) {
  return (
    <div className="card-surface p-6">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-ink-primary">{title}</h3>
        {subtitle && <p className="text-sm text-ink-secondary">{subtitle}</p>}
      </div>
      {children}
    </div>
  );
}
