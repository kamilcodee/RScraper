from rscraper import Config
from rscraper import SubmissionScraper
from rscraper import SubredditScraper

if __name__ == '__main__':
    config = Config()
    config.data_dir = f'../{config.data_dir}'

    subredditScraper = SubredditScraper(config)
    subredditScraper.limit = 2

    subredditScraper.scrape()
    # pprint(subredditScraper.subreddits)

    subredditScraper.save_data()

    submissionScraper = SubmissionScraper(config)
    submissionScraper.limit = 55

    submissionScraper.scrape()
