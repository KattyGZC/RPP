import { Link } from "react-router-dom";
import { BookOpen, ChevronRight, Clock } from "lucide-react";
import { useAuthStore } from "@/store/authStore";
import { useMyProgress } from "@/hooks/useExercises";
import { ScoreCard } from "@/components/dashboard/ScoreCard";
import { ProgressChart } from "@/components/dashboard/ProgressChart";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";

export function DashboardPage() {
  const { user } = useAuthStore();
  const { data: progress, isLoading } = useMyProgress();

  const hour = new Date().getHours();
  const greeting = hour < 12 ? "Buenos días" : hour < 18 ? "Buenas tardes" : "Buenas noches";

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Welcome header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            {greeting}, {user?.first_name || user?.username} 👋
          </h1>
          <p className="mt-1 text-gray-500">Aquí está tu progreso de lectura</p>
        </div>
        <Link to="/levels">
          <Button>
            <BookOpen className="h-4 w-4" />
            Practicar ahora
          </Button>
        </Link>
      </div>

      {isLoading ? (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-48 animate-pulse rounded-xl bg-gray-200" />
          ))}
        </div>
      ) : (
        <>
          {/* Stats cards */}
          {progress?.stats_by_level && progress.stats_by_level.length > 0 ? (
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {progress.stats_by_level.map((stats) => (
                <ScoreCard key={stats.level_slug} stats={stats} />
              ))}
            </div>
          ) : (
            <Card className="text-center py-10">
              <BookOpen className="mx-auto mb-3 h-12 w-12 text-gray-300" />
              <h3 className="font-semibold text-gray-700">Sin actividad aún</h3>
              <p className="mt-1 text-sm text-gray-400 mb-4">Completa tu primer ejercicio de lectura para ver tu progreso aquí</p>
              <Link to="/levels">
                <Button>Comenzar a leer</Button>
              </Link>
            </Card>
          )}

          {/* Chart */}
          {progress?.stats_by_level && progress.stats_by_level.length > 0 && (
            <ProgressChart stats={progress.stats_by_level} />
          )}

          {/* Recent sessions */}
          {progress?.recent_sessions && progress.recent_sessions.length > 0 && (
            <Card>
              <div className="mb-4 flex items-center gap-2">
                <Clock className="h-4 w-4 text-gray-400" />
                <h3 className="font-semibold text-gray-900">Sesiones recientes</h3>
              </div>
              <div className="divide-y divide-gray-100">
                {progress.recent_sessions.slice(0, 5).map((session) => (
                  <div key={session.id} className="flex items-center justify-between py-3">
                    <div>
                      <p className="text-sm font-medium text-gray-900">{session.exercise_title}</p>
                      <p className="text-xs text-gray-400">{session.level_name} · {new Date(session.created_at).toLocaleDateString("es-EC")}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-bold text-rpp-purple">{session.score.toFixed(0)} pts</p>
                      <p className="text-xs text-gray-400">{session.accuracy.toFixed(0)}% precisión</p>
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          )}
        </>
      )}
    </div>
  );
}
