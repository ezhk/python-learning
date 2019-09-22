import __main__ as main

from logging import getLogger
from . import logger


def log(func):
    role = "server" if "server" in main.__file__ else "client"
    logger = getLogger(f"messenger.{role}")

    def wrapper(*args, **kwargs):
        logger.info(
            f"Вызвана функция {func.__name__} с аргументами {args}, "
            f"{kwargs} в модуле {func.__module__}"
        )
        return func(*args, **kwargs)

    return wrapper


class Log:
    """
    Class works like a @log decorator,
    only as example.
    """

    def __init__(self, function):
        self.function = function

        role = "server" if "server" in main.__file__ else "client"
        self.logger = getLogger(f"messenger.{role}")

    def __call__(self, *args, **kwargs):
        self.logger.info(
            f"Вызвана функция {self.function.__name__} с аргументами {args}, "
            f"{kwargs} в модуле {self.function.__module__}"
        )
        return self.function(*args, **kwargs)
