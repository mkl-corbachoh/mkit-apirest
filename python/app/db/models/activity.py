from __future__ import annotations

from uuid import uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.db.types import UUIDPk


class Activity(Base):
    __tablename__ = "activities"
    __table_args__ = (
        CheckConstraint(
            "ends_at IS NULL OR starts_at IS NULL OR ends_at >= starts_at",
            name="activities_time_range_chk",
        ),
        Index("activities_trip_day_id_starts_at_index", "trip_day_id", "starts_at"),
    )

    id: Mapped[str] = mapped_column(UUIDPk, primary_key=True, default=uuid4)
    trip_day_id: Mapped[str] = mapped_column(ForeignKey("trip_days.id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    place: Mapped[str | None] = mapped_column(String, nullable=True)
    starts_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ends_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cost_currency: Mapped[str | None] = mapped_column(String(3), nullable=True)
    cost_amount: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    booking_ref: Mapped[str | None] = mapped_column(String, nullable=True)
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

    day: Mapped["TripDay"] = relationship("TripDay", back_populates="activities")
    attachments: Mapped[list["Attachment"]] = relationship(
        "Attachment",
        primaryjoin="and_(Attachment.attachable_type == 'activity', "
        "Attachment.attachable_id == Activity.id)",
        viewonly=True,
    )
