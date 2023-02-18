from rscraper import RScraperConfig, RScraper
from rscraper import SubredditKey, SubmissionKey
from rscraper.RSLogger import RSLogLevel
from rscraper.util import get_random_user_agent

if __name__ == '__main__':
    rsconfig = RScraperConfig(console_log=True, save_to_file=True)
    rsconfig.target_log_level = RSLogLevel.DEBUG  # override loglevel for debugging purposes
    rsconfig.ua_generator = get_random_user_agent  # own generation strategy for useragent

    rs = RScraper(rsconfig)

    reddits: dict
    reddits = rs.scrape_subreddits(limit=1, keys=[SubredditKey.ID, SubredditKey.NAME, SubredditKey.URL],
                                   return_data=True)

    rs.scrape_submissions(limit=1, keys=[SubmissionKey.ID, SubmissionKey.NAME, SubmissionKey.PERMALINK])

    rs.scrape_comments(limit=1)
