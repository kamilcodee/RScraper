class RScraperConfig:
    """
    RScraper config class
    """

    def __init__(self, console_log: bool, save_to_file: bool):
        """
        :param console_log: enable console logging
        :param save_to_file: save data to .json
        :raises TypeError
        """

        if not isinstance(console_log, bool):
            raise TypeError(f'Param console_log has to be bool [True/False], got {console_log} type = {type(console_log)}')

        if not isinstance(save_to_file, bool):
            raise TypeError(
                f'Param save_to_file has to be bool [True/False], got = {save_to_file} type = {type(save_to_file)}')

        self.console_log = console_log
        self.base_url = 'https://www.reddit.com/'

        self.reddits_sub_url = 'reddits'
        self.reddits_per_request = 100

        self.data_dir = 'data'

        self.save_to_file = save_to_file
        self.reddits_save_filename = 'reddits.json'

        self.key_not_found = 'N/A'  # fallback if an attribute isn't found

    @property
    def details(self) -> dict[str, str]:
        """
        :return: Content of given config instance
        """

        return vars(self)
