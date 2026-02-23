/**
 * Global auth state managed with Zustand.
 * Keeps the authenticated user in memory and syncs tokens to localStorage.
 */
import { create } from "zustand";
import { User } from "@/types/auth";
import { clearTokens, storeTokens } from "@/api/client";

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  setUser: (user: User) => void;
  login: (access: string, refresh: string, user: User) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: !!localStorage.getItem("access_token"),

  setUser: (user) => set({ user, isAuthenticated: true }),

  login: (access, refresh, user) => {
    storeTokens(access, refresh);
    set({ user, isAuthenticated: true });
  },

  logout: () => {
    clearTokens();
    set({ user: null, isAuthenticated: false });
  },
}));
