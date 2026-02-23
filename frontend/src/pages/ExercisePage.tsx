import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { ArrowLeft, BookOpen } from "lucide-react";
import { useMutation } from "@tanstack/react-query";
import { useExercises } from "@/hooks/useExercises";
import { useMediaRecorder } from "@/hooks/useMediaRecorder";
import { evaluationApi, EvaluationResult } from "@/api/evaluation";
import { Exercise } from "@/types/exercise";
import { RecordingControls } from "@/components/exercises/RecordingControls";
import { FeedbackModal } from "@/components/exercises/FeedbackModal";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";

export function ExercisePage() {
  const { levelSlug } = useParams<{ levelSlug: string }>();
  const navigate = useNavigate();
  const { data: exercises, isLoading } = useExercises(levelSlug ?? null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [evaluationResult, setEvaluationResult] = useState<EvaluationResult | null>(null);

  const { recordingState, elapsedSeconds, startRecording, stopRecording, error } = useMediaRecorder();

  const evaluateMutation = useMutation({
    mutationFn: async ({ blob, exercise }: { blob: Blob; exercise: Exercise }) => {
      return evaluationApi.evaluate(blob, exercise.id, elapsedSeconds);
    },
    onSuccess: (result) => setEvaluationResult(result),
  });

  const currentExercise = exercises?.[currentIndex];

  const handleStop = async () => {
    if (!currentExercise) return;
    const blob = await stopRecording();
    if (blob) {
      evaluateMutation.mutate({ blob, exercise: currentExercise });
    }
  };

  const handleNext = () => {
    setEvaluationResult(null);
    if (exercises && currentIndex < exercises.length - 1) {
      setCurrentIndex((i) => i + 1);
    } else {
      navigate("/dashboard");
    }
  };

  const handleRetry = () => setEvaluationResult(null);

  if (isLoading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-rpp-purple border-t-transparent" />
      </div>
    );
  }

  if (!exercises || exercises.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-400">No hay ejercicios disponibles para este nivel.</p>
        <Button variant="ghost" className="mt-4" onClick={() => navigate("/levels")}>
          <ArrowLeft className="h-4 w-4" /> Volver a niveles
        </Button>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-2xl space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center gap-3">
        <Button variant="ghost" size="sm" onClick={() => navigate("/levels")}>
          <ArrowLeft className="h-4 w-4" />
        </Button>
        <div>
          <h1 className="text-xl font-bold text-gray-900">{currentExercise?.level_name}</h1>
          <p className="text-sm text-gray-400">
            Ejercicio {currentIndex + 1} de {exercises.length}
          </p>
        </div>
      </div>

      {/* Progress dots */}
      <div className="flex gap-1.5">
        {exercises.map((_, i) => (
          <div
            key={i}
            className={`h-1.5 flex-1 rounded-full transition-colors ${
              i < currentIndex ? "bg-green-400" : i === currentIndex ? "bg-rpp-purple" : "bg-gray-200"
            }`}
          />
        ))}
      </div>

      {/* Exercise card */}
      <Card>
        <div className="mb-4 flex items-start gap-3">
          <div className="rounded-lg bg-rpp-light p-2">
            <BookOpen className="h-5 w-5 text-rpp-purple" />
          </div>
          <div>
            <h2 className="font-semibold text-gray-900">{currentExercise?.title}</h2>
            <p className="text-xs text-gray-400 mt-0.5">Puntuación máxima: {currentExercise?.max_score} pts</p>
          </div>
        </div>

        {/* Text to read */}
        <div className="mb-6 rounded-xl bg-gray-50 p-5">
          <p className="text-lg leading-relaxed text-gray-800 font-medium">
            {currentExercise?.text}
          </p>
        </div>

        {/* Recording controls */}
        <RecordingControls
          recordingState={recordingState}
          elapsedSeconds={elapsedSeconds}
          isEvaluating={evaluateMutation.isPending}
          onStart={startRecording}
          onStop={handleStop}
          error={error || (evaluateMutation.isError ? "Error al evaluar. Intenta de nuevo." : null)}
        />
      </Card>

      {/* Feedback modal */}
      {evaluationResult && currentExercise && (
        <FeedbackModal
          result={evaluationResult}
          maxScore={currentExercise.max_score}
          onNext={handleNext}
          onRetry={handleRetry}
        />
      )}
    </div>
  );
}
