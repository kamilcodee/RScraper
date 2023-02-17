import os.path
from datetime import datetime, timezone

from fake_useragent import UserAgent


def get_random_user_agent():
    return UserAgent().random


def get_timestamp_utc() -> datetime:
    """
    :raises TypeError
    :return: timestamp
    """

    return datetime.now(timezone.utc)


def create_dir_if_nonexistent(path: str) -> None:
    if not os.path.isdir(path):
        os.mkdir(path)


def delete_file_if_exists(path: str) -> None:
    if os.path.exists(path):
        os.remove(path)


def dir_exists(path: str) -> bool:
    return os.path.isdir(path)


def file_exists(path: str) -> bool:
    return os.path.isfile(path)
