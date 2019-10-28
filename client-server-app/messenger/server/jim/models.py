"""
Models contains user presentation in database.
"""

from sqlalchemy import (
    Column,
    Boolean,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Index,
    MetaData,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .config import STORAGE


metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(255), index=True, unique=True)
    password = Column(String(256))
    atime = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    is_active = Column(Boolean, default=True)

    history = relationship("UsersHistory")


class UsersHistory(Base):
    __tablename__ = "history"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user = Column(Integer, ForeignKey("users.id"), index=True)
    address = Column(String(42), nullable=False)
    port = Column(Integer, nullable=False)

    ctime = Column(DateTime(timezone=True), default=func.now())


class Contacts(Base):
    __tablename__ = "contacts"

    id = Column(Integer, autoincrement=True, primary_key=True)
    owner = Column(Integer, ForeignKey("users.id"), index=True)
    contact = Column(Integer, ForeignKey("users.id"), index=True)


class Groups(Base):
    __tablename__ = "groups"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255), index=True)


class GroupMembers(Base):
    __tablename__ = "group_members"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user = Column(Integer, ForeignKey("users.id"), index=True)
    group = Column(Integer, ForeignKey("groups.id"), index=True)


class Messages(Base):
    __tablename__ = "messages"
    __table_args__ = (
        Index("destination_user_delivered", "destination_user", "delivered"),
        Index("destination_group_delivered", "destination_group", "delivered"),
    )

    id = Column(Integer, autoincrement=True, primary_key=True)
    author = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(String(4096), default="")
    ctime = Column(DateTime(timezone=True), default=func.now())

    destination_user = Column(Integer, ForeignKey("users.id"), nullable=True)
    destination_group = Column(Integer, ForeignKey("groups.id"), nullable=True)
    delivered = Column(Boolean, default=False)


def create_db():
    engine = create_engine(STORAGE, echo=True)
    Base.metadata.create_all(engine)
