from rscraper.logger.LogLevel import LogLevel


class Colours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


class Logger:

    @staticmethod
    def log(level: LogLevel, component: str, msg: str) -> None:
        """
        param: level log level
        param: component:
        """

        level_colour = [Colours.OKBLUE, Colours.OKGREEN, Colours.WARNING, Colours.FAIL][level.value[1]]
        level = f'{level_colour}[{level.value[0]}]{Colours.ENDC}'

        timestamp = f'{Colours.HEADER}[timestamp]{Colours.ENDC}'
        component = f'{Colours.OKCYAN}[{component}]{Colours.ENDC}'

        print('\t'.join([timestamp, level, component, msg]))
