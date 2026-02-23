import { Navigate, Outlet } from "react-router-dom";
import { useAuthStore } from "@/store/authStore";
import { useCurrentUser } from "@/hooks/useAuth";

interface ProtectedRouteProps {
  requireRole?: "teacher" | "student" | "admin";
}

export function ProtectedRoute({ requireRole }: ProtectedRouteProps) {
  const { isAuthenticated, user } = useAuthStore();
  const { isLoading } = useCurrentUser();

  if (!isAuthenticated) return <Navigate to="/login" replace />;
  if (isLoading) return <div className="flex h-screen items-center justify-center">Cargando...</div>;
  if (requireRole && user?.profile.role !== requireRole && user?.profile.role !== "admin") {
    return <Navigate to="/dashboard" replace />;
  }

  return <Outlet />;
}
