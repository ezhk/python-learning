#!/usr/bin/env python

import json
from logging import getLogger
from socket import socket, AF_INET, SOCK_STREAM

import sys

sys.path.append(".")

from jim.config import BUFSIZE
from jim.exceptions import MessageError
from jim.utils import (
    parse_arguments,
    make_raw_json,
    parse_raw_json,
    send_data,
    recv_data,
    is_valid_message,
    is_valid_response,
    raise_invalid_username,
)
from jim.messages import presence, msg
import jim.logger


def _helo_message(sock, opts):
    message = presence(opts.username)
    return send_data(sock, message)


def _ack_data(sock):
    data = recv_data(sock)
    if not is_valid_response(data):
        raise MessageError(f"Получено некорректное подтверждение от сервера: {data}")
    return data


def _recv_data(sock):
    data = recv_data(sock)
    if not data:
        return False

    if not is_valid_message(data):
        raise MessageError(f"Получено некорректное сообщение: {data}")
    return data


if __name__ == "__main__":
    logger = getLogger("messenger.client")
    opts = parse_arguments()
    raise_invalid_username(opts.username)

    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect((opts.address, opts.port))
        s.settimeout(1)

        _helo_message(s, opts)
        while True:
            if opts.write:
                text = input("Введите сообщение:")
                message = msg(text, opts.username, "_all")
                send_data(s, message)

            # read all data
            while True:
                try:
                    data = _recv_data(s)
                    if not data:
                        break

                    logger.info(f"Сообщение от {data['from']}: {data['message']}")
                    logger.debug(f"Получено корректное сообщение от сервера: {data}")
                except Exception as err:
                    pass
