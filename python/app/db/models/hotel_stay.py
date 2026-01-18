from __future__ import annotations

from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.db.types import UUIDPk


class HotelStay(Base):
    __tablename__ = "hotel_stays"
    __table_args__ = (
        Index("hotel_stays_trip_day_id_index", "trip_day_id"),
    )

    id: Mapped[str] = mapped_column(UUIDPk, primary_key=True, default=uuid4)
    trip_day_id: Mapped[str] = mapped_column(ForeignKey("trip_days.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    checkin_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    checkout_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
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

    day: Mapped["TripDay"] = relationship("TripDay", back_populates="hotel_stays")
    attachments: Mapped[list["Attachment"]] = relationship(
        "Attachment",
        primaryjoin="and_(Attachment.attachable_type == 'hotel_stay', "
        "Attachment.attachable_id == HotelStay.id)",
        viewonly=True,
    )
