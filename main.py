from rscraper import RScraperConfig, RScraper
from rscraper import SubredditKey, SubmissionKey
from rscraper.RSLogger import RSLogLevel

if __name__ == '__main__':
    rsconfig = RScraperConfig(console_log=True, save_to_file=True)
    rsconfig.target_log_level = RSLogLevel.DEBUG  # override loglevel for debugging purposes

    rs = RScraper(rsconfig)

    reddits: dict
    reddits = rs.scrape_subreddits(limit=2, keys=[SubredditKey.ID, SubredditKey.NAME, SubredditKey.URL],
                                   return_data=True)

    rs.scrape_submissions(limit=2, keys=[SubmissionKey.ID, SubmissionKey.NAME, SubmissionKey.URL])
