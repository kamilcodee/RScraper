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


def is_file(path: str) -> bool:
    return os.path.isfile(path)


def get_files_in_dir(path: str, ext: str = None) -> list[str]:
    """
    Return names of files in directory (just the name, not full path)
    :param path dir path
    :param ext file extension for the search, default None for all
    """

    if not dir_exists(path):
        raise NotADirectoryError(f'Directory {path} does not exist')

    listed = os.listdir(path)
    output = list()

    for item in listed:
        if is_file(f'{path}/{item}'):
            if ext and not item.endswith(ext):
                continue

            output.append(item)

    return output
