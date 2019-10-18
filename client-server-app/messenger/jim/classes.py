from logging import getLogger
from threading import Thread
import time
from queue import Queue
from select import select
from socket import socket, AF_INET, SOCK_STREAM

from sqlalchemy import create_engine, or_
from sqlalchemy.orm import Session, aliased

from .config import STORAGE, BACKLOG
from .descriptors import Port, Username
from .exceptions import MessageError
from .metaclasses import ServerVerifier, ClientVerifier
from .messages import (
    presence,
    is_presence_message,
    is_message,
    is_get_contacts,
    is_contact_operation,
    msg,
    get_recipient,
    get_contacts,
    response,
)
from .server_models import Users, UsersHistory, Contacts, Groups, Messages
from .utils import is_valid_message, send_data, recv_data


class MessageReader(Thread):
    """
    Trhread, that read messages on client side.
    """

    def __init__(self, sock, logger):
        super().__init__()
        self.daemon = True
        self.sock = sock
        self.logger = logger

    def run(self):
        """
        Func is reading messages from socket in infinite cycle.
        """

        while True:
            data = recv_data(self.sock)
            if not data:
                time.sleep(0.3)
                continue

            # message received
            if not set({"from", "to", "message"}) - set(data.keys()):
                self.logger.info(f"Сообщение от {data['from']} >{data['to']} : {data['message']}")
                self.logger.debug(f"Получено корректное сообщение от сервера: {data}")
                continue

            # server data received
            if "alert" in data:
                if "contacts" in data["alert"]:
                    contacts = data["alert"]["contacts"]
                    self.logger.info(f"Список контактов: {', '.join(contacts)}")
        return True


class UsersExtension(object):
    """
    Class abstraction above user model in SQLAlchemy.
    """

    def __init__(self):
        self.sockets = {}
        self.groups = {}
        self.delayed_messages = {}

        engine = create_engine(STORAGE, pool_recycle=3600, echo=False)
        self.session = Session(bind=engine)

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
                user = self.session.query(Users).filter_by(username=client).first()
                if user is None:
                    return False

                (address, port) = socket.getpeername()
                h_object = UsersHistory(user=user.id, address=address, port=port)
                self.session.add(h_object)

                self.session.commit()
            except Exception as err:
                self.session.rollback()
                return False
            return True

        self.sockets.update({client: socket})
        user = self.session.query(Users).filter_by(username=client).first()

        # create user row if not exists
        if user is None:
            u_object = Users(username=client)
            try:
                self.session.add(u_object)
                self.session.commit()
            except Exception as err:
                self.session.rollback()
                return False
        # update user-state to active for exist user
        else:
            try:
                user.is_active = True
                self.session.commit()
            except Exception:
                self.session.rollback()
                return False

        return _save_history(client, socket)

    def quit(self, client):
        try:
            self.session.query(Users).filter_by(username=client).update({"is_active": False})
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
            if latest_session.address == address and latest_session.port == port:
                user.is_active = False
                self.session.commit()
        except Exception as err:
            self.session.rollback()
            return False
        return True

    def update_atime(self, client):
        try:
            self.session.query(Users).filter_by(username=client).update({})
            self.session.commit()
        except Exception:
            self.session.rollback()
            return False
        return True

    def is_active(self, client):
        user = self.session.query(Users).filter_by(username=client).first()
        return user is not None and user.is_active

    def get_socket(self, client):
        if self.is_active(client):
            return self.sockets.get(client, None)
        return None

    @property
    def all_sockets(self):
        return self.sockets

    def join(self, client, chat):
        """
        Group logic, don't used yet.
        """
        if client not in self.groups:
            self.groups.udpate({client: set()})
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
            destination = self.session.query(Groups).filter_by(name=recipient).first()
            if destination is None:
                return None
            m_object = Messages(author=author.id, destination_group=destination.id, content=message)
        else:
            destination = self.session.query(Users).filter_by(username=recipient).first()
            if destination is None:
                return None
            m_object = Messages(author=author.id, destination_user=destination.id, content=message)

        self.session.add(m_object)
        self.session.commit()
        return True

    def get_message(self, recipient):
        """
        Offline message logic, don't used yet.
        """

        usersAuthor = aliased(Users)
        usersDestination = aliased(Users)

        if recipient.startswith("#"):
            return (
                self.session.query(Messages)
                .join(usersAuthor, usersAuthor.id == Messages.author)
                .join(Groups, Groups.id == Messages.destination_group)
                .filter(Groups.name == recipient)
                .with_entities(usersAuthor.username, Groups.name, Messages.content, Messages.ctime)
                .all()
            )

        return (
            self.session.query(Messages)
            .join(usersAuthor, usersAuthor.id == Messages.author)
            .join(usersDestination, usersDestination.id == Messages.destination_user)
            .filter(usersDestination.username == recipient)
            .with_entities(
                usersAuthor.username, usersDestination.username, Messages.content, Messages.ctime
            )
            .all()
        )

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

        exist_contact = self.session.query(Contacts).filter_by(owner=owner.id, contact=contact.id)

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

    def __init__(self, address, port, **kwargs):
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

    def __del__(self):
        try:
            self.sock.close()
        except Exception:
            pass

    def _process_input_message(self, data, sock):
        # online message
        if is_presence_message(data) is not None:
            self.users_extension.presence(is_presence_message(data), sock)
            return

        # client message
        if is_message(data) is not None:
            self.users_extension.put_message(*is_message(data))
            return

        # receive contacts
        if is_get_contacts(data) is not None:
            return {"contacts": self.users_extension.get_contacts(is_get_contacts(data))}
        # add or delete contacts
        if is_contact_operation(data) is not None:
            self.users_extension.contact_operation(*is_contact_operation(data))
            return

        return None

    def _process_output_message(self, data, sock):
        sended = 0
        if get_recipient(data) is not None:
            username = get_recipient(data)
            if (
                self.users_extension.is_active(username)
                and self.users_extension.get_socket(username) == sock
            ):
                send_data(sock, data)
                sended += 1
        else:
            send_data(sock, data)
            sended += 1
        return sended

    def listen(self):
        self.sock = socket(family=self.family, type=self.type)
        self.sock.bind((self.address, self.port))
        self.sock.listen(self.backlog)
        self.sock.settimeout(self.timeout)
        self.sock.setblocking(0)

    def pull_requests(self, r_clients):
        requests = {}
        for client_sock in r_clients:
            try:
                data = recv_data(client_sock)
                if data is None:
                    raise MessageError("Получено сообщение None")
            except Exception as err:
                self.logger.debug(f"Клиент отключился {client_sock}: {err}")
                self.users_extension.disconnect(*client_sock.getpeername())
                self.client_sockets.remove(client_sock)
                client_sock.close()
                continue

            self.logger.debug(f"Получено сообщение от клиента {client_sock}: {data}")
            message = response(400, "Incorrect JSON", False)
            try:
                if is_valid_message(data):
                    message = response(202, "Accepted", True)
                    requests[client_sock] = data

                processing = self._process_input_message(data, client_sock)
                if processing:
                    message = response(202, processing, True)
            except MessageError as err:
                self.logger.error(f"Ошибка валидации сообщения от {client_sock}, {err}")

            try:
                send_data(client_sock, message)
            except Exception as err:
                self.logger.debug(f"Клиент отключился при подтверждении {client_sock}: {err}")
                self.users_extension.disconnect(*client_sock.getpeername())
                self.client_sockets.remove(client_sock)
                client_sock.close()

        return requests

    def push_requests(self, w_clients, requests):
        sended = 0
        for client in w_clients:
            try:
                for req in requests.values():
                    # reply to clients only messages
                    sended += self._process_output_message(req, client)
            except Exception as err:
                self.logger.debug(f"Клиент отключился {client}: {err}")
                self.users_extension.disconnect(*client.getpeername())
                self.client_sockets.remove(client)
                client.close()
                continue
        return sended

    def run(self):
        self.listen()

        while True:
            try:
                sock, addr = self.sock.accept()
                self.client_sockets.append(sock)
            except OSError as e:
                # timeout exceeded
                pass

            try:
                r_clients, w_clients, _ = select(self.client_sockets, self.client_sockets, [], 0)
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


class Client(metaclass=ClientVerifier):
    port = Port()
    username = Username()

    def __init__(self, address, port, username, **kwargs):
        self.username = username
        self.address = address or "localhost"
        self.port = port

        self.family = kwargs.get("family", AF_INET)
        self.type = kwargs.get("type", SOCK_STREAM)
        self.timeout = kwargs.get("timeout", 1)

        # listen methods define sock object
        self.sock = None

        # reader cannot be defined without sock
        self.reader = None

        self.readonly = kwargs.get("readonly", False)
        self.logger = kwargs.get("logger", getLogger("client"))

    def __del__(self):
        try:
            self.sock.close()
        except Exception:
            pass

    def _helo_message(self):
        message = presence(self.username)
        return send_data(self.sock, message)

    def _get_contacts(self):
        message = get_contacts(self.username)
        return send_data(self.sock, message)

    def connect(self):
        self.sock = socket(family=self.family, type=self.type)
        self.sock.connect((self.address, self.port))
        self.sock.settimeout(self.timeout)

        self._helo_message()
        self._get_contacts()

    def run(self):
        self.connect()
        self.reader = MessageReader(self.sock, self.logger)
        self.reader.start()

        if self.readonly:
            self.reader.join()
            return

        while True:
            try:
                text = input("Введите сообщение в формате 'recipient:message': ")
                (recipient, msg_body) = text.split(":", 1)
            except ValueError:
                self.logger.info("Введено пустое сообщение")
                continue

            message = msg(msg_body, self.username, recipient)
            send_data(self.sock, message)

        self.reader.join()
