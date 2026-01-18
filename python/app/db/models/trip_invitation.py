from __future__ import annotations

from uuid import uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.db.types import UUIDPk


class TripInvitation(Base):
    __tablename__ = "trip_invitations"
    __table_args__ = (
        Index(
            "trip_invitations_unique_pending",
            "trip_id",
            "email",
            unique=True,
            postgresql_where=text("status = 'pending'"),
        ),
    )

    id: Mapped[str] = mapped_column(UUIDPk, primary_key=True, default=uuid4)
    trip_id: Mapped[str] = mapped_column(ForeignKey("trips.id"), nullable=False)
    inviter_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, index=True)
    role: Mapped[str] = mapped_column(String, nullable=False)
    token: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    status: Mapped[str] = mapped_column(
        Enum("pending", "accepted", "revoked", "expired", name="invitation_status"),
        nullable=False,
        default="pending",
    )
    expires_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    accepted_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    trip: Mapped["Trip"] = relationship("Trip", back_populates="invitations")
    inviter: Mapped["User"] = relationship("User", back_populates="invitations_sent")
