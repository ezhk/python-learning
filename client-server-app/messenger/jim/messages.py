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
