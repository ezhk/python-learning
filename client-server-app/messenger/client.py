#!/usr/bin/env python

from logging import getLogger
from socket import socket, AF_INET, SOCK_STREAM

import sys

sys.path.append(".")

from jim.config import BUFSIZE
from jim.classes import MessageReader
from jim.exceptions import MessageError
from jim.utils import (
    parse_arguments,
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

        msg_reader = MessageReader(s, logger)
        msg_reader.start()

        _helo_message(s, opts)
        if opts.readonly:
            msg_reader.join()
            sys.exit()

        while True:
            try:
                text = input("Введите сообщение в формате 'recipient:message': ")
                (recipient, msg_body) = text.split(":", 1)
            except ValueError:
                logger.info("Введено пустое сообщение")
                continue

            message = msg(msg_body, opts.username, recipient)
            send_data(s, message)

        msg_reader.join()
