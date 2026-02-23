import { clsx } from "clsx";
import { Difficulty } from "@/types/exercise";

type Variant = "success" | "warning" | "error" | "info" | "neutral";

interface BadgeProps {
  variant?: Variant;
  children: React.ReactNode;
  className?: string;
}

const variantClasses: Record<Variant, string> = {
  success: "bg-green-100 text-green-700",
  warning: "bg-yellow-100 text-yellow-700",
  error: "bg-red-100 text-red-700",
  info: "bg-blue-100 text-blue-700",
  neutral: "bg-gray-100 text-gray-600",
};

export function Badge({ variant = "neutral", className, children }: BadgeProps) {
  return (
    <span className={clsx("inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium", variantClasses[variant], className)}>
      {children}
    </span>
  );
}

const difficultyVariant: Record<Difficulty, Variant> = {
  basic: "success",
  intermediate: "warning",
  advanced: "error",
};

const difficultyLabel: Record<Difficulty, string> = {
  basic: "Básico",
  intermediate: "Intermedio",
  advanced: "Avanzado",
};

export function DifficultyBadge({ difficulty }: { difficulty: Difficulty }) {
  return <Badge variant={difficultyVariant[difficulty]}>{difficultyLabel[difficulty]}</Badge>;
}
