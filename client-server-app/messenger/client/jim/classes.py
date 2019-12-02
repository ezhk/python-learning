from logging import getLogger
from threading import Thread
import time
from socket import socket, AF_INET, SOCK_STREAM

from kivy.app import App as KivyApp
from PyQt5 import QtCore

from .descriptors import Port, Username
from .messages import (
    is_helo,
    key_exchange,
    authenticate,
    presence,
    msg,
    chat,
    get_contacts,
    add_contact,
    del_contact,
    update_userpic,
    is_error_response,
)
from .security import (
    AsymmetricCipher,
    SymmetricCipher,
    generate_base64_session_key,
)
from .utils import send_data, recv_data


class Client(Thread, QtCore.QObject):
    """
    Class define client object, that based on Thread.

    Contains different methods for recv and send messages,
      all this methods are internal.

    External methods:

    - connect, open socket to server
    - close, close earlier openned socket
    - run, called, when Thread is starting,
      infinite read data from socket while
      running flas is True
    - stop, set running flag to False
    """

    port = Port()
    username = Username()

    client_error = QtCore.pyqtSignal(str)
    server_message = QtCore.pyqtSignal(dict)

    def __init__(self, address, port, username, password, **kwargs):
        Thread.__init__(self)
        QtCore.QObject.__init__(self)

        self.daemon = True

        self.username = username
        self.password = password
        self.address = address or "localhost"
        self.port = port or 7777

        # Root kivy object, using for send events
        self.kivy_object = kwargs.get("kivy_object", None)

        self.family = kwargs.get("family", AF_INET)
        self.type = kwargs.get("type", SOCK_STREAM)
        self.timeout = kwargs.get("timeout", 1)
        self.logger = kwargs.get("logger", getLogger("client"))

        # connect methods define sock object
        self.sock = None
        self.cipher = None
        self.running_flag = None

        self.current_chat = None
        self.contacts = []
        self.user_profile = None

    @property
    def active_chat(self):
        return self.current_chat

    @active_chat.setter
    def active_chat(self, value):
        self.current_chat = value

    def __del__(self):
        try:
            self.sock.close()
        except Exception:
            pass

    def _authenticate(self):
        message = authenticate(self.username, self.password)
        return send_data(self.sock, message, self.cipher)

    def _presence_message(self):
        message = presence(self.username)
        return send_data(self.sock, message, self.cipher)

    def _get_contacts(self):
        message = get_contacts(self.username)
        return send_data(self.sock, message, self.cipher)

    def _add_contact(self, contact):
        message = add_contact(self.username, contact)
        return send_data(self.sock, message, self.cipher)

    def _delete_contact(self, contact):
        message = del_contact(self.username, contact)
        return send_data(self.sock, message, self.cipher)

    def _get_chat(self, contact):
        message = chat(self.username, contact)
        return send_data(self.sock, message, self.cipher)

    def _send_message(self, destination, text):
        message = msg(text, self.username, destination)
        return send_data(self.sock, message, self.cipher)

    def _key_exchange(self, key):
        message = key_exchange(key)
        send_data(self.sock, message, self.cipher)

    def _upload_userpic(self, image_bytes):
        message = update_userpic(self.username, image_bytes)
        return send_data(self.sock, message, self.cipher)

    def connect(self):
        """
        Method initialize connect to serverside
        with socket.connect() call.
        """

        try:
            self.sock = socket(family=self.family, type=self.type)
            self.sock.connect((self.address, self.port))
            self.sock.settimeout(self.timeout)
        except Exception as err:
            self.client_error.emit(str(err))
            if self.kivy_object:
                self.kivy_object.emit({"error": str(err)})
            return False
        return True

    def close(self):
        """
        Close client socket with server.
        """

        self.sock.close()

    def run(self):
        """
        Method representing the thread’s activity.
        In this thread client always read data from socket
        while special flag set to True.
        """

        if not self.connect():
            return
        self.running_flag = True

        while self.running_flag:
            data = recv_data(self.sock, self.cipher)
            if not data:
                time.sleep(0.3)
                continue

            if is_helo(data) is not None:
                asymmetric_cipher = AsymmetricCipher(is_helo(data))
                session_key = generate_base64_session_key()
                crypted_session_key = asymmetric_cipher.encrypt(session_key)
                self._key_exchange(crypted_session_key.decode())

                # cipher must be defined after _key_exchange action
                self.cipher = SymmetricCipher(session_key)

                time.sleep(0.3)
                self._authenticate()

                time.sleep(0.3)
                self._presence_message()
                self._get_contacts()

            # session must be encrypted
            if not self.cipher:
                continue

            # error
            if is_error_response(data) is not None:
                self.client_error.emit(is_error_response(data))
                if self.kivy_object:
                    self.kivy_object.emit({"error": is_error_response(data)})
                continue

            if "action" in data and "msg" in data["action"]:
                # if notification for current active tab
                if self.active_chat and (
                    (
                        data["to"] == self.username
                        and data["from"] == self.active_chat
                    )
                    or (
                        data["to"] == self.active_chat
                        and self.active_chat.startswith("#")
                    )
                ):
                    self._get_chat(self.active_chat)
                    continue

                # don't show background notifications for group chats
                if data["to"].startswith("#"):
                    continue

                # show notification about background message
                self.server_message.emit(
                    {
                        "action": "background_message",
                        "from": data["from"],
                        "message": data["message"],
                    }
                )
                if self.kivy_object:
                    self.kivy_object.emit(
                        {
                            "action": "background_message",
                            "from": data["from"],
                            "message": data["message"],
                        }
                    )

            if "alert" in data:
                if "contacts" in data["alert"]:
                    self.contacts = data["alert"]["contacts"]
                    self.server_message.emit({"action": "update_contacts"})
                    if self.kivy_object:
                        self.kivy_object.emit(
                            {
                                "action": "update_contacts",
                                "data": self.contacts,
                            }
                        )

                if "chat" in data["alert"]:
                    self.chat = data["alert"]["chat"]
                    self.server_message.emit({"action": "update_chat"})
                    if self.kivy_object:
                        self.kivy_object.emit(
                            {"action": "update_chat", "data": self.chat}
                        )

                if "user_profile" in data["alert"]:
                    self.user_profile = data["alert"]["user_profile"]
                    self.server_message.emit({"action": "update_profile"})
                    if self.kivy_object:
                        self.kivy_object.emit(
                            {
                                "action": "update_profile",
                                "data": self.user_profile,
                            }
                        )

        self.close()

    def stop(self):
        """
        Method set running flag to false and thread stays is possible for join.
        """

        self.running_flag = False
