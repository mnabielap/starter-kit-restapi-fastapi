from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, index=True, nullable=False)
    type = Column(String, nullable=False)  # refresh, resetPassword, verifyEmail
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    expires = Column(DateTime, nullable=False)
    blacklisted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="tokens")