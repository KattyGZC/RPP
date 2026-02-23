"""
Custom exceptions and DRF exception handler.
Ensures consistent error response format across the entire API.
"""
import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Wraps DRF's default handler to produce a consistent error envelope:
    {
        "success": false,
        "error": { "code": "...", "message": "...", "details": {...} }
    }
    """
    response = exception_handler(exc, context)

    if response is not None:
        error_data = {
            "success": False,
            "error": {
                "code": _get_error_code(response.status_code),
                "message": _extract_message(response.data),
                "details": response.data if isinstance(response.data, dict) else {},
            },
        }
        response.data = error_data

    return response


def _get_error_code(status_code: int) -> str:
    codes = {
        400: "VALIDATION_ERROR",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        405: "METHOD_NOT_ALLOWED",
        409: "CONFLICT",
        429: "RATE_LIMIT_EXCEEDED",
        500: "INTERNAL_SERVER_ERROR",
    }
    return codes.get(status_code, "UNKNOWN_ERROR")


def _extract_message(data) -> str:
    if isinstance(data, dict):
        if "detail" in data:
            return str(data["detail"])
        first_key = next(iter(data), None)
        if first_key:
            value = data[first_key]
            return str(value[0] if isinstance(value, list) else value)
    if isinstance(data, list) and data:
        return str(data[0])
    return str(data)


class BusinessLogicError(Exception):
    """Raised when a business rule is violated."""

    def __init__(self, message: str, code: str = "BUSINESS_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)


class ResourceNotFoundError(Exception):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str, identifier=None):
        self.resource = resource
        self.identifier = identifier
        message = f"{resource} not found"
        if identifier:
            message += f" with id={identifier}"
        super().__init__(message)
