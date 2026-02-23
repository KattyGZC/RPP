import { useState } from "react";
import { useForm } from "react-hook-form";
import { Plus, Trash2, Edit2, BookOpen } from "lucide-react";
import { useLevels, useExercises, useCreateExercise, useDeleteExercise } from "@/hooks/useExercises";
import { Button } from "@/components/ui/Button";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { DifficultyBadge } from "@/components/ui/Badge";
import { Level } from "@/types/exercise";

interface ExerciseFormData {
  level_id: number;
  title: string;
  text: string;
  max_score: number;
}

export function ExerciseManager() {
  const [selectedLevel, setSelectedLevel] = useState<Level | null>(null);
  const [showForm, setShowForm] = useState(false);

  const { data: levels } = useLevels();
  const { data: exercises } = useExercises(selectedLevel?.slug ?? null);
  const createMutation = useCreateExercise();
  const deleteMutation = useDeleteExercise();

  const { register, handleSubmit, reset, formState: { errors } } = useForm<ExerciseFormData>();

  const onSubmit = (data: ExerciseFormData) => {
    createMutation.mutate(
      { ...data, level_id: Number(data.level_id), max_score: Number(data.max_score) },
      {
        onSuccess: () => { reset(); setShowForm(false); }
      }
    );
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Gestión de Ejercicios</h1>
        <Button onClick={() => setShowForm(true)}>
          <Plus className="h-4 w-4" /> Nuevo ejercicio
        </Button>
      </div>

      {/* Level filter */}
      <div className="flex flex-wrap gap-2">
        {levels?.map((level) => (
          <button
            key={level.id}
            onClick={() => setSelectedLevel(level)}
            className={`rounded-full px-4 py-1.5 text-sm font-medium transition-colors ${
              selectedLevel?.id === level.id
                ? "bg-rpp-purple text-white"
                : "bg-gray-100 text-gray-600 hover:bg-gray-200"
            }`}
          >
            {level.name}
          </button>
        ))}
      </div>

      {/* Create form */}
      {showForm && (
        <Card>
          <CardHeader>
            <CardTitle>Crear ejercicio</CardTitle>
            <button onClick={() => setShowForm(false)} className="text-gray-400 hover:text-gray-600 text-sm">
              Cancelar
            </button>
          </CardHeader>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">Nivel</label>
                <select
                  {...register("level_id", { required: "Requerido" })}
                  className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-rpp-purple focus:outline-none"
                >
                  <option value="">Selecciona...</option>
                  {levels?.map((l) => <option key={l.id} value={l.id}>{l.name}</option>)}
                </select>
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">Puntaje máximo</label>
                <input
                  {...register("max_score", { required: "Requerido", min: 1 })}
                  type="number"
                  defaultValue={100}
                  className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-rpp-purple focus:outline-none"
                />
              </div>
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">Título</label>
              <input
                {...register("title", { required: "Requerido" })}
                className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-rpp-purple focus:outline-none"
                placeholder="Ej: El sol y la luna"
              />
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">Texto de lectura</label>
              <textarea
                {...register("text", { required: "Requerido", minLength: { value: 10, message: "Mínimo 10 caracteres" } })}
                rows={4}
                className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-rpp-purple focus:outline-none"
                placeholder="Escribe el texto que el estudiante deberá leer..."
              />
            </div>

            <Button type="submit" isLoading={createMutation.isPending}>
              Guardar ejercicio
            </Button>
          </form>
        </Card>
      )}

      {/* Exercise list */}
      {selectedLevel && (
        <Card padding="none">
          <div className="p-4 border-b border-gray-100 flex items-center gap-2">
            <BookOpen className="h-4 w-4 text-gray-400" />
            <span className="font-medium text-gray-700">{selectedLevel.name}</span>
            <DifficultyBadge difficulty={selectedLevel.difficulty} />
          </div>
          {exercises && exercises.length > 0 ? (
            <div className="divide-y divide-gray-100">
              {exercises.map((ex) => (
                <div key={ex.id} className="flex items-center justify-between p-4 hover:bg-gray-50">
                  <div className="flex-1 min-w-0">
                    <p className="font-medium text-gray-900 truncate">{ex.title}</p>
                    <p className="text-xs text-gray-400 mt-0.5 line-clamp-1">{ex.text}</p>
                  </div>
                  <div className="flex items-center gap-2 ml-3">
                    <span className="text-xs text-gray-400">{ex.max_score} pts</span>
                    <button
                      onClick={() => deleteMutation.mutate(ex.id)}
                      className="rounded p-1.5 text-gray-400 hover:bg-red-50 hover:text-red-500 transition-colors"
                    >
                      <Trash2 className="h-3.5 w-3.5" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-center text-sm text-gray-400 py-8">No hay ejercicios en este nivel</p>
          )}
        </Card>
      )}
    </div>
  );
}
