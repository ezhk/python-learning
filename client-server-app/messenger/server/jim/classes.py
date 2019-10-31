from logging import getLogger
from threading import Thread
import time
from select import select
from socket import socket, AF_INET, SOCK_STREAM

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
    get_recipient,
    response,
)
from .models import Users, UsersHistory, Contacts, Groups, Messages
from .security import AsymmetricCipher, SymmetricCipher, get_text_digest
from .utils import is_valid_message, send_data, recv_data, load_server_settings


class ServerThread(object):
    """
    Running server object as a thread.
    """

    def __init__(self, logger):
        super().__init__()
        self.server = None
        self.thread = None

        self.logger = logger

    def start(self):
        """
        Read server settings and run Server object
        in a thread and store output in self variable.
        """

        if self.thread and self.thread.is_alive():
            return False

        settings = load_server_settings()
        self.server = Server(
            settings.get("address"),
            int(settings.get("port")),
            logger=self.logger,
        )
        self.thread = Thread(target=self.server.run, daemon=True)
        self.thread.start()
        return True

    def stop(self):
        """
        Calls stop for early running thread and join it.
        """

        try:
            self.server.stop()
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


class UsersExtension(object):
    """
    Class abstraction above user model in SQLAlchemy.
    """

    def __init__(self):
        self.sockets = {}
        self.groups = {}
        self.delayed_messages = {}

        self.salt = SALT

        engine = create_engine(STORAGE, pool_recycle=3600, echo=False)
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

    def presence(self, client, socket):
        """
        Create and save user history when
        received presence message type.
        """

        def _save_history(client, socket):
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

                (address, port) = socket.getpeername()
                h_object = UsersHistory(
                    user=user.id, address=address, port=port
                )
                self.session.add(h_object)

                self.session.commit()
            except Exception:
                self.session.rollback()
                return False
            return True

        self.sockets.update({client: socket})
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

        return _save_history(client, socket)

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

    def get_socket(self, client):
        """
        Return socket data from internal dict "sockets".
        Record in this "sockets" will be added when user
        will be connected to server.
        """

        if self.is_active(client):
            return self.sockets.get(client, None)
        return None

    @property
    def all_sockets(self):
        """
        Return sockets dict with users connections.
        """

        return self.sockets

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


class Server(metaclass=ServerVerifier):
    port = Port()

    """
    Main server object.
    All the magic are processing here:

    - encode/decode messages
    - recv and send messages
    - validate users and them state (connect/disconnect)
    """

    def __init__(self, address, port, **kwargs):
        self.cipher = AsymmetricCipher()
        self.address = address or "localhost"
        self.port = port

        self.family = kwargs.get("family", AF_INET)
        self.type = kwargs.get("type", SOCK_STREAM)
        self.backlog = kwargs.get("backlog", BACKLOG)
        self.timeout = kwargs.get("timeout", 0.1)

        # listen methods define sock object
        self.sock = None

        self.logger = kwargs.get("logger", getLogger("server"))

        self.users_extension = UsersExtension()
        self.client_sockets = []
        self.authenticated_clients = set()
        self.client_ciphers = {}

        self.running_flag = None

    def __del__(self):
        try:
            self.stop()
            self.sock.close()
        except Exception:
            pass

    def _process_input_message(self, data, sock):
        """
        Internal function, that detect message type
        and try to process it.
        """

        if is_key_exchange(data) is not None:
            session_key = self.cipher.decrypt(is_key_exchange(data).encode())
            cipher = SymmetricCipher(session_key)
            self.client_ciphers.update({sock: cipher})
            return

        # check auth data
        if is_authenticate(data) is not None:
            if self.users_extension.authenticate(*is_authenticate(data)):
                self.authenticated_clients.add(sock)
                return
            raise MessageError("Ошибка авторизации")

        if sock not in self.authenticated_clients:
            raise MessageError("Пользователь должен быть авторизован")

        # online message
        if is_presence_message(data) is not None:
            self.users_extension.presence(is_presence_message(data), sock)
            return

        # client message
        if is_message(data) is not None:
            self.users_extension.put_message(*is_message(data))
            return

        # load chat history
        if is_chat(data) is not None:
            return {"chat": self.users_extension.get_chat(*is_chat(data))}

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
            return

        return None

    def _process_output_message(self, data, sock):
        """
        Internal func that get recipient in message,
        find active socket and push message to user.
        """

        sended = 0
        if get_recipient(data) is not None:
            username = get_recipient(data)
            if (
                self.users_extension.is_active(username)
                and self.users_extension.get_socket(username) == sock
            ):
                send_data(sock, data, self.client_ciphers.get(sock, None))
                sended += 1
        else:
            send_data(sock, data, self.client_ciphers.get(sock, None))
            sended += 1
        return sended

    def listen(self):
        """
        Create listen socket on defined address and port.
        """

        self.sock = socket(family=self.family, type=self.type)
        self.sock.bind((self.address, self.port))
        self.sock.listen(self.backlog)
        self.sock.settimeout(self.timeout)
        self.sock.setblocking(0)

    def pull_requests(self, r_clients):
        """
        Read messages from read sockets, returned by select action.
        Here call internal function _process_input_message.
        """

        def _disconnect_client(self, c_socket):
            try:
                self.users_extension.disconnect(*c_socket.getpeername())

                self.authenticated_clients.remove(c_socket)
                self.client_sockets.remove(c_socket)
            except Exception:
                return False
            return True

        requests = {}
        for client_sock in r_clients:
            try:
                data = recv_data(
                    client_sock, self.client_ciphers.get(client_sock, None)
                )
                if data is None:
                    raise MessageError("Получено сообщение None")
            except Exception as err:
                self.logger.debug(f"Клиент отключился {client_sock}: {err}")
                _disconnect_client(self, client_sock)
                client_sock.close()
                continue

            self.logger.debug(
                f"Получено сообщение от клиента {client_sock}: {data}"
            )
            message = response(400, "Incorrect JSON", False)
            try:
                if is_valid_message(data):
                    message = response(202, "Accepted", True)
                    requests[client_sock] = data

                processing = self._process_input_message(data, client_sock)
                if processing:
                    message = response(202, processing, True)
            except MessageError as err:
                self.logger.error(
                    f"Ошибка валидации сообщения от {client_sock}, {err}"
                )
                message = response(400, str(err), False)

            try:
                send_data(
                    client_sock,
                    message,
                    self.client_ciphers.get(client_sock, None),
                )
            except Exception as err:
                self.logger.debug(
                    f"Клиент отключился при подтверждении {client_sock}: {err}"
                )
                self.users_extension.disconnect(*client_sock.getpeername())

                self.authenticated_clients.remove(client_sock)
                self.client_sockets.remove(client_sock)
                client_sock.close()

        return requests

    def push_requests(self, w_clients, requests):
        """
        Write messages to sockets, returned by select action.
        Here call internal function _process_output_message.
        """

        sended = 0
        for client in w_clients:
            try:
                for req in requests.values():
                    # reply to clients only messages
                    sended += self._process_output_message(req, client)
            except Exception as err:
                self.logger.debug(f"Клиент отключился {client}: {err}")
                self.users_extension.disconnect(*client.getpeername())

                self.authenticated_clients.remove(client)
                self.client_sockets.remove(client)
                client.close()
                continue
        return sended

    def _helo(self, c_socket):
        """
        Internal method sends help message with public key
        when client has been connected.
        """

        helo_message = helo(self.cipher.public_key.decode())
        send_data(c_socket, helo_message)

    def validate_client_sockets(self):
        """
        Function check, that possible to select with socket.
        """

        for c_sock in list(self.client_sockets):
            if c_sock.fileno() < 0:
                self.logger.debug(
                    f"Клиент отключился {c_sock}: fd is negative"
                )
                self.client_sockets.remove(c_sock)
                self.authenticated_clients.remove(c_sock)

    def run(self):
        """
        Main infinite cycle by flag running_flag was running here,
        it calls select() and get socket for read and write.
        pull_requests and push_requests are using here.
        """

        self.listen()
        self.running_flag = True

        while self.running_flag:
            try:
                sock, _ = self.sock.accept()
                self.client_sockets.append(sock)
                self._helo(sock)
            except OSError:
                # timeout exceeded
                pass

            try:
                self.validate_client_sockets()
                r_clients, w_clients, _ = select(
                    self.client_sockets, self.client_sockets, [], 0
                )
            except Exception as err:
                # received exception when client disconnect
                self.logger.debug(f"Исключение select: {err}")
                continue

            requests = {}
            if r_clients:
                requests = self.pull_requests(r_clients)
            if w_clients and requests:
                self.push_requests(w_clients, requests)

            time.sleep(0.1)

        self.sock.close()

    def stop(self):
        """
        Set running_flag to false and
        main cycle in run() will be ended.
        """

        self.running_flag = False
