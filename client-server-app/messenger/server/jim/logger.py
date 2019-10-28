"""
Module works as a function, that create logging handler.
Also it defines log-format, show **formatter** variable.
"""

import logging
import logging.handlers
import sys

from .config import SERVER_LOGFILE, LOGLEVEL, ENCODING


formatter = logging.Formatter(
    "%(asctime)s %(filename)s:%(lineno)s > %(module)s:%(levelname)s %(message)s"
)


# Server logger object
server_logger = logging.getLogger("messenger.server")
server_logger.setLevel(LOGLEVEL)

server_timed_fh = logging.handlers.TimedRotatingFileHandler(
    SERVER_LOGFILE, when="D", interval=1, backupCount=3, encoding=ENCODING
)
server_timed_fh.setLevel(logging.DEBUG)
server_timed_fh.setFormatter(formatter)
server_logger.addHandler(server_timed_fh)

err_stream = logging.StreamHandler(sys.stderr)
err_stream.setFormatter(formatter)
err_stream.setLevel(logging.ERROR)
server_logger.addHandler(err_stream)
