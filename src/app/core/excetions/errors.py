from typing import Any

from src.app.core.excetions.enums import ErrorCodes


class AppError(Exception):
    status_code: int = 500
    code: ErrorCodes = ErrorCodes.INTERNAL_ERROR
    message: str = "Internal server error"
    details: str | None = None
    headers: dict[str, str] | None = None

    def __init__(
        self,
        message: str | None = None,
        *,
        details: str | None = None,
    ):
        if message is not None:
            self.message = message
        self.details = details

    def to_payload(self) -> dict[str, Any]:
        return {
            "success": False,
            "code": self.code,
            "message": self.message,
            "details": self.details,
        }


class ValidationAppError(AppError):
    status_code = 422
    code = ErrorCodes.INVALID_INPUT
    message = "Validation failed"


class NotFoundAppError(AppError):
    status_code = 404
    code = ErrorCodes.NOT_FOUND
    message = "Resource not found"


class UnauthorizedAppError(AppError):
    status_code = 401
    code = ErrorCodes.UNAUTHORIZED
    message = "Unauthorized"


class ForbiddenAppError(AppError):
    status_code = 403
    code = ErrorCodes.FORBIDDEN
    message = "Forbidden"


class ConflictAppError(AppError):
    status_code = 409
    code = ErrorCodes.CONFLICT
    message = "Conflict"


class DbAppError(AppError):
    status_code = 500
    code = ErrorCodes.DB_ERROR
    message = "Database error"


class DbIntegrityAppError(DbAppError):
    code = ErrorCodes.DB_INTEGRITY_ERROR
    message = "Database integrity error"


class InternalAppError(AppError):
    status_code = 500
    code = ErrorCodes.INTERNAL_ERROR
    message = "Internal server error"
