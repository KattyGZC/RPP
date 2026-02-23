import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { authApi } from "@/api/auth";
import { useAuthStore } from "@/store/authStore";
import { LoginCredentials, RegisterData, UpdateProfileData } from "@/types/auth";

export function useCurrentUser() {
  const { isAuthenticated, setUser } = useAuthStore();
  return useQuery({
    queryKey: ["me"],
    queryFn: async () => {
      const user = await authApi.getMe();
      setUser(user);
      return user;
    },
    enabled: isAuthenticated,
    staleTime: 5 * 60 * 1000,
  });
}

export function useLogin() {
  const { login } = useAuthStore();
  return useMutation({
    mutationFn: (credentials: LoginCredentials) => authApi.login(credentials),
    onSuccess: (data) => login(data.access, data.refresh, data.user),
  });
}

export function useLogout() {
  const { logout } = useAuthStore();
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: () => {
      const refresh = localStorage.getItem("refresh_token") ?? "";
      return authApi.logout(refresh);
    },
    onSettled: () => {
      logout();
      queryClient.clear();
    },
  });
}

export function useRegister() {
  return useMutation({
    mutationFn: (data: RegisterData) => authApi.register(data),
  });
}

export function useUpdateProfile() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: UpdateProfileData) => authApi.updateProfile(data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["me"] }),
  });
}
