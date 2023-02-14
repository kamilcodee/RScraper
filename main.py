from rscraper import RScraperConfig, RScraper

if __name__ == '__main__':
    rsconfig = RScraperConfig(console_log=True, save_to_file=True)
    print(rsconfig.details)
    rs = RScraper(rsconfig)

    rs.scrape_reddits(limit=22)
