#!/usr/bin/env python3

from logging import getLogger
from socket import socket, AF_INET, SOCK_STREAM
import sys

sys.path.append(".")

from jim.exceptions import MessageError
from jim.messages import response
from jim.utils import parse_arguments, parse_raw_json, is_valid_message, make_raw_json
from jim.config import BACKLOG, BUFSIZE
import jim.logger


if __name__ == "__main__":
    logger = getLogger("messenger.server")
    opts = parse_arguments()

    s = socket(family=AF_INET, type=SOCK_STREAM)
    s.bind((opts.address, opts.port))
    s.listen(BACKLOG)

    while True:
        sock, addr = s.accept()
        raw_data = sock.recv(BUFSIZE)
        data = parse_raw_json(raw_data)

        logger.debug(f"Получено сообщение от клиента {addr}: {data}")

        message = response(400, "Incorrect JSON", False)
        try:
            if is_valid_message(data):
                message = response(202, "Accepted", True)
        except MessageError as err:
            logger.error(f"Ошибка валидации сообщения от {addr}, {err}")

        sock.send(make_raw_json(message))
        sock.close()

    s.close()
