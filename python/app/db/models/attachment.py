from __future__ import annotations

from uuid import uuid4

from sqlalchemy import BigInteger, DateTime, ForeignKey, Index, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.db.types import UUIDPk


class Attachment(Base):
    __tablename__ = "attachments"
    __table_args__ = (
        Index("attachments_trip_attachable_index", "trip_id", "attachable_type", "attachable_id"),
    )

    id: Mapped[str] = mapped_column(UUIDPk, primary_key=True, default=uuid4)
    attachable_type: Mapped[str] = mapped_column(String, nullable=False)
    attachable_id: Mapped[str] = mapped_column(UUIDPk, nullable=False)
    trip_id: Mapped[str] = mapped_column(ForeignKey("trips.id"), nullable=False)
    trip_day_id: Mapped[str | None] = mapped_column(ForeignKey("trip_days.id"), nullable=True)
    uploader_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    disk: Mapped[str] = mapped_column(String(32), nullable=False)
    path: Mapped[str] = mapped_column(String, nullable=False)
    original_name: Mapped[str] = mapped_column(String, nullable=False)
    mime: Mapped[str | None] = mapped_column(String(127), nullable=True)
    size: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
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
    day: Mapped["TripDay"] = relationship("TripDay")
    uploader: Mapped["User"] = relationship("User", back_populates="attachments")
