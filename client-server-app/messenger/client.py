#!/usr/bin/env python

from logging import getLogger
from socket import socket, AF_INET, SOCK_STREAM

import sys

sys.path.append(".")

from jim.config import BUFSIZE
from jim.utils import (
    parse_arguments,
    make_raw_json,
    parse_raw_json,
    is_valid_response,
    raise_invalid_username,
)
from jim.messages import presence
import jim.logger

if __name__ == "__main__":
    logger = getLogger("messenger.client")
    opts = parse_arguments()
    raise_invalid_username(opts.username)

    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect((opts.address, opts.port))

        message = presence(opts.username)
        s.send(make_raw_json(message))

        raw_data = s.recv(BUFSIZE)
        data = parse_raw_json(raw_data)

        if is_valid_response(data):
            logger.debug(f"Получено корректное сообщение от сервера: {data}")
        else:
            logger.error(f"Получено некорректное сообщение от сервера: {data}")
