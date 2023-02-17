from rscraper import RScraperConfig, RScraper
from rscraper import RedditKey

if __name__ == '__main__':
    rsconfig = RScraperConfig(console_log=True, save_to_file=True)
    rs = RScraper(rsconfig)

    reddits: dict
    reddits = rs.scrape_reddits(limit=22, keys=[RedditKey.ID, RedditKey.NAME, RedditKey.URL], return_data=True)

    rs.scrape_submissions()
