#!/usr/bin/env python

from socket import socket, AF_INET, SOCK_STREAM

import sys

sys.path.append('.')

from jim.config import BACKLOG, BUFSIZE
from jim.utils import parse_arguments, parse_raw_json, \
    is_valid_message, make_raw_json
from jim.messages import response

if __name__ == "__main__":
    opts = parse_arguments()

    s = socket(family=AF_INET, type=SOCK_STREAM)
    s.bind((opts.address, opts.port))
    s.listen(BACKLOG)

    while True:
        sock, addr = s.accept()
        raw_data = sock.recv(BUFSIZE)
        data = parse_raw_json(raw_data)

        print(f"Получено сообщение от клиента: {data}")
        message = response(400, 'Incorrect JSON', False)
        if is_valid_message(data):
            message = response(202, 'Accepted', True)

        sock.send(make_raw_json(message))
        sock.close()

    s.close()
