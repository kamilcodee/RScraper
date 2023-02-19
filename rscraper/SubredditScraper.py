from typing import Any

import requests

from rscraper.logger import Logger, LogLevel
from rscraper import Config


class SubredditScraper:
    def __init__(self, config: Config):
        self._component: str = 'Subreddit scraper'
        self._config = config
        self._limit: int | None = None
        self._after: str | None = None  # reddit uses 'after' to point to next batch of data
        self._subreddits: list[dict[str, Any]] = list()

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

    @property
    def subreddits(self):
        return self._subreddits

    def _create_url(self) -> str:
        return ''.join(
            [self._config.base_url, self._config.subreddits_sub_url, '.json',
             f'?limit={self._config.max_limit_per_request}',
             f'&after={self._after}' if self._after else ''])

    def scrape(self) -> None:

        print()
        Logger.log(LogLevel.INFO, self._component, f'Scraping subreddits with limit = {self._limit}')

        finished = False
        while not finished:
            request_url = self._create_url()
            Logger.log(LogLevel.DEBUG, self._component, f'Requesting {request_url}')

            req = requests.get(request_url, headers={'User-Agent': self._config.user_agent()})
            req_data = req.json().get('data')

            if not req_data:
                # TODO: error handle
                continue

            self._after = req_data['after']
            if not self._after:
                finished = True

            for subreddit in req_data['children']:
                self._subreddits.append(subreddit)

                if self._limit and len(self._subreddits) >= self._limit:
                    finished = True
                    break

    def save(self) -> None:
        """
        Save to file
        """
