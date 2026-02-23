import logging

from django.contrib.auth.models import User
from django.db import models

logger = logging.getLogger(__name__)


class UserRole(models.TextChoices):
    STUDENT = "student", "Estudiante"
    TEACHER = "teacher", "Profesor"
    ADMIN = "admin", "Administrador"


class Profile(models.Model):
    """
    Extends Django's built-in User with domain-specific attributes.
    Uses a OneToOne relation to keep auth concerns separate from profile concerns.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.STUDENT)
    birth_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to="profiles/", default="defaults/profile.png", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"

    @property
    def is_teacher(self) -> bool:
        return self.role in (UserRole.TEACHER, UserRole.ADMIN)

    @property
    def is_student(self) -> bool:
        return self.role == UserRole.STUDENT
