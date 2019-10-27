"""
Module describes some client configuration contants.

Recommends for changing only:

- CLIENT_LOGFILE, define path to client logs
- LOGLEVEL, default level is debug
"""

import logging

SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 7777

ENCODING = "utf-8"

CLIENT_LOGFILE = "log/client.log"
LOGLEVEL = logging.DEBUG
