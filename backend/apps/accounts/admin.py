from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Perfil"
    fields = ["role", "birth_date", "photo"]


class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]
    list_display = ["username", "get_full_name", "email", "get_role", "is_active", "date_joined"]
    list_filter = ["is_active", "profile__role"]

    @admin.display(description="Nombre completo")
    def get_full_name(self, obj):
        return obj.get_full_name() or "—"

    @admin.display(description="Rol")
    def get_role(self, obj):
        return obj.profile.get_role_display() if hasattr(obj, "profile") else "—"


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
