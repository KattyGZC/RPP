import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";
import { BookOpen } from "lucide-react";
import { useLogin } from "@/hooks/useAuth";
import { useAuthStore } from "@/store/authStore";
import { Button } from "@/components/ui/Button";
import { LoginCredentials } from "@/types/auth";

export function LoginPage() {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuthStore();
  const loginMutation = useLogin();

  const {
    register,
    handleSubmit,
    formState: { errors },
    setError,
  } = useForm<LoginCredentials>();

  useEffect(() => {
    if (isAuthenticated) navigate("/dashboard", { replace: true });
  }, [isAuthenticated, navigate]);

  const onSubmit = (data: LoginCredentials) => {
    loginMutation.mutate(data, {
      onSuccess: () => navigate("/dashboard"),
      onError: () => setError("root", { message: "Usuario o contraseña incorrectos." }),
    });
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-rpp-purple to-rpp-blue p-4">
      <div className="w-full max-w-sm">
        {/* Logo */}
        <div className="mb-8 text-center text-white">
          <div className="mx-auto mb-3 flex h-14 w-14 items-center justify-center rounded-2xl bg-white/20 backdrop-blur-sm">
            <BookOpen className="h-7 w-7" />
          </div>
          <h1 className="text-2xl font-bold">Read Praxis</h1>
          <p className="mt-1 text-sm text-white/70">Plataforma de lectura con IA</p>
        </div>

        {/* Form card */}
        <div className="rounded-2xl bg-white p-8 shadow-2xl">
          <h2 className="mb-6 text-xl font-bold text-gray-900">Iniciar sesión</h2>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div>
              <label className="mb-1.5 block text-sm font-medium text-gray-700">Usuario</label>
              <input
                {...register("username", { required: "El usuario es requerido." })}
                className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-rpp-purple focus:outline-none focus:ring-2 focus:ring-rpp-purple/20"
                placeholder="tu_usuario"
                autoComplete="username"
              />
              {errors.username && <p className="mt-1 text-xs text-red-500">{errors.username.message}</p>}
            </div>

            <div>
              <label className="mb-1.5 block text-sm font-medium text-gray-700">Contraseña</label>
              <input
                {...register("password", { required: "La contraseña es requerida." })}
                type="password"
                className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-rpp-purple focus:outline-none focus:ring-2 focus:ring-rpp-purple/20"
                placeholder="••••••••"
                autoComplete="current-password"
              />
              {errors.password && <p className="mt-1 text-xs text-red-500">{errors.password.message}</p>}
            </div>

            {errors.root && (
              <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-600">{errors.root.message}</p>
            )}

            <Button type="submit" className="w-full" isLoading={loginMutation.isPending}>
              Ingresar
            </Button>
          </form>

          <p className="mt-4 text-center text-sm text-gray-500">
            ¿No tienes cuenta?{" "}
            <Link to="/register" className="font-medium text-rpp-purple hover:underline">
              Regístrate
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
