from typing import TYPE_CHECKING
import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.domain.models import Base

if TYPE_CHECKING:
    from src.app.domain.models import User


class Token(Base):
    __tablename__ = "token"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), index=True)
    refresh_token: Mapped[str] = mapped_column(
        String(512),
        unique=True,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="tokens",
    )
