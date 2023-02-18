import json
from pprint import pprint

import requests

from rscraper import RScraperConfig
from rscraper import util
from rscraper.RSLogger import RSLogger, RSLogLevel
from rscraper.key import SubmissionKey, SubredditKey


# TODO: multiprocessing / threading to speed up [TODO1]
# TODO: add metrics (time taken, etc) [TODO4]
# TODO: general error handling [TODO5]
# TODO: comment scraping [TODO6]

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

    def scrape_subreddits(self, limit: int | None, keys: list[SubredditKey] = None, return_data: bool = False) \
            -> None | dict:
        """
        Scrape subreddit data
        :param limit: amount of subreddit fetched, can be None for all
        :param keys: list of attributes to receive, can be None for all (default)
        :param return_data: return scraped data as dict, default False
        :raises TypeError, ValueError
        :return: None or dict of scraped data if return_data = True
        """

        def _save_data() -> None:
            """
            Save data to the file specified in config
            """

            data_dir = self.rsconfig.data_dir
            filename = self.rsconfig.subreddits_save_filename
            save_file_path = f'{data_dir}/{filename}'

            util.create_dir_if_nonexistent(self.rsconfig.data_dir)
            util.delete_file_if_exists(save_file_path)

            with open(save_file_path, 'w') as reddit_out_file:
                json.dump(output_data, reddit_out_file, indent=4)

            self.logger.log(RSLogLevel.INFO, component, f'Save file location = {save_file_path}')

        def _process_subreddit(in_data: dict[str, str]) -> dict[str, str]:
            """
            Parse reddit data
            :param in_data Input data of a subreddit
            :param keys keys of interest, example: ['id', 'name']
            :return: dict of keys
            """

            output = dict()

            if keys:
                for k in keys:
                    output[k.value] = in_data['data'].get(k.value, self.rsconfig.key_not_found)
            else:
                output = in_data

            return {'kind': in_data['kind'], 'data': output}

        if limit:
            if not isinstance(limit, int):
                raise TypeError(f'Limit has to be [int/None], got {limit} type {type(limit)}')

            if limit <= 0:
                raise ValueError(f'Limit has to be >= 1, got {limit}')

        if keys:
            if not isinstance(keys, list):
                raise TypeError(f'Keys attribute has to be a list or None, got {keys} type {type(keys)}')

            for i, key in enumerate(keys):
                if key not in SubredditKey:
                    raise TypeError(
                        f'Key of index {i} has to be a {SubredditKey.__class__}, got {key} type {type(key)}')

        component = 'SubReddit Scraper'

        after = None
        finished = False

        # if limit is lower than max request limit in config use the lower value
        limit_per_request = self.rsconfig.subreddits_per_request
        if limit and limit < self.rsconfig.subreddits_per_request:
            limit_per_request = limit

        subreddits_fetched = list()

        print()
        self.logger.log(RSLogLevel.INFO, component,
                        f'Scraping with limit = {limit_per_request} per request | SubReddit limit = {limit}')

        while not finished:
            request_url = ''.join(
                [self.rsconfig.base_url, self.rsconfig.subreddits_sub_url, '.json', f'?limit={limit_per_request}',
                 f'&after={after}' if after else ''])

            self.logger.log(RSLogLevel.DEBUG, component, f'Requesting {request_url}')

            req = requests.get(request_url, headers={'User-Agent': self.rsconfig.ua_generator()})
            req_data = req.json().get('data')

            if not req_data:
                continue

            after = req_data['after']
            if not after:
                finished = True

            for subreddit in req_data['children']:
                subreddits_fetched.append(_process_subreddit(subreddit))

                if limit and len(subreddits_fetched) >= limit:
                    finished = True
                    break

            self.logger.log(RSLogLevel.DEBUG, component, f'Fetch count = {len(subreddits_fetched)}')

        output_data = {
            'count': len(subreddits_fetched),
            'timestamp': str(util.get_timestamp_utc()),
            'subreddits': subreddits_fetched
        }

        if self.rsconfig.save_to_file:
            _save_data()

        if return_data:
            return output_data

    def scrape_submissions(self, subreddit_url_list: list[str] | None = None, limit: int = None,
                           keys: list[SubmissionKey] | None = None) -> None:
        """
        Scrape submissions from subreddits
        :param subreddit_url_list: list of subreddit URLs to scrape [format /r/<title>/, example /r/Home],
         can be none to look for saved data (default None)
        :param limit: amount of submissions per subreddit, can be None for all (default None)
        :param keys: list of attributes to receive, can be None for all (default)
        :return: None
        """

        def _save_data() -> None:
            """
            Save data to the dir specified in the config
            """

            data_dir = self.rsconfig.data_dir
            submissions_data_dir = f'{data_dir}/{self.rsconfig.submissions_data_dir}'
            filename = f'{subreddit_name}.json'
            save_file_path = f'{submissions_data_dir}/{filename}'

            util.create_dir_if_nonexistent(data_dir)
            util.create_dir_if_nonexistent(submissions_data_dir)
            util.delete_file_if_exists(save_file_path)

            with open(save_file_path, 'w') as submission_out_file:
                json.dump(output_data, submission_out_file, indent=4)

            self.logger.log(RSLogLevel.INFO, component, f'Save file location = {save_file_path}')

        def _load_scraped_subreddits() -> list[str]:
            """
            Load data from the data dir and parse URLs
            :return: list of parsed URLS
            """

            if not util.dir_exists(self.rsconfig.data_dir):
                raise NotADirectoryError(f'Directory {self.rsconfig.data_dir} does not exist')

            subreddit_data_file_path = f'{self.rsconfig.data_dir}/{self.rsconfig.subreddits_save_filename}'
            if not util.file_exists(subreddit_data_file_path):
                raise FileNotFoundError(f'File {subreddit_data_file_path} does not exist')

            data = dict()
            with open(subreddit_data_file_path, 'r') as in_file:
                data = json.load(in_file)

            # "url": "/r/Home/",
            urls: list[str]
            urls = list()
            for subreddit in data['subreddits']:
                url = subreddit['data'].get('url')

                if not url:
                    raise KeyError(
                        f'URL can not be retrieved from {subreddit_data_file_path}.'
                        f' Please ensure {subreddit_data_file_path} '
                        f'contains subreddit URLs, or provide a list of URLs to scrape in subreddit_url_list param')

                urls.append(url)

            return urls

        def _get_name_from_url(url: str) -> str:
            """
            Return name from url, example from /r/Home return Home
            :param url: url to retrieve name from
            :return: name
            """

            if url.endswith('/'):
                url = url[:-1]

            url = url.replace('/r/', '')

            return url

        def _get_name_url_tuple(url) -> tuple[str, str]:
            """
            Parse URL, ensure correct format
            :param url: URL to be parsed
            :return: tuple (reddit_name, url)
            """
            EXPECTED_START = '/r/'

            if not url.startswith(EXPECTED_START):
                raise ValueError(f'{url} not in valid format, expected = /r/<title>/, example /r/Home')

            name = _get_name_from_url(url)

            if url.endswith('/'):
                url = url[:-1]

            url = url[1:]  # remove leading /

            return name, f'{self.rsconfig.base_url}{url}.json'

        def _process_submission(in_data: dict[str, str]) -> dict[str, str]:
            """
            Parse reddit data
            :param in_data Input data of a submission
            :param keys keys of interest, example: ['id', 'name']
            :return: dict of keys
            """

            output = dict()

            if keys:
                for k in keys:
                    output[k.value] = in_data['data'].get(k.value, self.rsconfig.key_not_found)
            else:
                output = in_data['data']

            return {'kind': in_data['kind'], 'data': output}

        if not subreddit_url_list:
            subreddit_url_list = _load_scraped_subreddits()

        subreddit_name_url_tuple_list: list[tuple[str, str]]
        subreddit_name_url_tuple_list = list()
        subreddit_name_url_tuple_list = [_get_name_url_tuple(url) for url in subreddit_url_list]

        if limit:
            if not isinstance(limit, int):
                raise TypeError(f'Limit has to be [int/None], got {limit} type {type(limit)}')

            if limit <= 0:
                raise ValueError(f'Limit has to be >= 1, got {limit}')

        if keys:
            if not isinstance(keys, list):
                raise TypeError(f'Keys attribute has to be a list or None, got {keys} type {type(keys)}')

            for i, key in enumerate(keys):
                if key not in SubmissionKey:
                    raise TypeError(
                        f'Key of index {i} has to be a {SubmissionKey.__class__}, got {key} type {type(key)}')

        print()

        component = 'Submission Scraper'

        for subreddit_name, url in subreddit_name_url_tuple_list:
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

                req = requests.get(request_url, headers={'User-Agent': self.rsconfig.ua_generator()})
                req_data = req.json().get('data')

                after = req_data['after']

                if not after:
                    finished = True

                for submission_data in req_data['children']:
                    submissions_fetched.append(_process_submission(submission_data))

                    if limit and len(submissions_fetched) >= limit:
                        finished = True
                        break

                self.logger.log(RSLogLevel.DEBUG, component, f'Fetch count for {url} = {len(submissions_fetched)}')

            output_data = {
                'subreddit': subreddit_name,
                'count': len(submissions_fetched),
                'timestamp': str(util.get_timestamp_utc()),
                'submissions': submissions_fetched
            }

            if self.rsconfig.save_to_file:
                _save_data()

    def scrape_comments(self, limit: int = None) -> None:
        """
        Scrape comments from submissions saved in the submission data dir
        :param limit: amount of submissions per subreddit, can be None for all (default None)
        """

        def _load_submissions() -> list[tuple[str, str, str]]:
            """
            Return tuple (reddit, url) of submissions saved in the submission data dir
            """

            data_dir = self.rsconfig.data_dir
            submissions_data_dir = f'{data_dir}/{self.rsconfig.submissions_data_dir}'

            if not util.dir_exists(data_dir):
                raise NotADirectoryError(f'Directory {data_dir} does not exist')

            if not util.dir_exists(submissions_data_dir):
                raise NotADirectoryError(f'Directory {submissions_data_dir} does not exist')

            submission_json_files = util.get_files_in_dir(submissions_data_dir, 'json')

            output: list[tuple[str, str]]
            output = list()

            for json_file in submission_json_files:
                with open(f'{submissions_data_dir}/{json_file}', 'r') as in_file:
                    in_data = json.load(in_file)

                subreddit = in_data.get('subreddit', self.rsconfig.key_not_found)

                for submission in in_data['submissions']:
                    submission_permalink = submission['data'].get('permalink')

                    if not submission_permalink:
                        raise KeyError(f'Submission from {json_file} does not contain the "permalink"')

                    output.append((subreddit, _format_link(submission_permalink)))

            return output

        def _format_link(link: str) -> str:
            if link.endswith('/'):
                link = link[:-1]

            if link.startswith('/'):
                link = link[1:]

            link = f'{self.rsconfig.base_url}{link}.json'

            return link

        def save_to_index(sub_name: str, sub_id: str) -> None:
            """
            Due to the fact submission names are lengthy, create an index file with id : name mappings
            :param sub_name name of submission
            :param sub_id id of submission
            """

            submission_index_file_path = f'{self.rsconfig.data_dir}/{self.rsconfig.comments_data_dir}/' \
                                         f'{self.rsconfig.submissions_index_file}.json'

            submissions_index = dict()
            if util.file_exists(submission_index_file_path):
                with open(submission_index_file_path, 'r') as in_file:
                    submissions_index = json.load(in_file)

                util.delete_file_if_exists(submission_index_file_path)

            submissions_index[sub_id] = sub_name

            with open(submission_index_file_path, 'w') as out_file:
                json.dump(submissions_index, out_file, indent=4)

        if limit:
            if not isinstance(limit, int):
                raise TypeError(f'Limit has to be [int/None], got {limit} type {type(limit)}')

            if limit <= 0:
                raise ValueError(f'Limit has to be >= 1, got {limit}')

        component = 'Comment Scraper'

        util.create_dir_if_nonexistent(f'{self.rsconfig.data_dir}/{self.rsconfig.comments_data_dir}')

        print()
        self.logger.log(RSLogLevel.DEBUG, component, f'Scraping with limit = {limit}')

        submissions_data = _load_submissions()
        for subreddit_name, submission_url in submissions_data:
            finished = False

            comments: list[dict]
            comments = list()

            submission_name = None
            submission_id = None

            while not finished:
                self.logger.log(RSLogLevel.DEBUG, component, f'Requesting {submission_url}')

                req = requests.get(submission_url, headers={'User-Agent': self.rsconfig.ua_generator()})

                # first element in array has info about submission, 2nd has comments
                if not submission_name:
                    submission_data = req.json()[0]['data']['children'][0]['data']

                    submission_name = submission_data.get('title', self.rsconfig.key_not_found)
                    submission_id = submission_data.get('id', self.rsconfig.key_not_found)

                req_data = req.json()[1]

                print(submission_name)
                print(submission_id)
                # pprint(req_data)

                save_to_index(submission_name, submission_id)
                finished = True

        pprint(submissions_data)
