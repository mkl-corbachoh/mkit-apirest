from __future__ import annotations

from sqlalchemy import BigInteger, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    email_verified_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    id_telegram: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    remember_token: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[DateTime | None] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime | None] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )

    owned_trips: Mapped[list["Trip"]] = relationship("Trip", back_populates="owner")
    member_trips: Mapped[list["Trip"]] = relationship(
        "Trip",
        secondary="trip_members",
        back_populates="members",
    )
    invitations_sent: Mapped[list["TripInvitation"]] = relationship(
        "TripInvitation",
        back_populates="inviter",
    )
    attachments: Mapped[list["Attachment"]] = relationship(
        "Attachment",
        back_populates="uploader",
    )
