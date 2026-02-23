import { Routes, Route, Navigate } from "react-router-dom";
import { Layout } from "@/components/layout/Layout";
import { ProtectedRoute } from "@/components/layout/ProtectedRoute";
import { LoginPage } from "@/pages/LoginPage";
import { RegisterPage } from "@/pages/RegisterPage";
import { DashboardPage } from "@/pages/DashboardPage";
import { LevelsPage } from "@/pages/LevelsPage";
import { ExercisePage } from "@/pages/ExercisePage";
import { ProfilePage } from "@/pages/ProfilePage";
import { TeacherDashboard } from "@/pages/teacher/TeacherDashboard";
import { ExerciseManager } from "@/pages/teacher/ExerciseManager";

export default function App() {
  return (
    <Routes>
      {/* Public routes */}
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      {/* Protected routes */}
      <Route element={<ProtectedRoute />}>
        <Route element={<Layout />}>
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/levels" element={<LevelsPage />} />
          <Route path="/exercise/:levelSlug" element={<ExercisePage />} />
          <Route path="/profile" element={<ProfilePage />} />

          {/* Teacher-only routes */}
          <Route element={<ProtectedRoute requireRole="teacher" />}>
            <Route path="/teacher" element={<TeacherDashboard />} />
            <Route path="/teacher/exercises" element={<ExerciseManager />} />
          </Route>
        </Route>
      </Route>

      {/* Default redirect */}
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}
