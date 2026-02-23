import { useNavigate } from "react-router-dom";
import { BookOpen, ChevronRight } from "lucide-react";
import { Level } from "@/types/exercise";
import { DifficultyBadge } from "@/components/ui/Badge";
import { clsx } from "clsx";

const difficultyGradient: Record<string, string> = {
  basic: "from-green-400 to-emerald-600",
  intermediate: "from-yellow-400 to-orange-500",
  advanced: "from-red-400 to-rose-600",
};

interface LevelCardProps {
  level: Level;
}

export function LevelCard({ level }: LevelCardProps) {
  const navigate = useNavigate();

  return (
    <button
      onClick={() => navigate(`/exercise/${level.slug}`)}
      className={clsx(
        "group relative w-full overflow-hidden rounded-2xl text-left shadow-md transition-all",
        "hover:shadow-xl hover:-translate-y-1 active:translate-y-0"
      )}
    >
      {/* Gradient header */}
      <div className={clsx("h-28 bg-gradient-to-br", difficultyGradient[level.difficulty] ?? "from-gray-400 to-gray-600")} />

      {/* Content */}
      <div className="bg-white p-5">
        <div className="mb-2 flex items-start justify-between">
          <h3 className="text-lg font-bold text-gray-900 group-hover:text-rpp-purple transition-colors">
            {level.name}
          </h3>
          <DifficultyBadge difficulty={level.difficulty} />
        </div>
        <p className="mb-3 text-sm text-gray-500 line-clamp-2">{level.description}</p>
        <div className="flex items-center justify-between">
          <span className="flex items-center gap-1 text-xs text-gray-400">
            <BookOpen className="h-3.5 w-3.5" />
            {level.exercise_count} ejercicios
          </span>
          <ChevronRight className="h-4 w-4 text-gray-400 group-hover:text-rpp-purple transition-colors" />
        </div>
      </div>
    </button>
  );
}
