import { useState } from "react";
import { Users, BookOpen, Plus, ChevronRight } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { authApi } from "@/api/auth";
import { useStudentProgress } from "@/hooks/useExercises";
import { Button } from "@/components/ui/Button";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { ProgressChart } from "@/components/dashboard/ProgressChart";
import { ScoreCard } from "@/components/dashboard/ScoreCard";
import { Link } from "react-router-dom";

export function TeacherDashboard() {
  const [selectedStudentId, setSelectedStudentId] = useState<number | null>(null);

  const { data: students, isLoading: loadingStudents } = useQuery({
    queryKey: ["students"],
    queryFn: authApi.getStudents,
  });

  const { data: studentProgress } = useStudentProgress(selectedStudentId);

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Panel Docente</h1>
          <p className="mt-1 text-gray-500">Gestiona ejercicios y monitorea el progreso de tus estudiantes</p>
        </div>
        <Link to="/teacher/exercises">
          <Button>
            <Plus className="h-4 w-4" />
            Nuevo ejercicio
          </Button>
        </Link>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Student list */}
        <Card className="lg:col-span-1">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Users className="h-4 w-4 text-gray-400" />
              <CardTitle>Estudiantes</CardTitle>
            </div>
          </CardHeader>

          {loadingStudents ? (
            <div className="space-y-2">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-12 animate-pulse rounded-lg bg-gray-100" />
              ))}
            </div>
          ) : students && students.length > 0 ? (
            <div className="divide-y divide-gray-100">
              {students.map((student) => (
                <button
                  key={student.id}
                  onClick={() => setSelectedStudentId(student.id)}
                  className={`w-full flex items-center justify-between px-3 py-3 rounded-lg transition-colors text-left ${
                    selectedStudentId === student.id
                      ? "bg-rpp-light text-rpp-purple"
                      : "hover:bg-gray-50 text-gray-700"
                  }`}
                >
                  <div>
                    <p className="text-sm font-medium">{student.full_name}</p>
                    <p className="text-xs text-gray-400">@{student.username}</p>
                  </div>
                  <ChevronRight className="h-4 w-4 text-gray-300" />
                </button>
              ))}
            </div>
          ) : (
            <p className="text-center text-sm text-gray-400 py-6">Sin estudiantes registrados</p>
          )}
        </Card>

        {/* Student progress detail */}
        <div className="lg:col-span-2 space-y-4">
          {selectedStudentId && studentProgress ? (
            <>
              <div className="flex items-center gap-2 mb-2">
                <h2 className="font-semibold text-gray-900">
                  Progreso de: {studentProgress.student.full_name}
                </h2>
              </div>

              {studentProgress.stats_by_level.length > 0 ? (
                <>
                  <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                    {studentProgress.stats_by_level.map((stats) => (
                      <ScoreCard key={stats.level_slug} stats={stats} />
                    ))}
                  </div>
                  <ProgressChart stats={studentProgress.stats_by_level} />
                </>
              ) : (
                <Card className="text-center py-8">
                  <BookOpen className="mx-auto mb-2 h-10 w-10 text-gray-200" />
                  <p className="text-sm text-gray-400">Este estudiante aún no ha practicado</p>
                </Card>
              )}
            </>
          ) : (
            <Card className="flex h-64 items-center justify-center">
              <div className="text-center">
                <Users className="mx-auto mb-3 h-12 w-12 text-gray-200" />
                <p className="text-gray-400">Selecciona un estudiante para ver su progreso</p>
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
