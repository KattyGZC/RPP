import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";
import { BookOpen } from "lucide-react";
import { useRegister } from "@/hooks/useAuth";
import { Button } from "@/components/ui/Button";
import { RegisterData } from "@/types/auth";

export function RegisterPage() {
  const navigate = useNavigate();
  const registerMutation = useRegister();
  const { register, handleSubmit, watch, setError, formState: { errors } } = useForm<RegisterData>();

  const onSubmit = (data: RegisterData) => {
    registerMutation.mutate(data, {
      onSuccess: () => navigate("/login", { state: { message: "Cuenta creada. Por favor inicia sesión." } }),
      onError: (err: any) => {
        const detail = err?.response?.data?.error?.message ?? "Error al registrar. Intenta de nuevo.";
        setError("root", { message: detail });
      },
    });
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-rpp-purple to-rpp-blue p-4">
      <div className="w-full max-w-md">
        <div className="mb-6 text-center text-white">
          <BookOpen className="mx-auto h-10 w-10 mb-2" />
          <h1 className="text-2xl font-bold">Crear cuenta</h1>
        </div>

        <div className="rounded-2xl bg-white p-8 shadow-2xl">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">Nombre</label>
                <input
                  {...register("first_name", { required: "Requerido" })}
                  className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-rpp-purple focus:outline-none"
                  placeholder="María"
                />
                {errors.first_name && <p className="mt-1 text-xs text-red-500">{errors.first_name.message}</p>}
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">Apellido</label>
                <input
                  {...register("last_name", { required: "Requerido" })}
                  className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-rpp-purple focus:outline-none"
                  placeholder="García"
                />
                {errors.last_name && <p className="mt-1 text-xs text-red-500">{errors.last_name.message}</p>}
              </div>
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">Usuario</label>
              <input
                {...register("username", { required: "El usuario es requerido." })}
                className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-rpp-purple focus:outline-none"
                placeholder="mi_usuario"
              />
              {errors.username && <p className="mt-1 text-xs text-red-500">{errors.username.message}</p>}
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">Correo (opcional)</label>
              <input
                {...register("email")}
                type="email"
                className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-rpp-purple focus:outline-none"
                placeholder="correo@ejemplo.com"
              />
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">Contraseña</label>
              <input
                {...register("password", { required: "Requerido", minLength: { value: 8, message: "Mínimo 8 caracteres" } })}
                type="password"
                className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-rpp-purple focus:outline-none"
                placeholder="••••••••"
              />
              {errors.password && <p className="mt-1 text-xs text-red-500">{errors.password.message}</p>}
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">Confirmar contraseña</label>
              <input
                {...register("password_confirm", {
                  required: "Requerido",
                  validate: (v) => v === watch("password") || "Las contraseñas no coinciden",
                })}
                type="password"
                className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-rpp-purple focus:outline-none"
                placeholder="••••••••"
              />
              {errors.password_confirm && <p className="mt-1 text-xs text-red-500">{errors.password_confirm.message}</p>}
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">Rol</label>
              <select
                {...register("role")}
                className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-rpp-purple focus:outline-none"
              >
                <option value="student">Estudiante</option>
                <option value="teacher">Profesor</option>
              </select>
            </div>

            {errors.root && (
              <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-600">{errors.root.message}</p>
            )}

            <Button type="submit" className="w-full" isLoading={registerMutation.isPending}>
              Crear cuenta
            </Button>
          </form>

          <p className="mt-4 text-center text-sm text-gray-500">
            ¿Ya tienes cuenta?{" "}
            <Link to="/login" className="font-medium text-rpp-purple hover:underline">Inicia sesión</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
