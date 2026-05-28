from sqlalchemy import Column, Integer, String,Boolean

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), unique=True, nullable=False, index=True)

    email = Column(String(100), unique=True, nullable=False, index=True)

    password = Column(String(100), nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)