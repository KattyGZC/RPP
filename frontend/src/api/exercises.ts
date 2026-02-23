import { Exercise, Level, UserProgress, ReadingSession } from "@/types/exercise";
import { ApiResponse, apiClient } from "./client";

export const exercisesApi = {
  getLevels: async (): Promise<Level[]> => {
    const { data } = await apiClient.get<ApiResponse<Level[]>>("/exercises/levels/");
    return data.data;
  },

  getExercises: async (levelSlug: string): Promise<Exercise[]> => {
    const { data } = await apiClient.get<ApiResponse<Exercise[]>>(`/exercises/?level=${levelSlug}`);
    return data.data;
  },

  createExercise: async (payload: {
    level_id: number;
    title: string;
    text: string;
    max_score?: number;
    order?: number;
  }): Promise<Exercise> => {
    const { data } = await apiClient.post<ApiResponse<Exercise>>("/exercises/", payload);
    return data.data;
  },

  updateExercise: async (id: number, payload: Partial<Exercise>): Promise<Exercise> => {
    const { data } = await apiClient.patch<ApiResponse<Exercise>>(`/exercises/${id}/`, payload);
    return data.data;
  },

  deleteExercise: async (id: number): Promise<void> => {
    await apiClient.delete(`/exercises/${id}/`);
  },

  getMyProgress: async (): Promise<UserProgress> => {
    const { data } = await apiClient.get<ApiResponse<UserProgress>>("/exercises/progress/");
    return data.data;
  },

  getStudentProgress: async (userId: number): Promise<UserProgress & { student: { id: number; username: string; full_name: string } }> => {
    const { data } = await apiClient.get<ApiResponse<UserProgress & { student: { id: number; username: string; full_name: string } }>>(`/exercises/progress/${userId}/`);
    return data.data;
  },
};
