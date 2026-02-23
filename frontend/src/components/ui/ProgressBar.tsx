import { clsx } from "clsx";

interface ProgressBarProps {
  value: number;
  max?: number;
  label?: string;
  showPercent?: boolean;
  className?: string;
  colorClass?: string;
}

export function ProgressBar({
  value,
  max = 100,
  label,
  showPercent = true,
  className,
  colorClass = "bg-rpp-purple",
}: ProgressBarProps) {
  const percent = Math.min(100, Math.round((value / max) * 100));

  return (
    <div className={clsx("w-full", className)}>
      {(label || showPercent) && (
        <div className="mb-1 flex items-center justify-between text-sm">
          {label && <span className="text-gray-600">{label}</span>}
          {showPercent && <span className="font-medium text-gray-900">{percent}%</span>}
        </div>
      )}
      <div className="h-2 w-full overflow-hidden rounded-full bg-gray-200">
        <div
          className={clsx("h-full rounded-full transition-all duration-500", colorClass)}
          style={{ width: `${percent}%` }}
        />
      </div>
    </div>
  );
}
