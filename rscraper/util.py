from datetime import datetime, timezone

from fake_useragent import UserAgent


def get_random_user_agent():
    return UserAgent().random


def get_timestamp_utc() -> datetime:
    return datetime.now(timezone.utc)
