import { CheckCircle, XCircle, AlertCircle, ChevronRight } from "lucide-react";
import { EvaluationResult } from "@/api/evaluation";
import { Button } from "@/components/ui/Button";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { clsx } from "clsx";

interface FeedbackModalProps {
  result: EvaluationResult;
  maxScore: number;
  onNext: () => void;
  onRetry: () => void;
}

export function FeedbackModal({ result, maxScore, onNext, onRetry }: FeedbackModalProps) {
  const accuracyColor =
    result.accuracy >= 80 ? "bg-green-500" :
    result.accuracy >= 60 ? "bg-yellow-500" : "bg-red-500";

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4 animate-fade-in">
      <div className="w-full max-w-lg rounded-2xl bg-white p-6 shadow-2xl animate-slide-up">
        {/* Header */}
        <div className="mb-6 text-center">
          <div className={clsx(
            "mx-auto mb-3 flex h-16 w-16 items-center justify-center rounded-full text-3xl font-bold text-white",
            result.accuracy >= 80 ? "bg-green-500" : result.accuracy >= 60 ? "bg-yellow-500" : "bg-red-500"
          )}>
            {result.score.toFixed(0)}
          </div>
          <h3 className="text-xl font-bold text-gray-900">
            {result.accuracy >= 80 ? "¡Excelente!" : result.accuracy >= 60 ? "¡Bien hecho!" : "Sigue practicando"}
          </h3>
          <p className="mt-1 text-sm text-gray-500">{result.feedback.overall_comment}</p>
        </div>

        {/* Stats */}
        <div className="mb-5 space-y-3">
          <ProgressBar label="Precisión" value={result.accuracy} colorClass={accuracyColor} />
          <ProgressBar label="Puntaje" value={result.score} max={maxScore} colorClass="bg-rpp-purple" />
        </div>

        {/* Transcription */}
        {result.transcription && (
          <div className="mb-4 rounded-lg bg-gray-50 p-3">
            <p className="text-xs font-medium uppercase tracking-wide text-gray-400 mb-1">Lo que dijiste:</p>
            <p className="text-sm text-gray-700 italic">"{result.transcription}"</p>
          </div>
        )}

        {/* Word analysis */}
        {result.feedback.word_analysis.length > 0 && (
          <div className="mb-4">
            <p className="text-xs font-medium uppercase tracking-wide text-gray-400 mb-2">Análisis por palabra:</p>
            <div className="flex flex-wrap gap-1.5">
              {result.feedback.word_analysis.map((wa, i) => (
                <span
                  key={i}
                  className={clsx(
                    "rounded-md px-2 py-0.5 text-xs font-medium",
                    wa.is_correct ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"
                  )}
                  title={!wa.is_correct ? `Dijiste: "${wa.transcribed}"` : undefined}
                >
                  {wa.expected}
                  {wa.is_correct ? (
                    <CheckCircle className="ml-0.5 inline h-3 w-3" />
                  ) : (
                    <XCircle className="ml-0.5 inline h-3 w-3" />
                  )}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Suggestions */}
        {result.feedback.suggestions.length > 0 && (
          <div className="mb-5 space-y-1.5">
            {result.feedback.suggestions.map((s, i) => (
              <div key={i} className="flex gap-2 text-sm text-gray-600">
                <AlertCircle className="mt-0.5 h-4 w-4 flex-shrink-0 text-yellow-500" />
                <span>{s}</span>
              </div>
            ))}
          </div>
        )}

        {/* Actions */}
        <div className="flex gap-3">
          <Button variant="secondary" className="flex-1" onClick={onRetry}>
            Intentar de nuevo
          </Button>
          <Button className="flex-1" onClick={onNext}>
            Siguiente <ChevronRight className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}
