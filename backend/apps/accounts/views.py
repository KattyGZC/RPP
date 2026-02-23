import logging

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from core.exceptions import BusinessLogicError
from core.permissions import IsTeacherOrAdmin
from core.responses import created_response, error_response, success_response

from .serializers import (
    RegisterSerializer,
    StudentListSerializer,
    UpdateProfileSerializer,
    UserSerializer,
)
from .services import UserService

logger = logging.getLogger(__name__)
_user_service = UserService()


class LoginView(TokenObtainPairView):
    """
    Extends SimpleJWT's login to return user data alongside the tokens.
    POST /api/auth/login/
    """

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            from django.contrib.auth.models import User
            from .serializers import UserSerializer as US
            username = request.data.get("username")
            user = User.objects.filter(username=username).select_related("profile").first()
            response.data["user"] = US(user).data
        return response


class LogoutView(APIView):
    """
    Blacklists the refresh token on logout.
    POST /api/auth/logout/
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return success_response(message="Sesión cerrada correctamente.")
        except Exception:
            return error_response("Token inválido o expirado.", code="INVALID_TOKEN")


class RegisterView(APIView):
    """
    Registers a new user.
    POST /api/accounts/register/
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                "Datos de registro inválidos.",
                code="VALIDATION_ERROR",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        data = serializer.validated_data
        try:
            user = _user_service.register(
                username=data["username"],
                password=data["password"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data.get("email", ""),
                birth_date=data.get("birth_date"),
                role=data.get("role", "student"),
            )
            return created_response(
                data=UserSerializer(user).data,
                message="Usuario registrado exitosamente.",
            )
        except BusinessLogicError as e:
            return error_response(e.message, code=e.code)


class MeView(APIView):
    """
    Returns the authenticated user's full profile.
    GET  /api/accounts/me/
    PATCH /api/accounts/me/
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return success_response(data=UserSerializer(request.user).data)

    def patch(self, request):
        serializer = UpdateProfileSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response("Datos inválidos.", code="VALIDATION_ERROR")

        try:
            user = _user_service.update_profile(request.user, **serializer.validated_data)
            return success_response(
                data=UserSerializer(user).data,
                message="Perfil actualizado.",
            )
        except BusinessLogicError as e:
            return error_response(e.message, code=e.code)


class StudentListView(APIView):
    """
    Returns list of all students. Only accessible by teachers/admins.
    GET /api/accounts/students/
    """

    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    def get(self, request):
        students = _user_service.get_all_students()
        return success_response(data=StudentListSerializer(students, many=True).data)
