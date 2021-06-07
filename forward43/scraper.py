import json
import logging
import os
import random
import requests
import time

from fp.fp          import FreeProxy

from forward43.hparams        import user_agent_list, accept_list
from forward43.data.data_path import DATA_DIRECTORY


class ForwardScraper:
    ''' A common class for all the scrapers '''

    def __init__(self, which_scraper):
        # NOTE: At a later point, fetch this from a constants file
        self.attributes    = ['id', 'title', 'description', 'status', 'innovation_type', 'country', 'city', 'link']
        self.which_scraper = which_scraper

        # Init logger
        logging.basicConfig(
            format   = '[%(asctime)s] %(levelname)-8s %(message)s',
            filename = f'./logs/scraper_{which_scraper}-{int(time.time())}.log'
        )
        self.logger  = logging.getLogger('scraper')
        self.logger.setLevel(logging.DEBUG)

    def write_to_file(self, projects, filename):
        ''' Write a list of projects to file in the data directory '''
        filepath = os.path.join(DATA_DIRECTORY, f'forward_scraper_{self.which_scraper}-{filename}.json')

        self.logger.info(f'Writing to file: {filepath}')
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(projects, f, ensure_ascii=False, indent=4)

        self.logger.info('Data write completed')

    def get_url(self, *args, **kwargs):
        raise NotImplementedError()

    def get_proxy(self):
        ''' Get a proxy for spoofing '''
        proxy    = FreeProxy().get()
        if proxy.startswith('https'):
            type = 'https'
        else:
            type = 'http'
        proxy    = { type : proxy }

        return proxy

    def get_response(self, url, spoof=False):
        ''' A wrapper over requests.get with/without spoofing '''
        self.logger.info(f'Making a request to: {url}')

        if spoof:
            proxies_    = self.get_proxy()
            user_agent_ = random.choice(user_agent_list)
            accept_     = random.choice(accept_list)
            headers_    = {
                'User-Agent'                : user_agent_,
                'Accept'                    : accept_,
                'Accept-Language'           : 'en-US,en;q=0.5',
                'DNT'                       : '1',
                'Connection'                : 'keep-alive',
                'Upgrade-Insecure-Requests' : '1',
            }

            response    = requests.get(url, headers=headers_, proxies=proxies_)
        else:
            response    = requests.get(url)

        if response.status_code != 200:
            raise Exception(f'Request failed on URL: {url}')

        return response

    def process_response(self, response):
        raise NotImplementedError()
