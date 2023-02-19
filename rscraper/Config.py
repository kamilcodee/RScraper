from dataclasses import dataclass
from typing import Callable

from fake_useragent import UserAgent


@dataclass
class Config:
    base_url: str = 'https://www.reddit.com/'
    subreddits_sub_url: str = 'reddits'
    max_limit_per_request: int = 100

    user_agent: Callable[[], str] | str = lambda: UserAgent().random

    data_dir: str = 'data'
    subreddits_data_filename: str = 'subreddits.json'
