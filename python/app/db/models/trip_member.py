from __future__ import annotations

from sqlalchemy import DateTime, Enum, ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class TripMember(Base):
    __tablename__ = "trip_members"
    __table_args__ = (
        Index("trip_members_user_id_index", "user_id"),
    )

    trip_id: Mapped[str] = mapped_column(
        ForeignKey("trips.id"),
        primary_key=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )
    role: Mapped[str] = mapped_column(
        Enum("reader", "editor", "admin", name="trip_member_role"),
        nullable=False,
    )
    added_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    created_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    trip: Mapped["Trip"] = relationship("Trip")
    user: Mapped["User"] = relationship("User")
