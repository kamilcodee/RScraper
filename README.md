# rscraper
Basic reddit scraper for publicly available data. Imitates the user "scrolling" down the pages and retrieving all
available data , until there is nothing to retrieve.

# How To
1. Config
```
from rscraper import RScraperConfig

rsconfig = RScraperConfig(console_log=True, save_to_file=True)
```
- You can modify the config, for example to change log level:
  ```
    rsconfig.target_log_level = RSLogLevel.DEBUG  # override loglevel for debugging purposes
    rsconfig.ua_generator = lambda: 'ABC'  # own generation strategy for useragent
  ```
  
UserAgent generator defaults to using fake_useragent if not overriden
2. Scraper instance
```
rs = RScraper(rsconfig)
```
3. Scrape submissions
```
reddits = rs.scrape_subreddits(limit=2, keys=[SubredditKey.ID, SubredditKey.NAME, SubredditKey.URL],
                                   return_data=True)
```
                                   
params:
- limit - how many subreddits to fetch, can be None for all **[int / None]**
- keys - list of keys(attributes) of a subreddit, that should be fetched, **[SubredditKey]**
```
from rscraper import SubredditKey
```
- return_data - should you want to retrieve the subreddits (on average there are about 4300 subreddits - can be fairly memory intensive) **[True / False]**

4. By default, subreddit data will be saved in **'./data/subreddits.json'** file
5. Scrape submissions
```
rs.scrape_submissions(limit=2, keys=[SubmissionKey.ID, SubmissionKey.NAME, SubmissionKey.URL])
```

params:
- limit - how many submissions per subreddit to fetch, can be None for all **[int / None]**
- keys - list of keys(attributes) of a submission, that should be fetched, **[SubmissionKey]**
```****
from rscraper import SubmissionKey
```
- there is NO return_data option as the amount of data now grows exponentially, data is saved to files (**.json**)

6. By default, submission data will be saved in **'./data/submissions/subreddit.json'**, where **subreddit** is the subreddit name


# Environment
Developed and tested using Python 3.11, Windows 10 Home, (M1 Pro) macOS 13.2.1 (Ventura)
## Requirements:
~= means compatible version
- requests~=2.28.2 (tested with 2.28.2)
- fake-useragent~=1.1.1 (tested with 1.1.1) [#TODO2 OPTIONAL - can provide your own UserAgent generation strategy]


# TODO
[TODOx] is a pointed to easier find in code
- multiprocessing / threading to speed up [TODO1]
- add metrics (time taken, etc) [TODO4]
- general error handling [TODO5]
- comment scraping [TODO6]