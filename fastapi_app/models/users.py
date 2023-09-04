import uuid

from models.base import Base
from sqlalchemy import UUID, String
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = 'users'  # noqa

    uuid: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name: Mapped[str] = mapped_column(String(50), nullable=False)
    phone: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
