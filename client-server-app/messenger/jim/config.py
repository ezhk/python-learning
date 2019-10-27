import logging

BACKLOG = 1024
BUFSIZE = 4096

SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 7777

ENCODING = "utf-8"

SERVER_LOGFILE = "log/server.log"
CLIENT_LOGFILE = "log/client.log"
LOGLEVEL = logging.DEBUG

STORAGE = "sqlite:///messenger.sql"
SALT = "376gizGQvQqaBE3GXzEC7J72PBKBSN0kB5msKOpGIN0o"
