from sqlalchemy.schema import Column
from sqlalchemy.types import String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
import uuid
from core.config.database import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    token_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    token = Column(String, nullable=True)
    expired_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
    deleted_at = Column(TIMESTAMP, nullable=True)
