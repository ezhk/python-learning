"""
Module describes server configuration.

Recommends for changing only:

- SERVER_ADDRESS, IPaddress, where server will be listened
- SERVER_PORT, like a server address, but a port
- SERVER_LOGFILE, define path to client logs
- LOGLEVEL, default level is debug
- SALT, it's secure value, YOU MUST CHANGED IT IN PRODUCTION
"""

import logging

SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 7777

ENCODING = "utf-8"

SERVER_LOGFILE = "log/server.log"
LOGLEVEL = logging.DEBUG

# STORAGE = "sqlite:///messenger.sql"
STORAGE = "mongodb://root:0Kk3KVDbR0BVKzPUodjw@localhost:27017/messenger"
SALT = "376gizGQvQqaBE3GXzEC7J72PBKBSN0kB5msKOpGIN0o"

ENABLE_FILTER = True
