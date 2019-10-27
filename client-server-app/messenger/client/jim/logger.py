"""
Module works as a function, that create logging handler.
Also it defines log-format, show **formatter** variable.
"""

import logging
import logging.handlers
import sys

from .config import CLIENT_LOGFILE, LOGLEVEL, ENCODING


formatter = logging.Formatter(
    "%(asctime)s %(filename)s:%(lineno)s > %(module)s:%(levelname)s %(message)s"
)


# Client logger object
client_logger = logging.getLogger("messenger.client")
client_logger.setLevel(LOGLEVEL)

client_fh = logging.FileHandler(CLIENT_LOGFILE, encoding=ENCODING, mode="a")
client_fh.setFormatter(formatter)
client_fh.setLevel(logging.ERROR)
client_logger.addHandler(client_fh)

out_stream = logging.StreamHandler(sys.stdout)
out_stream.setFormatter(formatter)
out_stream.setLevel(logging.INFO)
client_logger.addHandler(out_stream)
