#!/usr/bin/env python

import argparse
from asyncio import new_event_loop, set_event_loop
import configparser
import json
import struct

from .config import SERVER_ADDRESS, SERVER_PORT, STORAGE, ENCODING
from . import messages
from . import exceptions


def parse_arguments():
    parser = argparse.ArgumentParser(description="Messenger application.")
    parser.add_argument(
        "-a", "--address", dest="address", type=str, default=SERVER_ADDRESS
    )
    parser.add_argument(
        "-p", "--port", dest="port", type=int, default=SERVER_PORT
    )
    parser.add_argument(
        "-u", "--username", dest="username", type=str, default=None
    )
    parser.add_argument(
        "-r", "--readonly", dest="readonly", action="store_true"
    )
    args = parser.parse_args()

    return args


def is_valid_message(msg):
    """
    Function check that received message is correct.
    """

    try:
        action = msg.get("action", None)
        # A bit magic: call function from messages with name as action
        msg_template = getattr(messages, action)()
    except Exception as err:
        raise exceptions.MessageError(err)

    # check that input messages contains all template keys
    if set(msg_template.keys()) - set(msg.keys()):
        return False
    return True


def parse_raw_json(binary_json):
    """
    Принимает на вход бинарный объект
    и конвертирует его в python представление,
    или возвращает пустой словарь.
    """

    try:
        json_string = binary_json.decode(ENCODING)
        return json.loads(json_string, encoding=ENCODING)
    except Exception:
        pass
    return {}


def make_raw_json(python_object):
    """
    Принимает объект python и делает из него JSON
    преставление в бинрном виде (с помощью encode).
    """

    json_string = json.dumps(python_object, ensure_ascii=False)
    return json_string.encode(ENCODING)


async def send_data(sock, data, cipher_object=None, loop=None):
    """
    Функция отправляет сообщение в сокет добавляя
    в начало сообщения его длину, это позволяет
    вычитывать из сокета в recv_data сначала 4 байта —
    длина сообщения, а потом само сообщение по длине.
    """

    try:
        if loop is None:
            loop = new_event_loop()
            set_event_loop(loop)

        data = make_raw_json(data)
        if cipher_object is not None:
            data = cipher_object.encrypt(data)

        raw_data = struct.pack("I", len(data)) + data
        return await loop.sock_sendall(sock, raw_data)
    except Exception:
        pass
    return None


async def recv_data(sock, cipher_object=None, loop=None):
    """
    Финкция сначала читает 4 байта из сокета — длина сообщения,
    а затем само сообщение, декодируем и возвращает разобранный
    json в виде структуры данных python.
    """

    try:
        if loop is None:
            loop = new_event_loop()
            set_event_loop(loop)

        len_data = await loop.sock_recv(sock, 4)
        len_data = struct.unpack("I", len_data)[0]

        raw_data = await loop.sock_recv(sock, len_data)
        if cipher_object is not None:
            raw_data = cipher_object.decrypt(raw_data)

        return parse_raw_json(raw_data)
    except Exception:
        pass
    return None


def load_server_settings():
    """
    Func returns serer settins from settings.ini
    presented as a dict:

        {
        "address": <value>,
        "port": <value>,
        "storage": <value>,
        }
    """

    settings = configparser.ConfigParser()
    settings.read("settings.ini")

    return {
        "address": settings.get("SERVER", "address", fallback=SERVER_ADDRESS),
        "port": settings.get("SERVER", "port", fallback=SERVER_PORT),
        "storage": settings.get("SERVER", "storage", fallback=STORAGE),
    }


def save_server_settings(address, port, storage):
    """
    Func stores server settings (address, port, storage)
    into sessings.ini.
    """

    settings = configparser.ConfigParser()
    settings.read("settings.ini")

    settings.update(
        {"SERVER": {"Address": address, "Port": port, "Storage": storage}}
    )
    with open("settings.ini", "w") as fh:
        settings.write(fh)
