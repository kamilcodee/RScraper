from rscraper.logger import LogLevel


class Colours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Logger:

    @staticmethod
    def log(level: LogLevel, component: str, msg: str) -> None:
        """
        param: level log level
        param: component:
        """

        # TODO: depending on level different colour
        level = f'{Colours.OKGREEN}[{level.value[0]}]{Colours.ENDC}'

        timestamp = f'{Colours.HEADER}[timestamp]{Colours.ENDC}'
        component = f'{Colours.OKCYAN}[{component}]{Colours.ENDC}'

        print('\t'.join([timestamp, level, component, msg]))
