/**
 * Custom hook for audio recording via the MediaRecorder API.
 * Replaces the old browser-specific webkitSpeechRecognition approach.
 * The recorded audio is sent to the backend where Whisper handles transcription.
 */
import { useRef, useState, useCallback } from "react";

export type RecordingState = "idle" | "recording" | "stopped";

interface UseMediaRecorderReturn {
  recordingState: RecordingState;
  elapsedSeconds: number;
  startRecording: () => Promise<void>;
  stopRecording: () => Promise<Blob | null>;
  error: string | null;
}

export function useMediaRecorder(): UseMediaRecorderReturn {
  const [recordingState, setRecordingState] = useState<RecordingState>("idle");
  const [elapsedSeconds, setElapsedSeconds] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const resolveStopRef = useRef<((blob: Blob | null) => void) | null>(null);

  const startRecording = useCallback(async () => {
    setError(null);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream, { mimeType: "audio/webm;codecs=opus" });

      chunksRef.current = [];
      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data);
      };

      recorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: "audio/webm" });
        stream.getTracks().forEach((t) => t.stop());
        resolveStopRef.current?.(blob);
        resolveStopRef.current = null;
      };

      mediaRecorderRef.current = recorder;
      recorder.start(250);
      setRecordingState("recording");
      setElapsedSeconds(0);

      timerRef.current = setInterval(() => setElapsedSeconds((s) => s + 1), 1000);
    } catch (err) {
      setError("No se pudo acceder al micrófono. Verifica los permisos del navegador.");
      setRecordingState("idle");
    }
  }, []);

  const stopRecording = useCallback((): Promise<Blob | null> => {
    return new Promise((resolve) => {
      if (timerRef.current) clearInterval(timerRef.current);

      if (!mediaRecorderRef.current || mediaRecorderRef.current.state === "inactive") {
        resolve(null);
        return;
      }

      resolveStopRef.current = resolve;
      mediaRecorderRef.current.stop();
      setRecordingState("stopped");
    });
  }, []);

  return { recordingState, elapsedSeconds, startRecording, stopRecording, error };
}
