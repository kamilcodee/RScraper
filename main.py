from rscraper import RScraperConfig, RScraper
from rscraper import RedditKey

if __name__ == '__main__':
    rsconfig = RScraperConfig(console_log=True, save_to_file=True)
    rs = RScraper(rsconfig)

    rs.scrape_reddits(limit=22, keys=[RedditKey.ID, RedditKey.NAME])
