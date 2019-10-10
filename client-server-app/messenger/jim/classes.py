from logging import getLogger
from threading import Thread
import time
from queue import Queue
from select import select
from socket import socket, AF_INET, SOCK_STREAM

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .config import STORAGE, BACKLOG
from .descriptors import Port, Username
from .exceptions import MessageError
from .messages import presence, is_presence_message, msg, get_recipient, response
from .models import Users
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

            if not set({"from", "to", "message"}) - set(data.keys()):
                self.logger.info(f"Сообщение от {data['from']} >{data['to']} : {data['message']}")
                self.logger.debug(f"Получено корректное сообщение от сервера: {data}")
        return True


class UsersExtension(object):
    """
    Class abstraction above user model in SQLAlchemy.
    """

    def __init__(self):
        self.sockets = {}
        self.groups = {}
        self.delayed_messages = {}

        engine = create_engine(STORAGE, echo=False)
        self.session = Session(bind=engine)

    def presence(self, client, socket):
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
            return True

        try:
            user.is_active = True
            self.session.commit()
        except Exception:
            self.session.rollback()
            return False
        return True

    def quit(self, client):
        try:
            self.session.query(Users).filter_by(username=client).update({"is_active": False})
            self.session.commit()
        except Exception:
            self.session.rollback()
            return False
        return True

    def update_atime(self, client):
        try:
            session.query(Users).filter_by(username=client).update({})
            session.commit()
        except Exception:
            self.session.rollback()
            return False
        return True

    def is_active(self, client):
        user = self.session.query(Users).filter_by(username=client).first()
        return user is not None and user.is_active

    def get_socket(self, client):
        if self.is_active(client):
            return self.sockets[client]
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

    def put_message(self, recipient, sender, message):
        """
        Offline message logic, don't used yet.
        """
        if recipient not in self.delayed_messages:
            self.delayed_messages[recipient] = Queue(0)
        self.delayed_messages[recipient].put(
            {"message": message, "sender": sender, "ctime": time.time()}
        )

    def get_message(self, recipient):
        """
        Offline message logic, don't used yet.
        """
        if recipient not in self.delayed_messages:
            return None
        return self.delayed_messages[recipient].get()


class Server(object):
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
        if is_presence_message(data) is not None:
            self.users_extension.presence(is_presence_message(data), sock)
        return True

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
                self.client_sockets.remove(client_sock)
                client_sock.close()
                continue

            self.logger.debug(f"Получено сообщение от клиента {client_sock}: {data}")
            message = response(400, "Incorrect JSON", False)
            try:
                if is_valid_message(data):
                    message = response(202, "Accepted", True)
                    requests[client_sock] = data
                self._process_input_message(data, client_sock)
            except MessageError as err:
                self.logger.error(f"Ошибка валидации сообщения от {client_sock}, {err}")

            try:
                send_data(client_sock, message)
            except Exception as err:
                self.logger.debug(f"Клиент отключился при подтверждении {client_sock}: {err}")
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


class Client(object):
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

    def connect(self):
        self.sock = socket(family=self.family, type=self.type)
        self.sock.connect((self.address, self.port))
        self.sock.settimeout(self.timeout)

        self._helo_message()

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
