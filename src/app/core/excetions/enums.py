import enum


class ErrorCodes(str, enum.Enum):
    API_ERROR = "api_error"
    INVALID_INPUT = "invalid_input"
    NOT_FOUND = "not_found"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    CONFLICT = "conflict"
    DB_ERROR = "db_error"
    DB_INTEGRITY_ERROR = "db_integrity_error"
    HTTP_ERROR = "http_error"
    INTERNAL_ERROR = "internal_error"
