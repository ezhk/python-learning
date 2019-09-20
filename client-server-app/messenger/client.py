#!/usr/bin/env python

from socket import socket, AF_INET, SOCK_STREAM

from jim.config import BUFSIZE
from jim.utils import parse_arguments, make_raw_json, \
    parse_raw_json, is_valid_response
from jim.messages import presence

if __name__ == "__main__":
    opts = parse_arguments()

    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect((opts.address, opts.port))

        message = presence("John Galt", "Кто такой Джон Голт?")
        s.send(make_raw_json(message))

        raw_data = s.recv(BUFSIZE)
        data = parse_raw_json(raw_data)

        if is_valid_response(data):
            print(f"Получено корректное сообщение от сервера: {data}")
        else:
            print(f"Получено некорректное сообщение от сервера: {data}")
