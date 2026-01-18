from __future__ import annotations

from uuid import uuid4

from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.db.types import UUIDPk


class Trip(Base):
    __tablename__ = "trips"
    __table_args__ = (
        CheckConstraint("end_date >= start_date", name="trips_dates_chk"),
    )

    id: Mapped[str] = mapped_column(UUIDPk, primary_key=True, default=uuid4)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)
    timezone: Mapped[str] = mapped_column(String, nullable=False, default="UTC")
    created_at: Mapped[DateTime | None] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime | None] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )

    owner: Mapped["User"] = relationship("User", back_populates="owned_trips")
    members: Mapped[list["User"]] = relationship(
        "User",
        secondary="trip_members",
        back_populates="member_trips",
    )
    days: Mapped[list["TripDay"]] = relationship(
        "TripDay",
        back_populates="trip",
        order_by="TripDay.day_number",
        cascade="all, delete-orphan",
    )
    invitations: Mapped[list["TripInvitation"]] = relationship(
        "TripInvitation",
        back_populates="trip",
        cascade="all, delete-orphan",
    )
