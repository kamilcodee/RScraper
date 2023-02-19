from rscraper import SubredditScraper
from rscraper import Config

if __name__ == '__main__':
    config = Config()

    subredditScraper = SubredditScraper(config)
    subredditScraper.limit = 2

    subredditScraper.scrape()
