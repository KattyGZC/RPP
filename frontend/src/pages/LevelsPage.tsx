import { BookOpen } from "lucide-react";
import { useLevels } from "@/hooks/useExercises";
import { LevelCard } from "@/components/exercises/LevelCard";

export function LevelsPage() {
  const { data: levels, isLoading } = useLevels();

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Elige un nivel</h1>
        <p className="mt-1 text-gray-500">Selecciona el nivel de dificultad para practicar</p>
      </div>

      {isLoading ? (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-56 animate-pulse rounded-2xl bg-gray-200" />
          ))}
        </div>
      ) : levels && levels.length > 0 ? (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {levels.map((level) => (
            <LevelCard key={level.id} level={level} />
          ))}
        </div>
      ) : (
        <div className="rounded-xl border border-dashed border-gray-300 p-12 text-center">
          <BookOpen className="mx-auto mb-3 h-12 w-12 text-gray-300" />
          <p className="text-gray-400">No hay niveles disponibles aún.</p>
        </div>
      )}
    </div>
  );
}
