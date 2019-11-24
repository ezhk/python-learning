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
