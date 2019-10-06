#!/usr/bin/env python3

from logging import getLogger
from select import select
from socket import socket, AF_INET, SOCK_STREAM
import sys
import time

sys.path.append(".")

from jim.exceptions import MessageError
from jim.messages import response, is_presence_message, get_recipient
from jim.utils import parse_arguments, is_valid_message, send_data, recv_data, Clients
from jim.config import BACKLOG, BUFSIZE
import jim.logger


def process_input_message(data, sock):
    global clients_state

    if is_presence_message(data) is not None:
        clients_state.presence(is_presence_message(data), sock)
    return True


def process_output_message(data, sock):
    global clients_state

    sended = 0
    if get_recipient(data) is not None:
        username = get_recipient(data)
        if clients_state.is_active(username) and clients_state.get_socket(username) == sock:
            send_data(sock, data)
            sended += 1
    else:
        send_data(sock, data)
        sended += 1
    return sended


def get_request(r_clients, all_clients):
    requests = {}
    for client_sock in r_clients:
        try:
            data = recv_data(client_sock)
            if data is None:
                raise MessageError("Получено сообщение None")
        except Exception as err:
            logger.debug(f"Клиент отключился {client_sock}: {err}")
            all_clients.remove(client_sock)

            client_sock.close()
            continue

        logger.debug(f"Получено сообщение от клиента {addr}: {data}")
        message = response(400, "Incorrect JSON", False)
        try:
            if is_valid_message(data):
                message = response(202, "Accepted", True)
                requests[client_sock] = data
            process_input_message(data, client_sock)
        except MessageError as err:
            logger.error(f"Ошибка валидации сообщения от {addr}, {err}")

        try:
            send_data(client_sock, message)
        except Exception as err:
            logger.debug(f"Клиент отключился при подтверждении {client_sock}: {err}")
            all_clients.remove(client_sock)
            client_sock.close()

    return requests


def put_reply(w_clients, all_clients, requests):
    sended = 0
    for client in w_clients:
        try:
            for req in requests.values():
                # reply to clients only messages
                sended += process_output_message(req, client)
        except Exception as err:
            logger.debug(f"Клиент отключился {client}: {err}")
            all_clients.remove(client)
            client.close()
            continue

    return sended


if __name__ == "__main__":
    logger = getLogger("messenger.server")
    opts = parse_arguments()
    clients_state = Clients()

    s = socket(family=AF_INET, type=SOCK_STREAM)
    s.bind((opts.address, opts.port))
    s.listen(BACKLOG)
    s.settimeout(0.1)
    s.setblocking(0)

    sockets = []
    while True:
        try:
            sock, addr = s.accept()
            sockets.append(sock)
        except OSError as e:
            # timeout exceeded
            pass

        try:
            r_clients, w_clients, _ = select(sockets, sockets, [], 0)
        except Exception as err:
            # received exception when client disconnect
            logger.debug(f"Исключение select: {err}")
            continue

        requests = {}
        if r_clients:
            requests = get_request(r_clients, sockets)
        if w_clients and requests:
            put_reply(w_clients, sockets, requests)

        time.sleep(0.1)

    s.close()
