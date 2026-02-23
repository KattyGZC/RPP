import { ApiResponse, apiClient } from "./client";
import { SessionFeedback } from "@/types/exercise";

export interface EvaluationResult {
  session_id: number;
  score: number;
  accuracy: number;
  transcription: string;
  confidence: number;
  duration_seconds: number;
  feedback: SessionFeedback;
}

export const evaluationApi = {
  evaluate: async (
    audioBlob: Blob,
    exerciseId: number,
    durationSeconds: number
  ): Promise<EvaluationResult> => {
    const formData = new FormData();
    formData.append("audio", audioBlob, "recording.webm");
    formData.append("exercise_id", String(exerciseId));
    formData.append("duration_seconds", String(durationSeconds));

    const { data } = await apiClient.post<ApiResponse<EvaluationResult>>(
      "/evaluation/evaluate/",
      formData,
      { headers: { "Content-Type": "multipart/form-data" }, timeout: 120_000 }
    );
    return data.data;
  },
};
