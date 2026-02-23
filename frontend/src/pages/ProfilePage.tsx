import { useRef } from "react";
import { useForm } from "react-hook-form";
import { Camera, User } from "lucide-react";
import { useCurrentUser, useUpdateProfile } from "@/hooks/useAuth";
import { Button } from "@/components/ui/Button";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { UpdateProfileData } from "@/types/auth";

export function ProfilePage() {
  const { data: user } = useCurrentUser();
  const updateMutation = useUpdateProfile();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { register, handleSubmit, formState: { errors, isDirty } } = useForm<UpdateProfileData>({
    defaultValues: {
      first_name: user?.first_name ?? "",
      last_name: user?.last_name ?? "",
      birth_date: user?.profile.birth_date ?? "",
    },
  });

  const onSubmit = (data: UpdateProfileData) => {
    updateMutation.mutate(data);
  };

  const handlePhotoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) updateMutation.mutate({ photo: file });
  };

  const roleLabel: Record<string, string> = {
    student: "Estudiante",
    teacher: "Profesor",
    admin: "Administrador",
  };

  return (
    <div className="mx-auto max-w-lg space-y-6 animate-fade-in">
      <h1 className="text-2xl font-bold text-gray-900">Mi Perfil</h1>

      {/* Photo */}
      <Card className="flex flex-col items-center gap-4 py-8">
        <div className="relative">
          {user?.profile.photo ? (
            <img src={user.profile.photo} alt="Foto de perfil" className="h-24 w-24 rounded-full object-cover" />
          ) : (
            <div className="flex h-24 w-24 items-center justify-center rounded-full bg-rpp-light">
              <User className="h-12 w-12 text-rpp-purple" />
            </div>
          )}
          <button
            onClick={() => fileInputRef.current?.click()}
            className="absolute bottom-0 right-0 rounded-full bg-rpp-purple p-1.5 text-white shadow-md hover:bg-purple-700 transition-colors"
          >
            <Camera className="h-3.5 w-3.5" />
          </button>
          <input ref={fileInputRef} type="file" accept="image/*" className="hidden" onChange={handlePhotoChange} />
        </div>
        <div className="text-center">
          <p className="font-semibold text-gray-900">{user?.full_name}</p>
          <p className="text-sm text-gray-400">@{user?.username}</p>
          <Badge variant="info" className="mt-1">
            {roleLabel[user?.profile.role ?? "student"] ?? user?.profile.role}
          </Badge>
        </div>
      </Card>

      {/* Edit form */}
      <Card>
        <CardHeader>
          <CardTitle>Editar información</CardTitle>
        </CardHeader>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">Nombre</label>
              <input
                {...register("first_name")}
                className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-rpp-purple focus:outline-none"
              />
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">Apellido</label>
              <input
                {...register("last_name")}
                className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-rpp-purple focus:outline-none"
              />
            </div>
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Fecha de nacimiento</label>
            <input
              {...register("birth_date")}
              type="date"
              className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-rpp-purple focus:outline-none"
            />
          </div>

          <Button
            type="submit"
            isLoading={updateMutation.isPending}
            disabled={!isDirty}
            className="w-full"
          >
            Guardar cambios
          </Button>

          {updateMutation.isSuccess && (
            <p className="text-center text-sm text-green-600">✓ Perfil actualizado correctamente</p>
          )}
        </form>
      </Card>
    </div>
  );
}
