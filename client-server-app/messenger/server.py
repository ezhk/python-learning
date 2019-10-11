#!/usr/bin/env python3

from logging import getLogger
import sys

sys.path.append(".")

from jim.utils import parse_arguments
from jim.classes import Server
import jim.logger


if __name__ == "__main__":
    logger = getLogger("messenger.server")
    opts = parse_arguments()

    server = Server(opts.address, opts.port, logger=logger)
    server.run()
