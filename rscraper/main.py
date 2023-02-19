from pprint import pprint

from rscraper import SubredditScraper
from rscraper import Config

if __name__ == '__main__':
    config = Config()
    config.data_dir = f'../{config.data_dir}'

    subredditScraper = SubredditScraper(config)

    subredditScraper.limit = 2

    subredditScraper.scrape()
    # pprint(subredditScraper.subreddits)

    subredditScraper.save_data()
