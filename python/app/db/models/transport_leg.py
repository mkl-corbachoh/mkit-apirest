from __future__ import annotations

from uuid import uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.db.types import UUIDPk


class TransportLeg(Base):
    __tablename__ = "transport_legs"
    __table_args__ = (
        Index("transport_legs_trip_day_id_depart_at_index", "trip_day_id", "depart_at"),
    )

    id: Mapped[str] = mapped_column(UUIDPk, primary_key=True, default=uuid4)
    trip_day_id: Mapped[str] = mapped_column(ForeignKey("trip_days.id"), nullable=False)
    kind: Mapped[str] = mapped_column(
        Enum("flight", "train", "bus", "car", "boat", "other", name="transport_kind"),
        nullable=False,
    )
    carrier: Mapped[str | None] = mapped_column(String, nullable=True)
    ref_code: Mapped[str | None] = mapped_column(String, nullable=True)
    depart_place: Mapped[str] = mapped_column(String, nullable=False)
    arrive_place: Mapped[str] = mapped_column(String, nullable=False)
    depart_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    arrive_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
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

    day: Mapped["TripDay"] = relationship("TripDay", back_populates="transport_legs")
    attachments: Mapped[list["Attachment"]] = relationship(
        "Attachment",
        primaryjoin="and_(Attachment.attachable_type == 'transport_leg', "
        "Attachment.attachable_id == TransportLeg.id)",
        viewonly=True,
    )
