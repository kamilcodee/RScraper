from abc import ABC
from enum import Enum

from rscraper import RScraperConfig
from rscraper import util


class RSLogLevel(Enum):
    DEBUG = ('DEBUG', 1)
    INFO = ('INFO', 2)
    ERROR = ('ERROR', 3)


class RSLoggerInterface(ABC):

    def log(self, level: RSLogLevel, component: str, msg: str) -> None:
        """
        Log a message
        :param level log level
        :param component Component
        :param msg message to be logged
        """

        pass


class RSLogger(RSLoggerInterface):
    def __init__(self, rsconfig: RScraperConfig):
        self.rsconfig = rsconfig

    def log(self, level: RSLogLevel, component: str, msg: str) -> None:
        if level.value[1] >= self.rsconfig.target_log_level.value[1]:
            print(f'{util.get_timestamp_utc()}\t[{level.value[0]}]\t[RScraper]\t[{component}]\t{msg}')
