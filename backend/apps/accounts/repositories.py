"""
Repository layer for accounts.
Encapsulates all database access, keeping views and services free of ORM details.
"""
import logging
from typing import Optional

from django.contrib.auth.models import User
from django.db.models import QuerySet

from .models import Profile

logger = logging.getLogger(__name__)


class UserRepository:
    """Data access operations for the User model."""

    def get_by_id(self, user_id: int) -> Optional[User]:
        return User.objects.filter(id=user_id).first()

    def get_by_username(self, username: str) -> Optional[User]:
        return User.objects.filter(username=username).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return User.objects.filter(email=email).first()

    def exists_by_username(self, username: str) -> bool:
        return User.objects.filter(username=username).exists()

    def exists_by_email(self, email: str) -> bool:
        return User.objects.filter(email=email).exists()

    def create(self, username: str, password: str, first_name: str, last_name: str, email: str = "") -> User:
        return User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

    def all_students(self) -> QuerySet:
        return User.objects.filter(profile__role="student").select_related("profile")


class ProfileRepository:
    """Data access operations for the Profile model."""

    def get_by_user(self, user: User) -> Optional[Profile]:
        return Profile.objects.filter(user=user).first()

    def update(self, profile: Profile, **kwargs) -> Profile:
        for field, value in kwargs.items():
            setattr(profile, field, value)
        profile.save(update_fields=list(kwargs.keys()) + ["updated_at"])
        return profile
