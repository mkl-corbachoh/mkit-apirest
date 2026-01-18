from __future__ import annotations

from uuid import uuid4

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.db.types import UUIDPk


class TripDay(Base):
    __tablename__ = "trip_days"
    __table_args__ = (
        UniqueConstraint("trip_id", "day_number", name="trip_days_trip_id_day_number_unique"),
        UniqueConstraint("trip_id", "date", name="trip_days_trip_id_date_unique"),
    )

    id: Mapped[str] = mapped_column(UUIDPk, primary_key=True, default=uuid4)
    trip_id: Mapped[str] = mapped_column(ForeignKey("trips.id"), nullable=False)
    day_number: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[DateTime | None] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime | None] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )

    trip: Mapped["Trip"] = relationship("Trip", back_populates="days")
    activities: Mapped[list["Activity"]] = relationship(
        "Activity",
        back_populates="day",
        order_by="Activity.starts_at",
        cascade="all, delete-orphan",
    )
    transport_legs: Mapped[list["TransportLeg"]] = relationship(
        "TransportLeg",
        back_populates="day",
        order_by="TransportLeg.depart_at",
        cascade="all, delete-orphan",
    )
    hotel_stays: Mapped[list["HotelStay"]] = relationship(
        "HotelStay",
        back_populates="day",
        order_by="HotelStay.checkin_at",
        cascade="all, delete-orphan",
    )
