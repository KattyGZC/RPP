import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { exercisesApi } from "@/api/exercises";

export function useLevels() {
  return useQuery({
    queryKey: ["levels"],
    queryFn: exercisesApi.getLevels,
    staleTime: 10 * 60 * 1000,
  });
}

export function useExercises(levelSlug: string | null) {
  return useQuery({
    queryKey: ["exercises", levelSlug],
    queryFn: () => exercisesApi.getExercises(levelSlug!),
    enabled: !!levelSlug,
  });
}

export function useMyProgress() {
  return useQuery({
    queryKey: ["my-progress"],
    queryFn: exercisesApi.getMyProgress,
    staleTime: 2 * 60 * 1000,
  });
}

export function useStudentProgress(userId: number | null) {
  return useQuery({
    queryKey: ["student-progress", userId],
    queryFn: () => exercisesApi.getStudentProgress(userId!),
    enabled: !!userId,
  });
}

export function useCreateExercise() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: exercisesApi.createExercise,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["exercises"] }),
  });
}

export function useDeleteExercise() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: exercisesApi.deleteExercise,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["exercises"] }),
  });
}
