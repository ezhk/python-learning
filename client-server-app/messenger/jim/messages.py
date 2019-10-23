import datetime

from .config import ENCODING
from .decorators import log


@log
def authenticate(account_name=None, password=None):
    return {
        "action": "authenticate",
        "time": datetime.datetime.now().timestamp(),
        "user": {"account_name": account_name, "password": password},
    }


@log
def presence(account_name=None, status=None):
    return {
        "action": "presence",
        "time": datetime.datetime.now().timestamp(),
        "type": "status",
        "user": {"account_name": account_name, "status": status},
    }


def is_presence_message(message):
    try:
        if message["action"] == "presence":
            return message["user"]["account_name"]
    except Exception:
        pass
    return None


@log
def probe():
    return {"action": "probe", "time": datetime.datetime.now().timestamp()}


@log
def msg(message=None, source=None, destination=None):
    return {
        "action": "msg",
        "time": datetime.datetime.now().timestamp(),
        "from": source,
        "to": destination,
        "encoding": ENCODING,
        "message": message,
    }


def is_message(message):
    try:
        if message["action"] == "msg":
            return message["from"], message["to"], message["encoding"], message["message"]
    except Exception:
        pass
    return None


def get_recipient(message):
    try:
        return message.get("to", None)
    except Exception:
        pass
    return None


@log
def join(room=None):
    return {"action": "join", "time": datetime.datetime.now().timestamp(), "room": room}


@log
def leave(room=None):
    return {"action": "leave", "time": datetime.datetime.now().timestamp(), "room": room}


@log
def quit():
    return {"action": "quit"}


@log
def response(status, message="", is_success=True):
    body = {"response": status, "time": datetime.datetime.now().timestamp()}

    message_desc = {"alert": message} if is_success else {"error": message}
    body.update(message_desc)

    return body


@log
def get_contacts(account_name=None):
    return {
        "action": "get_contacts",
        "time": datetime.datetime.now().timestamp(),
        "user": account_name,
    }


@log
def is_get_contacts(message):
    try:
        if message["action"] == "get_contacts":
            return message["user"]
    except Exception:
        pass
    return None


@log
def add_contact(account_name=None, contact=None):
    return {
        "action": "add_contact",
        "time": datetime.datetime.now().timestamp(),
        "user": account_name,
        "contact": contact,
    }


@log
def del_contact(account_name=None, contact=None):
    return {
        "action": "del_contact",
        "time": datetime.datetime.now().timestamp(),
        "user": account_name,
        "contact": contact,
    }


def is_contact_operation(message):
    try:
        if message["action"] == "add_contact" or message["action"] == "del_contact":
            return message["action"], message["user"], message["contact"]
    except Exception:
        pass
    return None


@log
def chat(source=None, destination=None):
    return {
        "action": "chat",
        "time": datetime.datetime.now().timestamp(),
        "from": source,
        "to": destination,
    }


def is_chat(message):
    try:
        if message["action"] == "chat":
            return message["from"], message["to"]
    except Exception:
        pass
    return None
