class RScraperConfig:
    """
    RScraper config class
    """

    def __init__(self, console_log: bool):
        """
        :param console_log: enable console logging [True/False]
        :raises ValueError if console_log is not [True/False]
        """

        if not isinstance(console_log, bool):
            raise ValueError

        self.console_log = console_log
        self.base_url = 'https://www.reddit.com/'
        self.data_dir = 'data'

        self.reddits_sub_url = 'reddits'
        self.reddits_per_request = 100
        self.reddits_save_file = 'reddits.json'

    @property
    def details(self) -> dict[str, str]:
        """
        :return: Content of given config instance
        """

        return vars(self)
