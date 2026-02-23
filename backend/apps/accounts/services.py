"""
Business logic for user accounts.
Services coordinate repositories and enforce business rules.
"""
import logging

from core.exceptions import BusinessLogicError

from .models import Profile, UserRole
from .repositories import ProfileRepository, UserRepository

logger = logging.getLogger(__name__)

_user_repo = UserRepository()
_profile_repo = ProfileRepository()


class UserService:
    """Handles user registration and profile management."""

    def register(
        self,
        username: str,
        password: str,
        first_name: str,
        last_name: str,
        email: str = "",
        birth_date=None,
        role: str = UserRole.STUDENT,
    ):
        """
        Creates a new user and their profile atomically.
        Raises BusinessLogicError if username or email already exist.
        """
        if _user_repo.exists_by_username(username):
            raise BusinessLogicError(f"El nombre de usuario '{username}' ya está en uso.", code="USERNAME_TAKEN")

        if email and _user_repo.exists_by_email(email):
            raise BusinessLogicError(f"El correo '{email}' ya está registrado.", code="EMAIL_TAKEN")

        user = _user_repo.create(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        # Profile is created by signal; we update it with the extra fields
        profile = _profile_repo.get_by_user(user)
        if profile:
            _profile_repo.update(profile, birth_date=birth_date, role=role)

        logger.info("New user registered: %s (role=%s)", username, role)
        return user

    def update_profile(self, user, birth_date=None, photo=None, first_name=None, last_name=None):
        """Updates mutable profile and user fields."""
        profile = _profile_repo.get_by_user(user)
        if not profile:
            raise BusinessLogicError("Perfil no encontrado.", code="PROFILE_NOT_FOUND")

        updates = {}
        if birth_date is not None:
            updates["birth_date"] = birth_date
        if photo is not None:
            updates["photo"] = photo
        if updates:
            _profile_repo.update(profile, **updates)

        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        user.save(update_fields=["first_name", "last_name"])

        return user

    def get_all_students(self):
        return _user_repo.all_students()
