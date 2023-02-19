import json
from typing import Any

import requests

from rscraper import Config
from rscraper.Util import Util
from rscraper.logger.LogLevel import LogLevel
from rscraper.logger.Logger import Logger


class SubmissionScraper:
    def __init__(self, config: Config):
        self._component: str = 'Subreddit scraper'
        self._config = config
        self._limit: int | None = None
        self._subreddit_name_url_list: list[tuple[str, str]] = list()

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, value):
        if not isinstance(value, int):
            raise TypeError(f'Limit has to be [int/None], got {self.limit} type {type(self.limit)}')

        if value <= 0:
            raise ValueError(f'Limit has to be >= 1, got {self.limit}')

        self._limit = value

    def _load_subreddits(self):
        data_dir = self._config.data_dir
        save_file_path = f'{data_dir}/{self._config.subreddits_data_filename}'

        if not Util.dir_exists(data_dir):
            raise NotADirectoryError(f'Directory {data_dir} does not exist')

        if not Util.file_exists(save_file_path):
            raise FileNotFoundError(f'File {save_file_path} does not exist')

        with open(save_file_path, 'r') as in_file:
            in_data = json.load(in_file)

            subreddits = in_data['subreddits']

            for subreddit in subreddits:
                url = subreddit['data']['url'][:-1]
                name = url.replace('/r/', '')

                name_url = name, ''.join([self._config.base_url[:-1], url])

                self._subreddit_name_url_list.append(name_url)

        Logger.log(LogLevel.DEBUG, self._component,
                   f'Retrieved subreddits count = {len(self._subreddit_name_url_list)}')

    def _create_url(self, base_url: str, after: str) -> str:
        return ''.join(
            [base_url, '.json', '?limit=', f'{self._config.max_limit_per_request}', f'&after={after}' if after else ''])

    def scrape(self):

        print()
        Logger.log(LogLevel.INFO, self._component, f'Scraping subreddits with limit = {self._limit} per subreddit')

        self._load_subreddits()

        for subreddit_name, subreddit_url in self._subreddit_name_url_list:
            finished: bool = False
            after: str | None = None

            submissions: list[dict[str, Any]]
            submissions = list()

            while not finished:
                request_url = self._create_url(subreddit_url, after)

                Logger.log(LogLevel.DEBUG, self._component, f'{subreddit_name} - Requesting {request_url}')

                req = requests.get(request_url, headers={'User-Agent': self._config.user_agent()})
                req_data = req.json().get('data')

                after = req_data['after']

                if not after:
                    finished = True

                for submission_data in req_data['children']:
                    submissions.append(submission_data)

                    if self._limit and len(submissions) >= self._limit:
                        finished = True
                        break

            self._save_data(subreddit_name, submissions)

    def _save_data(self, subreddit_name: str, submissions: list[dict[str, Any]]):

        new_component = f'{self._component} - data save'

        data_dir = self._config.data_dir
        submissions_data_dir = self._config.submissions_data_dir
        full_submissions_dir_path = f'{data_dir}/{submissions_data_dir}'

        save_file_path = f'{full_submissions_dir_path}/{subreddit_name}.json'

        def callback_on_create() -> None:
            Logger.log(LogLevel.INFO, new_component,
                       f'Directory {full_submissions_dir_path} created')

        def callback_on_delete() -> None:
            Logger.log(LogLevel.WARN, new_component,
                       f'File {save_file_path} exists -> Deleted')

        Util.create_dir(data_dir, callback=None)
        Util.create_dir(full_submissions_dir_path, callback=callback_on_create)

        Util.del_file(save_file_path, callback=callback_on_delete)

        output = {
            'saved': Util.get_timestamp_utc(),
            'count': len(submissions),
            'submissions': submissions
        }

        with open(save_file_path, 'w') as out_file:
            json.dump(output, out_file, indent=4)

        Logger.log(LogLevel.INFO, new_component, f'Data saved to {save_file_path}')
