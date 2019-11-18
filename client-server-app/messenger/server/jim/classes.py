from logging import getLogger
from threading import Thread
import time
from select import select
from socket import socket, AF_INET, SOCK_STREAM

import asyncio

from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import Session, aliased

from .config import STORAGE, BACKLOG, SALT
from .descriptors import Port
from .exceptions import MessageError
from .metaclasses import ServerVerifier
from .messages import (
    helo,
    is_key_exchange,
    is_authenticate,
    is_presence_message,
    is_message,
    is_chat,
    is_get_contacts,
    is_contact_operation,
    is_update_userpic,
    get_recipient,
    response,
)
from .models import Users, UsersHistory, Contacts, Groups, Messages
from .security import AsymmetricCipher, SymmetricCipher, get_text_digest
from .utils import (
    is_valid_message,
    load_server_settings,
    conv_data_to_bytes,
    conv_bytes_to_data,
)


class UsersExtension(object):
    """
    Class abstraction above user model in SQLAlchemy.
    """

    def __init__(self):
        self.salt = SALT
        self.groups = {}

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
            print("here")
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

    def join(self, client, chat):
        """
        Group logic, don't used yet.
        """

        if client not in self.groups:
            self.groups.update({client: set()})
        self.groups[client].add(chat)
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

    def leave(self, client, chat):
        """
        Group logic, don't used yet.
        """
        if client not in self.groups:
            return False
        self.groups[client].remove(chat)
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

    def get_chat(self, recipient, sender=None):
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

        if not recipient:
            return messages

        usersAuthor = aliased(Users)
        usersDestination = aliased(Users)

        if recipient.startswith("#"):
            for msg in (
                self.session.query(Messages)
                .join(usersAuthor, usersAuthor.id == Messages.author)
                .join(Groups, Groups.id == Messages.destination_group)
                .filter(Groups.name == recipient)
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
                        "text": text,
                        "ctime": ctime.isoformat(),
                    }
                )

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
                        usersAuthor.username == sender,
                        usersDestination.username == recipient,
                    ),
                    and_(
                        usersAuthor.username == recipient,
                        usersDestination.username == sender,
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
                    "text": text,
                    "ctime": ctime.isoformat(),
                }
            )

        return messages

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

        return [contact.username for contact in contacts]

    def contact_operation(self, action, user, input_contact):
        """
        Function add or del link between users in contacts
        if users exist. Operation depends on action
        "add_contact" or "del_contact".
        """
        users = self.session.query(Users).filter(
            or_(Users.username == user, Users.username == input_contact)
        )
        if users.count() != 2:
            return None

        owner, contact = users[0], users[1]
        if users[0].username == input_contact:
            owner, contact = users[1], users[0]

        exist_contact = self.session.query(Contacts).filter_by(
            owner=owner.id, contact=contact.id
        )

        if not exist_contact.count() and action == "add_contact":
            c_object = Contacts(owner=owner.id, contact=contact.id)
            self.session.add(c_object)
            self.session.commit()
            return True

        if exist_contact.count() and action == "del_contact":
            exist_contact.delete()
            self.session.commit()
            return True

        return False


class AsyncioServer(asyncio.Protocol):
    cipher = AsymmetricCipher()

    _authenticated_clients = set()
    _ciphers = {}
    _transport_per_user = {}

    def __init__(self, **kwargs):
        self._transport = None
        self._address = None
        self._port = None

        self.logger = kwargs.get("logger", getLogger("server"))
        self.users_extension = UsersExtension()

    def _write(self, data):
        cipher = self._ciphers.get(self._transport, None)
        return self._transport.write(conv_data_to_bytes(data, cipher))

    def _read(self, data):
        cipher = self._ciphers.get(self._transport, None)
        return conv_bytes_to_data(data, cipher)

    def _init_session_messages(self, data):
        if is_key_exchange(data) is not None:
            session_key = self.cipher.decrypt(is_key_exchange(data).encode())
            cipher = SymmetricCipher(session_key)
            self._ciphers.update({self._transport: cipher})
            return True

        # check auth data
        if is_authenticate(data) is not None:
            username, password = is_authenticate(data)
            if self.users_extension.authenticate(username, password):
                self._authenticated_clients.add(self._transport)
                self._transport_per_user.update({username: self._transport})
                return True
            raise MessageError("Ошибка авторизации")

        if self._transport not in self._authenticated_clients:
            raise MessageError("Пользователь должен быть авторизован")

        return None

    def _user_state_messages(self, data):
        # online message
        if is_presence_message(data) is not None:
            username = is_presence_message(data)
            self.users_extension.presence(username, self._address, self._port)
            return {"user_profile": self.users_extension.get_profile(username)}

        # update userpic
        if is_update_userpic(data) is not None:
            username, image = is_update_userpic(data)

            self.users_extension.update_userpic(username, image)
            return {"user_profile": self.users_extension.get_profile(username)}
        return None

    def _user_messages(self, data):
        # load chat history
        if is_chat(data) is not None:
            return {"chat": self.users_extension.get_chat(*is_chat(data))}

        # client message
        if is_message(data) is not None:
            self.users_extension.put_message(*is_message(data))

        # deliver message to destination
        if get_recipient(data) is not None:
            username = get_recipient(data)
            if (
                self.users_extension.is_active(username)
                and username in self._transport_per_user
            ):
                transport = self._transport_per_user[username]
                cipher = self._ciphers.get(transport, None)
                transport.write(conv_data_to_bytes(data, cipher))
            return True
        return None

    def _user_contacts(self, data):
        # receive contacts
        if is_get_contacts(data) is not None:
            return {
                "contacts": self.users_extension.get_contacts(
                    is_get_contacts(data)
                )
            }

        # add or delete contacts
        if is_contact_operation(data) is not None:
            self.users_extension.contact_operation(*is_contact_operation(data))
            return True

    def handle_request(self, data):
        if self._init_session_messages(data):
            return None

        userstate_message = self._user_state_messages(data)
        if userstate_message:
            return userstate_message

        messages = self._user_messages(data)
        if messages:
            return messages

        contacts = self._user_contacts(data)
        if contacts:
            return contacts

        return None

    def connection_made(self, transport):
        self._transport = transport
        self._address, self._port = self._transport.get_extra_info("peername")

        # send ciphers to client, when it has beed connected
        helo_message = helo(self.cipher.public_key.decode())
        self._write(helo_message)

    def data_received(self, data):
        data = self._read(data)

        try:
            answer = self.handle_request(data)
            if answer and isinstance(answer, dict):
                answer = response(200, answer, True)
            elif is_valid_message(data):
                answer = response(202, "Accepted", True)
            else:
                raise MessageError("Incorrect request")
        except MessageError as err:
            answer = response(400, str(err), False)

        self._write(answer)

    def connection_lost(self, exc):
        # clean old ciphers
        if self._transport in self._ciphers:
            del self._ciphers[self._transport]

        # clean authenticated flag
        if self._transport in self._authenticated_clients:
            self._authenticated_clients.remove(self._transport)

        self.users_extension.disconnect(self._address, self._port)


class ServerThread(object):
    """
    Running server object as a thread.
    """

    def __init__(self, logger):
        super().__init__()
        self.thread = None
        self.loop = asyncio.get_event_loop()

        self.logger = logger

    def _serve(self, address, port):
        coro = self.loop.create_server(lambda: AsyncioServer(), address, port)
        server = self.loop.run_until_complete(coro)

        try:
            self.loop.run_forever()
        finally:
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())
            server.close()

    def start(self):
        """
        Read server settings and run Server object
        in a thread and store output in self variable.
        """

        if self.thread and self.thread.is_alive():
            return False

        settings = load_server_settings()
        self.thread = Thread(
            target=self._serve,
            args=(settings.get("address"), int(settings.get("port"))),
            daemon=True,
        )
        self.thread.start()
        return True

    def stop(self):
        """
        Calls stop for early running thread and join it.
        """

        try:
            self.loop.call_soon_threadsafe(self.loop.stop)
            self.thread.join()
        except Exception as err:
            self.logger.error(f"Cannot stop server: {err}")
            return False
        return True

    def alive(self):
        """
        Return thread alive status, boolean.
        """

        try:
            return self.thread.is_alive()
        except Exception:
            pass
        return False
