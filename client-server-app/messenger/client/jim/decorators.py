"""
Module describes decorators.
"""

import sys

from logging import getLogger

# from . import logger


def log(func):
    """
    Function-decorator creates record about called function.
    """

    program_name = sys.argv[0]
    role = "server" if "server" in program_name else "client"
    logger = getLogger(f"messenger.{role}")

    def wrapper(*args, **kwargs):
        logger.debug(
            f"Вызвана функция {func.__name__} с аргументами {args}, "
            f"{kwargs} в модуле {func.__module__}"
        )
        return func(*args, **kwargs)

    return wrapper
