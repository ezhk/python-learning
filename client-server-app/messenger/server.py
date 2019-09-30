#!/usr/bin/env python3

from logging import getLogger
from select import select
from socket import socket, AF_INET, SOCK_STREAM
import sys

sys.path.append(".")

from jim.exceptions import MessageError
from jim.messages import response
from jim.utils import parse_arguments, is_valid_message, send_data, recv_data
from jim.config import BACKLOG, BUFSIZE
import jim.logger


def get_request(r_clients, all_clients):
    requests = {}
    for client in r_clients:
        try:
            data = recv_data(client)
            if data is None:
                raise MessageError("Получено сообщение None")
        except Exception as err:
            logger.debug(f"Клиент отключился {client}: {err}")
            all_clients.remove(client)

            client.close()
            continue

        logger.debug(f"Получено сообщение от клиента {addr}: {data}")
        message = response(400, "Incorrect JSON", False)
        try:
            if is_valid_message(data):
                message = response(202, "Accepted", True)
                requests[client] = data
        except MessageError as err:
            logger.error(f"Ошибка валидации сообщения от {addr}, {err}")

        try:
            send_data(client, message)
        except Exception as err:
            logger.debug(f"Клиент отключился {client}: {err}")
            all_clients.remove(client)
            client.close()

    return requests


def put_reply(w_clients, all_clients, requests):
    sended = 0
    for client in w_clients:
        try:
            for req in requests.values():
                # reply to clients only messages
                send_data(client, req)
                sended += 1
        except Exception as err:
            logger.debug(f"Клиент отключился {client}: {err}")
            all_clients.remove(client)
            client.close()
            continue

    return sended


if __name__ == "__main__":
    logger = getLogger("messenger.server")
    opts = parse_arguments()

    s = socket(family=AF_INET, type=SOCK_STREAM)
    s.bind((opts.address, opts.port))
    s.listen(BACKLOG)
    s.settimeout(0.1)
    s.setblocking(0)

    clients = []
    while True:
        try:
            sock, addr = s.accept()
            clients.append(sock)
        except OSError as e:
            # timeout exceeded
            pass

        try:
            r_clients, w_clients, _ = select(clients, clients, [], 0)
        except Exception as err:
            # received exception when client disconnect
            logger.debug(f"Исключение select: {err}")

        requests = {}
        if r_clients:
            requests = get_request(r_clients, clients)
        if w_clients and requests:
            put_reply(w_clients, clients, requests)

    s.close()
