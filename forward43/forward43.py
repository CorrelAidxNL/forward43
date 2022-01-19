import argparse
import os


def main(scrapers, num_pages, update_elastic_db):

    if 'kickstarter' in scrapers:
        from forward43.hparams             import keywords
        from forward43.scraper_kickstarter import KickstarterScraper
        
        scraper = KickstarterScraper(keywords=keywords, num_pages=num_pages)
        scraper.scrape()

    if 'start_some_good' in scrapers:
        from forward43.scraper_startsomegood import StartSomeGoodScraper
        scraper = StartSomeGoodScraper(num_pages=num_pages)
        scraper.scraper()

    if 'ulule' in scrapers:
        from forward43.scraper_ulule import UluleScraper
        scraper = UluleScraper()
        scraper.scrape()

    if update_elastic_db:
        pass


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--scrapers', nargs='+', help='List of scrapers: [kickstarter, start_some_good, ulule]', required=True)
    parser.add_argument('--num_pages', type=int, help='Number of pages to scrape', required=False, default=1)
    parser.add_argument('--update_elastic_db', action='store_true', help='Update Elastic DB')

    args = parser.parse_args()

    main(**vars(args))
