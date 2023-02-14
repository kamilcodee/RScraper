import os.path
from datetime import datetime, timezone

from fake_useragent import UserAgent


def get_random_user_agent():
    return UserAgent().random


def get_timestamp_utc(as_str: bool = False) -> datetime | str:
    """
    :param as_str: return as string
    :raises TypeError
    :return: timestamp
    """

    if not isinstance(as_str, bool):
        raise TypeError(f'Param as_str has to be [True/False], got = {as_str} type = {type(as_str)}')

    timestamp = datetime.now(timezone.utc)

    return timestamp if not as_str else str(as_str)


def create_dir_if_nonexistent(path: str) -> None:
    if not os.path.isdir(path):
        os.mkdir(path)


def delete_file_if_exists(path: str) -> None:
    if os.path.exists(path):
        os.remove(path)
