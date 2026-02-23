import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { BookOpen, ChevronDown, GraduationCap, LogOut, User } from "lucide-react";
import { useAuthStore } from "@/store/authStore";
import { useLogout } from "@/hooks/useAuth";

export function Navbar() {
  const { user } = useAuthStore();
  const navigate = useNavigate();
  const logoutMutation = useLogout();
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const handleLogout = () => {
    logoutMutation.mutate(undefined, { onSuccess: () => navigate("/login") });
  };

  return (
    <header className="sticky top-0 z-50 border-b border-gray-200 bg-white shadow-sm">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">
        {/* Logo */}
        <Link to="/dashboard" className="flex items-center gap-2 text-rpp-purple font-bold text-xl">
          <BookOpen className="h-6 w-6" />
          Read Praxis
        </Link>

        {/* Nav links */}
        <div className="hidden items-center gap-6 md:flex">
          <Link to="/dashboard" className="text-sm font-medium text-gray-600 hover:text-rpp-purple transition-colors">
            Inicio
          </Link>
          <Link to="/levels" className="text-sm font-medium text-gray-600 hover:text-rpp-purple transition-colors">
            Ejercicios
          </Link>
          {user?.profile.role === "teacher" && (
            <Link to="/teacher" className="flex items-center gap-1 text-sm font-medium text-gray-600 hover:text-rpp-purple transition-colors">
              <GraduationCap className="h-4 w-4" />
              Panel Docente
            </Link>
          )}
        </div>

        {/* User menu */}
        <div className="relative">
          <button
            onClick={() => setDropdownOpen((o) => !o)}
            className="flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 transition-colors"
          >
            {user?.profile.photo ? (
              <img src={user.profile.photo} alt="" className="h-7 w-7 rounded-full object-cover" />
            ) : (
              <div className="flex h-7 w-7 items-center justify-center rounded-full bg-rpp-purple text-white text-xs font-bold">
                {user?.first_name?.[0]?.toUpperCase() ?? "U"}
              </div>
            )}
            <span className="max-w-32 truncate">{user?.first_name || user?.username}</span>
            <ChevronDown className="h-4 w-4 text-gray-400" />
          </button>

          {dropdownOpen && (
            <div
              className="absolute right-0 mt-2 w-48 rounded-lg border border-gray-200 bg-white py-1 shadow-lg"
              onBlur={() => setDropdownOpen(false)}
            >
              <Link
                to="/profile"
                onClick={() => setDropdownOpen(false)}
                className="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
              >
                <User className="h-4 w-4" /> Mi perfil
              </Link>
              <hr className="my-1 border-gray-100" />
              <button
                onClick={handleLogout}
                className="flex w-full items-center gap-2 px-4 py-2 text-sm text-red-600 hover:bg-red-50"
              >
                <LogOut className="h-4 w-4" /> Cerrar sesión
              </button>
            </div>
          )}
        </div>
      </nav>
    </header>
  );
}
