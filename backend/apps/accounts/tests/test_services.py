from django.test import TestCase

from apps.accounts.models import UserRole
from apps.accounts.services import UserService
from core.exceptions import BusinessLogicError


class UserServiceRegisterTests(TestCase):
    def setUp(self):
        self.service = UserService()
        self.valid_data = {
            "username": "testuser",
            "password": "securepassword123",
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
        }

    def test_register_creates_user_and_profile(self):
        user = self.service.register(**self.valid_data)

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.first_name, "Test")
        self.assertTrue(hasattr(user, "profile"))
        self.assertEqual(user.profile.role, UserRole.STUDENT)

    def test_register_raises_if_username_taken(self):
        self.service.register(**self.valid_data)

        with self.assertRaises(BusinessLogicError) as ctx:
            self.service.register(**self.valid_data)

        self.assertEqual(ctx.exception.code, "USERNAME_TAKEN")

    def test_register_raises_if_email_taken(self):
        self.service.register(**self.valid_data)
        duplicate = {**self.valid_data, "username": "otheruser"}

        with self.assertRaises(BusinessLogicError) as ctx:
            self.service.register(**duplicate)

        self.assertEqual(ctx.exception.code, "EMAIL_TAKEN")

    def test_register_teacher_role(self):
        user = self.service.register(**self.valid_data, role=UserRole.TEACHER)
        self.assertEqual(user.profile.role, UserRole.TEACHER)
        self.assertTrue(user.profile.is_teacher)

    def test_register_student_is_not_teacher(self):
        user = self.service.register(**self.valid_data, role=UserRole.STUDENT)
        self.assertFalse(user.profile.is_teacher)
        self.assertTrue(user.profile.is_student)
