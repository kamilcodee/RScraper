from rscraper import RScraperConfig, RScraper
from rscraper import RedditKey
from rscraper.RSLogger import RSLogLevel

if __name__ == '__main__':
    rsconfig = RScraperConfig(console_log=True, save_to_file=True)
    rsconfig.target_log_level = RSLogLevel.DEBUG  # override loglevel for debugging purposes

    rs = RScraper(rsconfig)

    reddits: dict
    reddits = rs.scrape_reddits(limit=1, keys=[RedditKey.ID, RedditKey.NAME, RedditKey.URL], return_data=True)

    rs.scrape_submissions(limit=234)
