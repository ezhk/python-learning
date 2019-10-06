from threading import Thread
import time
from queue import Queue

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .utils import recv_data
from .config import STORAGE
from .models import Users


class MessageReader(Thread):
    def __init__(self, sock, logger):
        super().__init__()
        self.daemon = True
        self.sock = sock
        self.logger = logger

    def run(self):
        while True:
            data = recv_data(self.sock)
            if not data:
                time.sleep(0.3)
                continue

            if not set({"from", "to", "message"}) - set(data.keys()):
                self.logger.info(f"Сообщение от {data['from']} >{data['to']} : {data['message']}")
                self.logger.debug(f"Получено корректное сообщение от сервера: {data}")
        return True


class Clients(object):
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
