import datetime

from .config import ENCODING
from .decorators import log


@log
def helo(publickey=None):
    """
    Server initiate key exchange with send public key.
    """

    return {
        "action": "helo",
        "time": datetime.datetime.now().timestamp(),
        "type": "handshake",
        "publickey": publickey,
    }


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


def is_key_exchange(message):
    """
    Checks that message has key_exchange data.
    Return key or None.
    """

    try:
        if message["action"] == "key_exchange":
            return message["key"]
    except Exception:
        pass
    return None


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


def is_authenticate(message=None):
    """
    Checks that message has authenticate data.
    Return (username, password) or None.
    """

    try:
        if message["action"] == "authenticate":
            return message["user"]["account_name"], message["user"]["password"]
    except Exception:
        pass
    return None


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


def is_presence_message(message):
    """
    Checks that message has presence data.
    Return username or None.
    """

    try:
        if message["action"] == "presence":
            return message["user"]["account_name"]
    except Exception:
        pass
    return None


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


def is_message(message):
    """
    Checks that message has msg data.
    Return (from, to, encoding, message) or None.
    """

    try:
        if message["action"] == "msg":
            return (
                message["from"],
                message["to"],
                message["encoding"],
                message["message"],
            )
    except Exception:
        pass
    return None


def get_recipient(message):
    """
    Function try to read recipient from data
    or return None.
    """

    try:
        return message.get("to", None)
    except Exception:
        pass
    return None


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


@log
def response(status, message="", is_success=True):
    """
    Function create response server message.
    """

    body = {"response": status, "time": datetime.datetime.now().timestamp()}

    message_desc = {"alert": message} if is_success else {"error": message}
    body.update(message_desc)

    return body


@log
def is_get_contacts(message):
    """
    Checks that message has get_contacts request.
    Return message user or None.
    """

    try:
        if message["action"] == "get_contacts":
            return message["user"]
    except Exception:
        pass
    return None


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


def is_contact_operation(message):
    """
    Checks that message has operation with contacts (add/del).
    Return (action, user, contact) or None.
    """

    try:
        if (
            message["action"] == "add_contact"
            or message["action"] == "del_contact"
        ):
            return message["action"], message["user"], message["contact"]
    except Exception:
        pass
    return None


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


def is_chat(message):
    """
    Checks that message has chat message.
    Return (from, to) or None.
    """

    try:
        if message["action"] == "chat":
            return message["from"], message["to"]
    except Exception:
        pass
    return None
