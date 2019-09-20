#!/usr/bin/env python

import argparse
import json

from .config import SERVER_ADDRESS, SERVER_PORT, ENCODING
from . import messages


def parse_arguments():
    parser = argparse.ArgumentParser(description='Messenger application.')
    parser.add_argument('-a', '--address', dest='address',
                        type=str, default=SERVER_ADDRESS)
    parser.add_argument('-p', '--port', dest='port',
                        type=int, default=SERVER_PORT)
    args = parser.parse_args()

    return args


def parse_raw_json(binary_json):
    try:
        json_string = binary_json.decode(ENCODING)
        return json.loads(json_string, encoding=ENCODING)
    except Exception as err:
        pass
    return {}


def make_raw_json(python_object):
    json_string = json.dumps(python_object, ensure_ascii=False)
    return json_string.encode(ENCODING)


def is_valid_message(msg):
    try:
        action = msg.get('action', None)
        # A bit magic: call function from messages with name as action
        msg_template = getattr(messages, action)()
    except Exception:
        return False

    # check that input messages contains all template keys
    if set(msg_template.keys()) - set(msg.keys()):
        return False
    return True


def is_valid_response(msg):
    if 'response' not in msg or 'time' not in msg:
        return False
    return True