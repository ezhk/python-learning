#!/usr/bin/env python

from logging import getLogger
import sys

sys.path.append(".")

from jim.classes import Client
from jim.utils import parse_arguments
import jim.logger


if __name__ == "__main__":
    opts = parse_arguments()

    client = Client(
        opts.address,
        opts.port,
        opts.username,
        logger=getLogger("messenger.client"),
        readonly=opts.readonly,
    )
    client.run()
