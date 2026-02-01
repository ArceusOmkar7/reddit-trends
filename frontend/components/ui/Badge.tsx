import clsx from "clsx";

type BadgeVariant = "purple" | "orange" | "green";

const variants: Record<BadgeVariant, string> = {
  purple: "bg-[#EDE9FF] text-brand-purple",
  orange: "bg-[#FFF0E8] text-accent-orange",
  green: "bg-[#ECFDF5] text-accent-green"
};

export default function Badge({
  label,
  variant = "purple"
}: {
  label: string;
  variant?: BadgeVariant;
}) {
  return <span className={clsx("pill", variants[variant])}>{label}</span>;
}
