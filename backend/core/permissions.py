from rest_framework.permissions import BasePermission


class IsTeacherOrAdmin(BasePermission):
    """Grants access only to users with teacher or admin role."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return hasattr(request.user, "profile") and request.user.profile.role in (
            "teacher",
            "admin",
        )


class IsStudent(BasePermission):
    """Grants access only to users with student role."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return hasattr(request.user, "profile") and request.user.profile.role == "student"


class IsOwnerOrTeacher(BasePermission):
    """Grants access if the user owns the object or is a teacher/admin."""

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.user.profile.role in ("teacher", "admin"):
            return True
        owner = getattr(obj, "user", None)
        return owner == request.user
