import os
from datetime import datetime, timezone
from typing import Callable


class Util:

    @staticmethod
    def create_dir(path, callback: Callable) -> None:
        """
        Create directory if it does not exist
        :param path dirpath
        :param callback Dir has been created callback
        """

        if not os.path.isdir(path):
            os.mkdir(path)

            callback()

    @staticmethod
    def del_file(path, callback: Callable) -> None:
        """
        Delete file if it exists
        :param path filepath
        :param callback File has been removed callback
        """

        if os.path.isfile(path):
            os.remove(path)

            callback()

    @staticmethod
    def get_timestamp_utc() -> str:
        """
        Get timestamp utc
        """
        return str(datetime.now(timezone.utc))
