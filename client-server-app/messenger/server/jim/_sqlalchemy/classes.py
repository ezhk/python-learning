from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import Session, aliased

from .config import STORAGE, SALT, ENABLE_FILTER
from .models import (
    Users,
    UsersHistory,
    Groups,
    Contacts,
    GroupMembers,
    Messages,
)
from .security import get_text_digest


class UsersExtension(object):
    """
    Class abstraction above user model in SQLAlchemy.
    """

    def __init__(self):
        self.salt = SALT

        self.profanity = lambda message: False
        if ENABLE_FILTER:
            module = __import__("profanity_check")
            predict = getattr(module, "predict")
            self.profanity = lambda message: predict([message]).max()

        engine = create_engine(
            STORAGE,
            pool_recycle=3600,
            echo=False,
            connect_args={"check_same_thread": False},
        )
        self.session = Session(bind=engine)

    def authenticate(self, username, password):
        """
        Validate user password and create user if doesn't exist.
        Function calculate hash from string user + passwd + salt.
        """

        password_hash = get_text_digest(f"{username}{password}", self.salt)

        user = self.session.query(Users).filter_by(username=username).first()
        if user is None:
            u_object = Users(username=username, password=password_hash)
            try:
                self.session.add(u_object)
                self.session.commit()
            except Exception:
                self.session.rollback()
                return False
            return True

        if user.password is None:
            user.password = password_hash
            self.session.commit()
            return True

        if user.password == password_hash:
            return True
        return False

    def presence(self, client, address, port):
        """
        Create and save user history when
        received presence message type.
        """

        def _save_history(client, address, port):
            """
            Internal method, that save login history by user.
            """

            try:
                user = (
                    self.session.query(Users)
                    .filter_by(username=client)
                    .first()
                )
                if user is None:
                    return False

                h_object = UsersHistory(
                    user=user.id, address=address, port=port
                )
                self.session.add(h_object)

                self.session.commit()
            except Exception:
                self.session.rollback()
                return False
            return True

        user = self.session.query(Users).filter_by(username=client).first()

        # user must create in authenticate function
        if user is None:
            return False

        # update user-state to active for exist user
        try:
            user.is_active = True
            self.session.commit()
        except Exception:
            self.session.rollback()
            return False

        return _save_history(client, address, port)

    def quit(self, client):
        """
        Currently not used.
        """

        try:
            self.session.query(Users).filter_by(username=client).update(
                {"is_active": False}
            )
            self.session.commit()
        except Exception:
            self.session.rollback()
            return False
        return True

    def disconnect(self, address, port):
        """
        Try to make disconnected user is inactive.
        Found in history database last session with
        current address and port, set this user flag
        is_active to False.
        """

        try:
            user = (
                self.session.query(Users)
                .join(Users.history)
                .filter_by(address=address, port=port)
                .order_by(UsersHistory.ctime.desc())
                .first()
            )
            if user is None or not user.history:
                return True

            latest_session = user.history[-1]
            # validate latest session data, user might have same address and port
            # this case possible, when user is not logged in
            if (
                latest_session.address == address
                and latest_session.port == port
            ):
                user.is_active = False
                self.session.commit()
        except Exception:
            self.session.rollback()
            return False
        return True

    def update_atime(self, client):
        """
        Function call update with empty object,
        it causes update atime field in database.
        """

        try:
            self.session.query(Users).filter_by(username=client).update({})
            self.session.commit()
        except Exception:
            self.session.rollback()
            return False
        return True

    def is_active(self, client):
        """
        Return boolean value and check that user exists
        and active (is_active firld is True)
        """

        user = self.session.query(Users).filter_by(username=client).first()
        return user is not None and user.is_active

    @property
    def active_users(self):
        """
        Return dict with active users like a

            {
            "username": <value>,
            "address": <value>,
            "port": <value>,
            "atime": <value>
            }

        """

        users = []
        for user in (
            self.session.query(Users)
            .join(Users.history)
            .filter(Users.is_active == True)
            .order_by(UsersHistory.id)
            .all()
        ):
            last_access = user.history[-1]
            users.append(
                {
                    "username": user.username,
                    "address": last_access.address,
                    "port": last_access.port,
                    "atime": user.atime.isoformat(),
                }
            )
        return users

    @property
    def users_history(self):
        """
        Return users login history, presented as a dict:

            {
            "username": <value>,
            "address": <value>,
            "port": <value>,
            "ctime": <value>
            }
        """

        history = []
        for history_record in (
            self.session.query(UsersHistory)
            .join(Users, Users.id == UsersHistory.user)
            .order_by(UsersHistory.id.desc())
            .with_entities(
                Users.username,
                UsersHistory.address,
                UsersHistory.port,
                UsersHistory.ctime,
            )
            .limit(30)
            .all()
        ):
            username, address, port, ctime = history_record
            history.append(
                {
                    "username": username,
                    "address": address,
                    "port": port,
                    "ctime": ctime.isoformat(),
                }
            )
        return history

    def _create_group(self, group_name):
        group = self.session.query(Groups).filter_by(name=group_name).first()
        if group:
            return group

        g_object = Groups(name=group_name)
        try:
            self.session.add(g_object)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise RuntimeError("group cannot be created")
        return g_object

    def join(self, client, chat):
        """
        Group logic, don't used yet.
        """

        user = self.session.query(Users).filter_by(username=client).first()
        if not user:
            return False
        group = self._create_group(chat)

        exist_record = self.session.query(GroupMembers).filter_by(
            user=user.id, group=group.id
        )
        if exist_record.count():
            return True

        try:
            gm_object = GroupMembers(user=user.id, group=group.id)
            self.session.add(gm_object)
            self.session.commit()
        except Exception:
            self.session.rollback()
            return False
        return True

    def leave(self, client, chat):
        """
        Group logic, don't used yet.
        """

        user = self.session.query(Users).filter_by(username=client).first()
        if not user:
            return False
        group = self.session.query(Groups).filter_by(name=chat).first()
        if not group:
            return True

        exist_record = self.session.query(GroupMembers).filter_by(
            user=user.id, group=group.id
        )
        if not exist_record.count():
            return True

        try:
            exist_record.delete()
            self.session.commit()
        except Exception:
            self.session.rollback()
            return False
        return True

    def _get_defined_users(self, users=[]):
        db_users = (
            self.session.query(Users).filter(Users.username.in_(users)).all()
        )
        db_users = sorted(db_users, key=lambda u: users.index(u.username))
        return db_users

    def add_contact(self, owner, contact):
        """
        Function add link between user and contact in contact list.
        Also it validates that both accounts exist.
        """

        users = self._get_defined_users([owner, contact])
        if len(users) != 2:
            return None
        owner, contact = users
        exist_contact = self.session.query(Contacts).filter_by(
            owner=owner.id, contact=contact.id
        )
        if exist_contact.count():
            return True

        try:
            c_object = Contacts(owner=owner.id, contact=contact.id)
            self.session.add(c_object)
            self.session.commit()
        except Exception:
            self.session.rollback()
            return False
        return True

    def del_contact(self, owner, contact):
        users = self._get_defined_users([owner, contact])
        if len(users) != 2:
            return None
        owner, contact = users
        exist_contact = self.session.query(Contacts).filter_by(
            owner=owner.id, contact=contact.id
        )

        if not exist_contact.count():
            return True

        try:
            exist_contact.delete()
            self.session.commit()
        except Exception:
            self.session.rollback()
            return False
        return True

    def get_profile(self, client):
        """
        Return user detail information:
        models Users without password data:

            {
            "username": user.username,
            "userpic": user.userpic,
            "atime": user.atime,
            "is_active": user.is_active,
            }
        """

        user = self.session.query(Users).filter_by(username=client).first()
        return {
            "username": user.username,
            "userpic": user.userpic.decode() if user.userpic else None,
            "atime": user.atime.isoformat(),
            "is_active": user.is_active,
        }

    def update_userpic(self, client, userpic):
        try:
            self.session.query(Users).filter_by(username=client).update(
                {"userpic": userpic.encode()}
            )
            self.session.commit()
        except Exception:
            self.session.rollback()
            return False
        return True

    def put_message(self, sender, recipient, encoding, message):
        """
        Offline message logic.
        """

        author = self.session.query(Users).filter_by(username=sender).first()
        if author is None:
            return None

        m_object = None
        if recipient.startswith("#"):
            destination = (
                self.session.query(Groups).filter_by(name=recipient).first()
            )
            if destination is None:
                return None
            m_object = Messages(
                author=author.id,
                destination_group=destination.id,
                content=message,
            )
        else:
            destination = (
                self.session.query(Users).filter_by(username=recipient).first()
            )
            if destination is None:
                return None
            m_object = Messages(
                author=author.id,
                destination_user=destination.id,
                content=message,
            )

        self.session.add(m_object)
        self.session.commit()
        return True

    def censored_message(self, message):
        if self.profanity(message):
            return "<censored>"
        return message

    def get_chat(self, whom, source=None):
        """
        Return chat dialog between users or group.
        Messages limit in request = 50.
        Answer is a dict

            {
            "from": sender,
            "to": recipient,
            "text": text,
            "ctime": ctime.isoformat(),
            }
        """

        messages = []

        if not whom:
            return messages

        usersAuthor = aliased(Users)
        usersDestination = aliased(Users)

        if source.startswith("#"):
            for msg in (
                self.session.query(Messages)
                .join(usersAuthor, usersAuthor.id == Messages.author)
                .join(Groups, Groups.id == Messages.destination_group)
                .filter(Groups.name == source)
                .with_entities(
                    usersAuthor.username,
                    Groups.name,
                    Messages.content,
                    Messages.ctime,
                )
                .order_by(Messages.ctime.desc())
                .limit(50)
                .all()
            ):
                user, group, text, ctime = msg
                messages.append(
                    {
                        "from": user,
                        "to": group,
                        "text": self.censored_message(text),
                        "ctime": ctime.isoformat(),
                    }
                )
            return messages

        for msg in (
            self.session.query(Messages)
            .join(usersAuthor, usersAuthor.id == Messages.author)
            .join(
                usersDestination,
                usersDestination.id == Messages.destination_user,
            )
            .filter(
                or_(
                    and_(
                        usersAuthor.username == source,
                        usersDestination.username == whom,
                    ),
                    and_(
                        usersAuthor.username == whom,
                        usersDestination.username == source,
                    ),
                )
            )
            .with_entities(
                usersAuthor.username,
                usersDestination.username,
                Messages.content,
                Messages.ctime,
            )
            .order_by(Messages.ctime.desc())
            .limit(50)
            .all()
        ):
            sender, recipient, text, ctime = msg
            messages.append(
                {
                    "from": sender,
                    "to": recipient,
                    "text": self.censored_message(text),
                    "ctime": ctime.isoformat(),
                }
            )

        return messages

    def get_group_members(self, name):
        members = (
            self.session.query(GroupMembers)
            .join(Groups, Groups.id == GroupMembers.group)
            .join(Users, Users.id == GroupMembers.user)
            .filter(Groups.name == name)
            .with_entities(Users.username)
            .all()
        )
        return [member.username for member in members]

    def get_contacts(self, user):
        """
        Get contact usernames by username-owner.
        Background it called SQL query like a:

            SELECT u2.username FROM contacts
            JOIN users ON users.id = contacts.owner
            JOIN users AS u2 ON u2.id = contacts.contact
            WHERE users.username = user;

        """

        usersContact = aliased(Users)
        usersOwner = aliased(Users)

        contacts = (
            self.session.query(Contacts)
            .join(usersOwner, usersOwner.id == Contacts.owner)
            .join(usersContact, usersContact.id == Contacts.contact)
            .filter(usersOwner.username == user)
            .with_entities(usersContact.username)
            .all()
        )

        groups = (
            self.session.query(GroupMembers)
            .join(Groups, Groups.id == GroupMembers.group)
            .join(Users, Users.id == GroupMembers.user)
            .filter(Users.username == user)
            .with_entities(Groups.name)
            .all()
        )

        contacts = [contact.username for contact in contacts]
        groups = [group.name for group in groups]
        return contacts + groups

    def contact_operation(self, action, user, input_contact):
        """
        Function add or del link between users/groups in contacts
        if users exist (if group doesn't exist, it wil be created).
        Operation depends on action "add_contact" or "del_contact".
        """

        def _process_group_operation(self, action, user, group):
            if action == "add_contact":
                return self.join(user, group)
            if action == "del_contact":
                return self.leave(user, group)
            return False

        def _process_user_operation(self, action, user, contact):
            if action == "add_contact":
                return self.add_contact(user, contact)
            if action == "del_contact":
                return self.del_contact(user, contact)
            return False

        if input_contact.startswith("#"):
            return _process_group_operation(self, action, user, input_contact)
        return _process_user_operation(self, action, user, input_contact)
