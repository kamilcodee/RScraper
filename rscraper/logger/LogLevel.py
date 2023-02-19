from enum import Enum


class LogLevel(Enum):
    TRACE = ('TRACE', 0)
    DEBUG = ('DEBUG', 1)
    INFO = ('INFO', 2)
    WARN = ('WARN', 3)
    ERROR = ('ERROR', 4)
    FATAL = ('FATAL', 5)
    ALL = ('ALL', 6)
