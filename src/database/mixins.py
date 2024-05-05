from datetime import datetime
from typing import Optional

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        onupdate=datetime.utcnow,
        nullable=True,
    )
