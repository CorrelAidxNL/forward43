# Entry point to the script
# This function will scrape from the relevant scrapers
# and update the Elasticsearch database
# 
# Example usage: 
#   `python -m forward43.forward43 --scrapers kickstarter ulule --num_pages 10 --update_elastic_db`

import argparse
import os


def main(scrapers, num_pages, update_elastic_db, host, port):

    if 'kickstarter' in scrapers:
        from forward43.hparams             import keywords
        from forward43.scraper_kickstarter import KickstarterScraper
        
        scraper = KickstarterScraper(keywords=keywords, num_pages=num_pages)
        scraper.scrape()

    if 'startsomegood' in scrapers:
        from forward43.scraper_startsomegood import StartSomeGoodScraper
        scraper = StartSomeGoodScraper(num_pages=num_pages)
        scraper.scraper()

    if 'ulule' in scrapers:
        from forward43.scraper_ulule import UluleScraper
        scraper = UluleScraper()
        scraper.scrape()

    if update_elastic_db:
        from forward43.es_ingest import injest_data_to_es
        injest_data_to_es(host=host, port=port, user=user, secret=secret)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--scrapers',  nargs='+', help='List of scrapers: [kickstarter, startsomegood, ulule]', default=["kickstarter", "startsomegood", "ulule"])
    parser.add_argument('--num_pages', type=int,  help='Number of pages to scrape', required=False, default=10)

    parser.add_argument('--update_elastic_db', action='store_true', help='Update Elastic DB')
    parser.add_argument('--host',   type=str, help='Elastic DB host',   required=False, default='localhost')
    parser.add_argument('--port',   type=int, help='Elastic DB port',   required=False, default=9200)
    parser.add_argument('--user',   type=str, help='Elastic DB user',   required=False)
    parser.add_argument('--secret', type=str, help='Elastic DB secret', required=False)

    args = parser.parse_args()

    main(**vars(args))
