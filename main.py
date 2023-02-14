from rscraper import RScraperConfig, RScraper
from rscraper.key.RedditKey import RedditKey

if __name__ == '__main__':
    rsconfig = RScraperConfig(console_log=True, save_to_file=True)
    rs = RScraper(rsconfig)

    rs.scrape_reddits(limit=22)
