import { HTMLAttributes } from "react";
import { clsx } from "clsx";

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  padding?: "none" | "sm" | "md" | "lg";
}

export function Card({ padding = "md", className, children, ...props }: CardProps) {
  const paddingClasses = { none: "", sm: "p-4", md: "p-6", lg: "p-8" };
  return (
    <div
      className={clsx("rounded-xl border border-gray-200 bg-white shadow-sm", paddingClasses[padding], className)}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardHeader({ className, children, ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={clsx("mb-4 flex items-center justify-between", className)} {...props}>
      {children}
    </div>
  );
}

export function CardTitle({ className, children, ...props }: HTMLAttributes<HTMLHeadingElement>) {
  return (
    <h3 className={clsx("text-lg font-semibold text-gray-900", className)} {...props}>
      {children}
    </h3>
  );
}
