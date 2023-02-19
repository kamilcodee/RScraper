# rscraper

Basic reddit scraper for publicly available data. Imitates the user "scrolling" down the pages and retrieving all
available data, until there is nothing to retrieve.

Can be used to scrape **subreddits** and **submissions**.
For comment scraping use **PRAW**.

# How To

**1. Config**

```
from rscraper import Config
```

You can change the properties:

```
config = Config()
config.data_dir = f'../{config.data_dir}'
```

By default, fake_useragent will be used to generate the useragent, you can change it by providing a different callable
or string

```
def get_user_agent():
  return expected_val

self.config.user_agent = get_user_agent
```

**2. SubredditScraper instance**

```
subredditScraper = SubredditScraper(config)
```

Limit can be configured as such:

```
subredditScraper.limit = 2
```

**3. Scrape subreddits**

```
subredditScraper.scrape()
```

**4. Save the data**

```
subredditScraper.save_data()
```

**5. SubmissionScraper instance**

```
submissionScraper = SubmissionScraper(config)
```

Limit of submissions per reddit can be configured similarly to SubredditScraper

**6. Scrape submissions** (subreddits are retrieved from the subreddit.json file)

```
submissionScraper.scrape()
```

Note: submission scraper saves the data automatically (due to the exponentially growing size)

By default, it will be saved to **./data/submissions/SUBREDDIT.json** file, where **SUBREDDIT** is the subreddit name

# Environment

Developed and tested using

- Python 3.11
    - Windows 10 Home
    - macOS 13.2.1 (M1 Pro)

## Requirements:

- To install the requirements use **pip install -r requirements.txt**

~= means compatible version

== strong equal

- requests~=2.28.2 (tested with 2.28.2)
- fake-useragent~=1.1.1 (tested with 1.1.1)

# FYI
The size of data fetched if not setting limits is quite large.
On average there are about 4300 subreddits that you can scroll through
Each one has an average of 1000 submissions to scroll through

Fetching all the data for 284 subreddits (6% of total) takes up about 2GB of disk space
