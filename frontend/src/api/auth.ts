import { User, LoginCredentials, RegisterData, UpdateProfileData } from "@/types/auth";
import { ApiResponse, apiClient } from "./client";

export const authApi = {
  login: async (credentials: LoginCredentials) => {
    const { data } = await apiClient.post<{ access: string; refresh: string; user: User }>(
      "/auth/login/",
      credentials
    );
    return data;
  },

  logout: async (refreshToken: string) => {
    await apiClient.post("/auth/logout/", { refresh: refreshToken });
  },

  register: async (registerData: RegisterData) => {
    const { data } = await apiClient.post<ApiResponse<User>>("/accounts/register/", registerData);
    return data.data;
  },

  getMe: async () => {
    const { data } = await apiClient.get<ApiResponse<User>>("/accounts/me/");
    return data.data;
  },

  updateProfile: async (profileData: UpdateProfileData) => {
    const formData = new FormData();
    Object.entries(profileData).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        formData.append(key, value instanceof File ? value : String(value));
      }
    });
    const { data } = await apiClient.patch<ApiResponse<User>>("/accounts/me/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return data.data;
  },

  getStudents: async () => {
    const { data } = await apiClient.get<ApiResponse<User[]>>("/accounts/students/");
    return data.data;
  },
};
