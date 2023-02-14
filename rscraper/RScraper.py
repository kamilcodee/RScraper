import json

import requests

from rscraper import RScraperConfig
from rscraper import util
from rscraper.RSLogger import RSLogLevel
from rscraper.RSLogger import RSLogger
from rscraper.key.RedditKey import RedditKey


class RScraper:
    """
    Reddit Scraper
    """

    def __init__(self, rsconfig: RScraperConfig):
        """
        :param rsconfig Config instance
        """

        self.rsconfig = rsconfig
        self.logger = RSLogger(self.rsconfig)

    def scrape_reddits(self, limit: int | None, keys: list[RedditKey] = None) -> None:
        """
        Scrape reddit data
        :param limit: amount of reddits fetched, can be None for all
        :param keys: list of attributes to receive, can be None for all (default)
        :raises TypeError, ValueError
        :return: None
        """

        def _process_reddit(in_data: dict[str, str]) -> dict[str, str]:
            """
            Parse reddit data
            :param in_data Input data of a reddit
            :param keys keys of interest, example: ['id', 'name']
            :return:
            """

            output = dict()

            if keys:
                for k in keys:
                    output[k.value] = in_data['data'].get(k.value, self.rsconfig.key_not_found)
            else:
                output = in_data

            return {'kind': in_data['kind'], 'data': output}

        # TODO: add metrics (time taken etc)

        if limit:
            if not isinstance(limit, int):
                raise TypeError(f'Limit has to be [int/None], got {limit} type {type(limit)}')

            if limit <= 0:
                raise ValueError(f'Limit has to be >= 1, got {limit}')

        if keys:
            if not isinstance(keys, list):
                raise TypeError(f'Keys attribute has to be a list or None, got {keys} type {type(keys)}')

            for i, key in enumerate(keys):
                if key not in RedditKey:
                    raise TypeError(f'Key of index {i} has to be a RedditKey, got {key} type {type(key)}')

        component = 'Reddit Scraper'

        after = None
        finished = False

        # if limit is lower than max request limit in config use the lower value
        limit_per_request = self.rsconfig.reddits_per_request
        if limit and limit < self.rsconfig.reddits_per_request:
            limit_per_request = limit

        reddits_fetched = list()

        print()
        self.logger.log(RSLogLevel.INFO, 'Reddit Scraper', f'Scraping with limit = {limit_per_request}')

        while not finished:
            request_url = ''.join(
                [self.rsconfig.base_url, self.rsconfig.reddits_sub_url, '.json', f'?limit={limit_per_request}',
                 f'&after={after}' if after else ''])

            self.logger.log(RSLogLevel.INFO, component, f'Requesting {request_url}')

            req = requests.get(request_url, headers={'User-Agent': util.get_random_user_agent()})
            req_data = req.json().get('data')

            if not req_data:
                # TODO: handling on error/ etc
                pass

            after = req_data['after']
            if not after:
                finished = True

            for reddit in req_data['children']:
                reddits_fetched.append(_process_reddit(reddit))

                if limit and len(reddits_fetched) >= limit:
                    finished = True
                    break

            self.logger.log(RSLogLevel.INFO, component, f'Fetch count = {len(reddits_fetched)}')

        if self.rsconfig.save_to_file:
            data_dir = self.rsconfig.data_dir
            filename = self.rsconfig.reddits_save_filename
            save_file_path = f'{data_dir}/{filename}'

            util.create_dir_if_nonexistent(self.rsconfig.data_dir)
            util.delete_file_if_exists(save_file_path)

            # TODO: encapsulate
            with open(save_file_path, 'w') as reddit_out_file:
                json.dump({
                    'count': len(reddits_fetched),
                    'timestamp': util.get_timestamp_utc(True),
                    'reddits': reddits_fetched
                }, reddit_out_file, indent=4)

            self.logger.log(RSLogLevel.INFO, 'Reddit Scraper', f'Save file location = {save_file_path}')
