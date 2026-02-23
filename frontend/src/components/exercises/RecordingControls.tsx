import { Mic, MicOff, Square, Loader2 } from "lucide-react";
import { clsx } from "clsx";
import { RecordingState } from "@/hooks/useMediaRecorder";
import { Button } from "@/components/ui/Button";

interface RecordingControlsProps {
  recordingState: RecordingState;
  elapsedSeconds: number;
  isEvaluating: boolean;
  onStart: () => void;
  onStop: () => void;
  error: string | null;
}

function formatTime(seconds: number): string {
  const m = Math.floor(seconds / 60).toString().padStart(2, "0");
  const s = (seconds % 60).toString().padStart(2, "0");
  return `${m}:${s}`;
}

export function RecordingControls({
  recordingState,
  elapsedSeconds,
  isEvaluating,
  onStart,
  onStop,
  error,
}: RecordingControlsProps) {
  return (
    <div className="flex flex-col items-center gap-4">
      {/* Recording indicator */}
      {recordingState === "recording" && (
        <div className="flex items-center gap-2 text-red-600">
          <span className="h-3 w-3 animate-pulse rounded-full bg-red-500" />
          <span className="font-mono text-sm font-medium">{formatTime(elapsedSeconds)}</span>
        </div>
      )}

      {/* Main control button */}
      <div className="flex items-center gap-3">
        {recordingState !== "recording" ? (
          <button
            onClick={onStart}
            disabled={isEvaluating}
            className={clsx(
              "flex h-16 w-16 items-center justify-center rounded-full shadow-lg transition-all",
              "bg-rpp-purple hover:bg-purple-700 text-white",
              "disabled:opacity-50 disabled:cursor-not-allowed",
              "hover:scale-105 active:scale-95"
            )}
            title="Comenzar grabación"
          >
            <Mic className="h-7 w-7" />
          </button>
        ) : (
          <button
            onClick={onStop}
            className={clsx(
              "flex h-16 w-16 items-center justify-center rounded-full shadow-lg transition-all",
              "bg-red-500 hover:bg-red-600 text-white",
              "hover:scale-105 active:scale-95"
            )}
            title="Detener grabación"
          >
            <Square className="h-6 w-6 fill-current" />
          </button>
        )}

        {isEvaluating && (
          <div className="flex items-center gap-2 text-gray-500">
            <Loader2 className="h-5 w-5 animate-spin" />
            <span className="text-sm">Evaluando con IA...</span>
          </div>
        )}
      </div>

      {/* Instructions */}
      {recordingState === "idle" && !isEvaluating && (
        <p className="text-center text-sm text-gray-500">
          Presiona el micrófono y lee el texto en voz alta
        </p>
      )}

      {/* Error */}
      {error && (
        <p className="flex items-center gap-1 text-sm text-red-600">
          <MicOff className="h-4 w-4" />
          {error}
        </p>
      )}
    </div>
  );
}
