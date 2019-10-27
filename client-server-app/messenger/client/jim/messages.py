import datetime

from .config import ENCODING
from .decorators import log


def is_helo(message):
    """
    Check that received message is helo.
    """

    try:
        if message["action"] == "helo":
            return message["publickey"]
    except Exception:
        pass
    return None


@log
def key_exchange(sessionkey=None):
    """
    Server initiate key exchange with send public key.
    """

    return {
        "action": "key_exchange",
        "time": datetime.datetime.now().timestamp(),
        "type": "handshake",
        "key": sessionkey,
    }


@log
def authenticate(account_name=None, password=None):
    """
    Return message with auth data:
    - username
    - password
    """

    return {
        "action": "authenticate",
        "time": datetime.datetime.now().timestamp(),
        "user": {"account_name": account_name, "password": password},
    }


@log
def presence(account_name=None, status=None):
    """
    Return dict, that contains presence data.
    """

    return {
        "action": "presence",
        "time": datetime.datetime.now().timestamp(),
        "type": "status",
        "user": {"account_name": account_name, "status": status},
    }


@log
def probe():
    """
    Currently not used.
    """

    return {"action": "probe", "time": datetime.datetime.now().timestamp()}


@log
def msg(message=None, source=None, destination=None):
    """
    Return dict with message data:
    - from message
    - to message
    - encoding, by default using UTF-8
    - message body
    """

    return {
        "action": "msg",
        "time": datetime.datetime.now().timestamp(),
        "from": source,
        "to": destination,
        "encoding": ENCODING,
        "message": message,
    }


@log
def join(room=None):
    """
    Currently not used.
    """
    return {
        "action": "join",
        "time": datetime.datetime.now().timestamp(),
        "room": room,
    }


@log
def leave(room=None):
    """
    Currently not used.
    """
    return {
        "action": "leave",
        "time": datetime.datetime.now().timestamp(),
        "room": room,
    }


@log
def quit():
    """
    Currently not used.
    """
    return {"action": "quit"}


def is_error_response(message):
    """
    Check that server-side returns error message.
    """

    try:
        if "error" in message:
            return message["error"]
    except Exception:
        pass
    return None


@log
def get_contacts(account_name=None):
    """
    Return dict, that contains request "get_contacts".
    Used for load user list.
    """

    return {
        "action": "get_contacts",
        "time": datetime.datetime.now().timestamp(),
        "user": account_name,
    }


@log
def add_contact(account_name=None, contact=None):
    """
    Return dict, that contains request "add_contact".
    Used when user add new contact.
    """

    return {
        "action": "add_contact",
        "time": datetime.datetime.now().timestamp(),
        "user": account_name,
        "contact": contact,
    }


@log
def del_contact(account_name=None, contact=None):
    """
    Return dict, that contains request "del_contact".
    Used when user delete new contact.
    """

    return {
        "action": "del_contact",
        "time": datetime.datetime.now().timestamp(),
        "user": account_name,
        "contact": contact,
    }


@log
def chat(source=None, destination=None):
    """
    Return dict, that contains request "chat".
    This call return chat with source and desctination sides.
    """

    return {
        "action": "chat",
        "time": datetime.datetime.now().timestamp(),
        "from": source,
        "to": destination,
    }

