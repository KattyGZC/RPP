import { TrendingUp, Trophy, Target } from "lucide-react";
import { LevelStats } from "@/types/exercise";
import { Card } from "@/components/ui/Card";
import { DifficultyBadge } from "@/components/ui/Badge";
import { ProgressBar } from "@/components/ui/ProgressBar";

interface ScoreCardProps {
  stats: LevelStats;
  maxPossibleScore?: number;
}

export function ScoreCard({ stats, maxPossibleScore = 100 }: ScoreCardProps) {
  return (
    <Card className="hover:shadow-md transition-shadow">
      <div className="mb-3 flex items-center justify-between">
        <h4 className="font-semibold text-gray-900">{stats.level_name}</h4>
        <DifficultyBadge difficulty={stats.difficulty} />
      </div>

      <div className="mb-4 grid grid-cols-3 gap-3 text-center">
        <div>
          <div className="flex justify-center text-yellow-500 mb-1">
            <Trophy className="h-4 w-4" />
          </div>
          <p className="text-lg font-bold text-gray-900">{stats.best_score.toFixed(0)}</p>
          <p className="text-xs text-gray-400">Mejor</p>
        </div>
        <div>
          <div className="flex justify-center text-blue-500 mb-1">
            <TrendingUp className="h-4 w-4" />
          </div>
          <p className="text-lg font-bold text-gray-900">{stats.avg_score.toFixed(0)}</p>
          <p className="text-xs text-gray-400">Promedio</p>
        </div>
        <div>
          <div className="flex justify-center text-green-500 mb-1">
            <Target className="h-4 w-4" />
          </div>
          <p className="text-lg font-bold text-gray-900">{stats.total_sessions}</p>
          <p className="text-xs text-gray-400">Sesiones</p>
        </div>
      </div>

      <ProgressBar
        label="Precisión promedio"
        value={stats.avg_accuracy}
        colorClass={stats.avg_accuracy >= 75 ? "bg-green-500" : stats.avg_accuracy >= 50 ? "bg-yellow-500" : "bg-red-500"}
      />
    </Card>
  );
}
