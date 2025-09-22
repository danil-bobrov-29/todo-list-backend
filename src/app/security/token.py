from datetime import UTC, datetime, timedelta
from typing import Any

from authlib.jose import JoseError, jwt

from src.app.core.excetions.errors import ConflictAppError
from src.app.domain.schemas.token import TokenPayload


class TokenService:
    def __init__(self, security_settings: dict[str, Any]):
        self.security_settings = security_settings

    @staticmethod
    def _exp(minutes: int | None = None, days: int | None = None) -> datetime:
        now = datetime.now(UTC)
        if minutes is not None:
            return now + timedelta(minutes=minutes)
        if days is not None:
            return now + timedelta(days=days)
        return now + timedelta(minutes=15)

    @staticmethod
    def is_token_valid(exp_ts: int, leeway_seconds: int = 0) -> bool:
        now = datetime.now(UTC)
        exp = datetime.fromtimestamp(exp_ts, tz=UTC)
        return now <= (exp + timedelta(seconds=leeway_seconds))

    def create_access_token(
        self,
        sub: str,
        extra: dict[str, Any] | None = None,
    ) -> str:
        payload: dict[str, Any] = {
            "sub": sub,
            "type": "access",
            "exp": int(
                self._exp(minutes=self.security_settings["jwt_access_ttl_min"]).timestamp(),
            ),
        }
        if extra:
            payload.update(extra)
        return jwt.encode(
            {"alg": self.security_settings["jwt_algorithm"]},
            payload,
            self.security_settings["jwt_secret"],
        )

    def create_refresh_token(self, sub: str) -> str:
        payload = {
            "sub": sub,
            "type": "refresh",
            "exp": int(
                self._exp(
                    days=self.security_settings["jwt_refresh_ttl_days"],
                ).timestamp(),
            ),
        }
        return jwt.encode(
            {"alg": self.security_settings["jwt_algorithm"]},
            payload,
            self.security_settings["jwt_secret"],
        ).decode("utf-8")

    def decode_token(self, token: str) -> TokenPayload:
        try:
            return TokenPayload.model_validate(
                jwt.decode(
                    token,
                    self.security_settings["jwt_secret"],
                ),
            )
        except JoseError as error:
            raise ConflictAppError(details="Invalid token") from error
