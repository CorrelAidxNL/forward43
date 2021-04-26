import json
import os
import random
import requests

from hparams        import user_agent_list, accept_list
from data.data_path import DATA_DIRECTORY


class ForwardScraper:
    ''' A common class for all the scrapers '''

    def __init__(self):
        # NOTE: At a later point, fetch this from a constants file
        self.attributes = ['id', 'title', 'description', 'status', 'innovation_type', 'country', 'city', 'link']

    def write_to_file(self, projects, filename, which_scraper):
        ''' Write a list of projects to file in the data directory '''
        filepath = os.path.join(DATA_DIRECTORY, f'{which_scraper}-{filename}.json')

        print(f'Writing to file: {filepath}')
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(projects, f, ensure_ascii=False, indent=4)

        print(f'Data write completed')

    def get_url(self, *args, **kwargs):
        raise NotImplementedError()

    def get_proxy(self):
        ''' Get a proxy for spoofing '''
        from fp.fp import FreeProxy

        proxy    = FreeProxy().get()
        if proxy.startswith('https'):
            type = 'https'
        else:
            type = 'http'
        proxy    = { type : proxy }

        return proxy

    def get_response(self, url, spoof=False):
        ''' A wrapper over requests.get with/without spoofing '''
        print(f'    url: {url}')

        if spoof:
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
            user_agent_ = random.choice(user_agent_list)
            accept_     = random.choice(accept_list)
            proxies_    = self.get_proxy()

            response    = requests.get(url, headers=headers_, proxies=proxies_)
        else:
            response    = requests.get(url)

        if response.status_code != 200:
            raise Exception(f'Request failed on URL: {url}')

        return response

    def process_response(self, response):
        raise NotImplementedError()
