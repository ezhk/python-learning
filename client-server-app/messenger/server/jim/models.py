"""
Models contains user presentation in database.
"""

from datetime import datetime

from mongoengine import (
    Document,
    StringField,
    BinaryField,
    DateTimeField,
    BooleanField,
    ReferenceField,
    IntField,
    CASCADE,
)

# from sqlalchemy import (
#     Column,
#     Boolean,
#     Integer,
#     String,
#     DateTime,
#     BLOB,
#     ForeignKey,
#     Index,
#     MetaData,
#     create_engine,
# )
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func

# from .config import STORAGE

##########################
# SQLAlchemy class logic #
##########################

# metadata = MetaData()
# Base = declarative_base(metadata=metadata)


# class Users(Base):
#     __tablename__ = "users"

#     id = Column(Integer, autoincrement=True, primary_key=True)
#     username = Column(String(255), index=True, unique=True)
#     password = Column(String(256))
#     userpic = Column(BLOB, nullable=True)

#     atime = Column(
#         DateTime(timezone=True), default=func.now(), onupdate=func.now()
#     )
#     is_active = Column(Boolean, default=True)

#     history = relationship("UsersHistory")


# class UsersHistory(Base):
#     __tablename__ = "history"

#     id = Column(Integer, autoincrement=True, primary_key=True)
#     user = Column(Integer, ForeignKey("users.id"), index=True)
#     address = Column(String(42), nullable=False)
#     port = Column(Integer, nullable=False)

#     ctime = Column(DateTime(timezone=True), default=func.now())


# class Contacts(Base):
#     __tablename__ = "contacts"

#     id = Column(Integer, autoincrement=True, primary_key=True)
#     owner = Column(Integer, ForeignKey("users.id"), index=True)
#     contact = Column(Integer, ForeignKey("users.id"), index=True)


# class Groups(Base):
#     __tablename__ = "groups"

#     id = Column(Integer, autoincrement=True, primary_key=True)
#     name = Column(String(255), index=True)


# class GroupMembers(Base):
#     __tablename__ = "group_members"

#     id = Column(Integer, autoincrement=True, primary_key=True)
#     user = Column(Integer, ForeignKey("users.id"), index=True)
#     group = Column(Integer, ForeignKey("groups.id"), index=True)


# class Messages(Base):
#     __tablename__ = "messages"
#     __table_args__ = (
#         Index("destination_user_delivered", "destination_user", "delivered"),
#         Index("destination_group_delivered", "destination_group", "delivered"),
#     )

#     id = Column(Integer, autoincrement=True, primary_key=True)
#     author = Column(Integer, ForeignKey("users.id"), nullable=False)
#     content = Column(String(4096), default="")
#     ctime = Column(DateTime(timezone=True), default=func.now())

#     destination_user = Column(Integer, ForeignKey("users.id"), nullable=True)
#     destination_group = Column(Integer, ForeignKey("groups.id"), nullable=True)
#     delivered = Column(Boolean, default=False)


# def create_db():
#     engine = create_engine(STORAGE, echo=False)
#     Base.metadata.create_all(engine)


class Users(Document):
    username = StringField(max_length=256, required=True)
    password = StringField(max_length=256, required=True)
    userpic = BinaryField()

    atime = DateTimeField(default=datetime.now)
    is_active = BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.atime = datetime.now()
        super().save(*args, **kwargs)


class UsersHistory(Document):
    user = ReferenceField(Users)
    address = StringField(max_length=42, required=True)
    port = IntField(required=True)

    ctime = DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        if not self.ctime:
            self.ctime = datetime.now()
        super().save(*args, **kwargs)


class Contacts(Document):
    owner = ReferenceField(Users, reverse_delete_rule=CASCADE)
    contact = ReferenceField(Users, reverse_delete_rule=CASCADE)


class Groups(Document):
    name = StringField(max_length=256, required=True)


class GroupMembers(Document):
    user = ReferenceField(Users)
    group = ReferenceField(Groups)


class Messages(Document):
    author = ReferenceField(Users)
    content = StringField(max_length=8192, required=True, default="")
    ctime = DateTimeField(default=datetime.now)

    destination_user = ReferenceField(Users)
    destination_group = ReferenceField(Groups)
    delivered = BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.ctime:
            self.ctime = datetime.now()
        super().save(*args, **kwargs)
