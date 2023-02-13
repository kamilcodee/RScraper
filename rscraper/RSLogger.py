from abc import ABC
from enum import Enum

from rscraper import RScraperConfig
from rscraper import util


class RSLogLevel(Enum):
    INFO = 'INFO'
    ERROR = 'ERROR'


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
        print(f'{util.get_timestamp_utc()}\t[{level.value}]\t[RScraper]\t[{component}]\t{msg}')
