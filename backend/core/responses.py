from rest_framework import status
from rest_framework.response import Response


def success_response(data=None, message: str = "OK", status_code: int = status.HTTP_200_OK) -> Response:
    """Standard success envelope: { success: true, message: "...", data: {...} }"""
    return Response({"success": True, "message": message, "data": data}, status=status_code)


def created_response(data=None, message: str = "Created") -> Response:
    return success_response(data, message, status.HTTP_201_CREATED)


def no_content_response() -> Response:
    return Response(status=status.HTTP_204_NO_CONTENT)


def error_response(message: str, code: str = "ERROR", status_code: int = status.HTTP_400_BAD_REQUEST) -> Response:
    """Standard error envelope: { success: false, error: { code: "...", message: "..." } }"""
    return Response(
        {"success": False, "error": {"code": code, "message": message}},
        status=status_code,
    )
