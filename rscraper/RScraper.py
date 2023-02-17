import json
from pprint import pprint

import requests

from rscraper import RScraperConfig
from rscraper import util
from rscraper.RSLogger import RSLogLevel
from rscraper.RSLogger import RSLogger
from rscraper.key.RedditKey import RedditKey


# TODO: multiprocessing / threading to speed up

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

    def scrape_reddits(self, limit: int | None, keys: list[RedditKey] = None, return_data: bool = False) -> None | dict:
        """
        Scrape reddit data
        :param limit: amount of reddits fetched, can be None for all
        :param keys: list of attributes to receive, can be None for all (default)
        :param return_data: return scraped data as dict, default False
        :raises TypeError, ValueError
        :return: None or dict of scraped data if return_data = True
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
        self.logger.log(RSLogLevel.INFO, 'Reddit Scraper',
                        f'Scraping with limit = {limit_per_request} per request | Reddit limit = {limit}')

        while not finished:
            request_url = ''.join(
                [self.rsconfig.base_url, self.rsconfig.reddits_sub_url, '.json', f'?limit={limit_per_request}',
                 f'&after={after}' if after else ''])

            self.logger.log(RSLogLevel.DEBUG, component, f'Requesting {request_url}')

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

            self.logger.log(RSLogLevel.DEBUG, component, f'Fetch count = {len(reddits_fetched)}')

        output_data = {
            'count': len(reddits_fetched),
            'timestamp': str(util.get_timestamp_utc()),
            'reddits': reddits_fetched
        }

        if self.rsconfig.save_to_file:
            data_dir = self.rsconfig.data_dir
            filename = self.rsconfig.reddits_save_filename
            save_file_path = f'{data_dir}/{filename}'

            util.create_dir_if_nonexistent(self.rsconfig.data_dir)
            util.delete_file_if_exists(save_file_path)

            # TODO: encapsulate
            with open(save_file_path, 'w') as reddit_out_file:
                json.dump(output_data, reddit_out_file, indent=4)

            self.logger.log(RSLogLevel.INFO, 'Reddit Scraper', f'Save file location = {save_file_path}')

        if return_data:
            return output_data

    def scrape_submissions(self, reddit_url_list: list[str] | None = None, limit: int = None) -> None:
        """
        Scrape submissions from subreddits
        :param reddit_url_list: list of reddit URLs to scrape [format /r/<title>/, example /r/Home],
         can be none to look for saved data (default None)
        :param limit: amount of submissions per reddit, can be None for all (default None)
        :return: None
        """

        def _load_scraped_reddits() -> list[str]:
            """
            Load data from the data dir and parse URLs
            :return: list of parsed URLS
            """

            if not util.dir_exists(self.rsconfig.data_dir):
                raise NotADirectoryError(f'Directory {self.rsconfig.data_dir} does not exist')

            reddit_data_file_path = f'{self.rsconfig.data_dir}/{self.rsconfig.reddits_save_filename}'
            if not util.file_exists(reddit_data_file_path):
                raise FileNotFoundError(f'File {reddit_data_file_path} does not exist')

            data = dict()
            with open(reddit_data_file_path, 'r') as in_file:
                data = json.load(in_file)

            # "url": "/r/Home/",
            urls: list[str]
            urls = list()
            for reddit in data['reddits']:
                url = reddit['data'].get('url')

                if not url:
                    raise KeyError(
                        f'URL can not be retrieved from {reddit_data_file_path}. Please ensure {reddit_data_file_path} '
                        f'contains reddit URLs, or provide a list of URLs to scrape in reddit_url_list param')

                urls.append(url)

            return urls

        def _format_url(url) -> str:
            """
            Parse URL, ensure correct format
            :param url: URL to be parsed
            :return: URL as str
            """
            EXPECTED_START = '/r/'

            if not url.startswith(EXPECTED_START):
                raise ValueError(f'{url} not in valid format, expected = /r/<title>/, example /r/Home')

            # TODO: parsing, "/r/Home/"

            if url.endswith('/'):
                url = url[:-1]

            url = url[1:]  # remove leading /

            return f'{self.rsconfig.base_url}{url}.json'

        if not reddit_url_list:
            reddit_url_list = _load_scraped_reddits()
        reddit_url_list = [_format_url(url) for url in reddit_url_list]

        if limit and not isinstance(limit, int):
            raise TypeError(f'Limit has to be [int/None], got {limit} type {type(limit)}')

        print()

        component = 'Submission Scraper'

        for url in reddit_url_list:
            finished = False
            after = None

            limit_per_request = self.rsconfig.submissions_per_request
            if limit and limit < self.rsconfig.submissions_per_request:
                limit_per_request = limit

            self.logger.log(RSLogLevel.INFO, component,
                            f'Scraping {url} with limit = {limit_per_request} per request | Submission limit = {limit}')

            submissions_fetched = list()

            while not finished:
                request_url = ''.join(
                    [url, '?limit=', f'{limit_per_request}', f'&after={after}' if after else ''])

                self.logger.log(RSLogLevel.DEBUG, component, f'Requesting {request_url}')

                req = requests.get(request_url, headers={'User-Agent': util.get_random_user_agent()})
                req_data = req.json().get('data')

                after = req_data['after']

                if not after:
                    finished = True

                for submission_data in req_data['children']:
                    # TODO: key parsing
                    submissions_fetched.append(submission_data)

                    if limit and len(submissions_fetched) >= limit:
                        finished = True
                        break

                self.logger.log(RSLogLevel.DEBUG, component, f'Fetch count for {url} = {len(submissions_fetched)}')

            pprint(submissions_fetched[0])
