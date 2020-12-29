import os

import json
import random
import time
import requests
from pathlib        import Path

from datetime       import datetime
from urllib.request import urlopen

from fp.fp          import FreeProxy

from spoof_params   import user_agent_list, accept_list


MAX_VALUE                  = 65536
KICKSTARTER_URL            = 'https://www.kickstarter.com/discover/advanced.json?'
KICKSTARTER_DEFAULT_PARAMS = ['sort=popularity']
ATTRIBUTES                 = ['rank', 'id', 'name', 'creator', 'goal', 'pledged',
                              'state', 'backers', 'launch_date', 'deadline', 'url']

def write_data_to_file(data, category):
    '''
    Write json data to file
    @data: dictionary
    @category: category id
    '''
    filepath = '../data/{}.json'.format(category)

    with open(filepath, 'w+') as f:
        json.dump(data, f)


def generate_url(category, page):
    '''
    Generates a URL to scrape from. It's necessary that category and page parameters are not None
    '''
    random_seed   = 'seed='   + str(random.randint(1, MAX_VALUE))
    random_woe_id = 'woe_id=' + str(random.randint(1, MAX_VALUE))
    get_params  = KICKSTARTER_DEFAULT_PARAMS + ['category_id={}'.format(category), 'page={}'.format(str(page)), random_seed, random_woe_id]
    return KICKSTARTER_URL + '&'.join(get_params)

def fetch_data(url, proxies):

    try:
        user_agent_ = random.choice(user_agent_list)
        accept_     = random.choice(accept_list)
        headers_    = {
            'User-Agent': user_agent_,
            'Accept': accept_,
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

        r = requests.get(url, headers=headers_, proxies=proxies)
        print(r.json()['origin'])
        if r.status_code != 200:
            print('*** http error ***')
            return ''

        data         = r.json()
        num_projects = len(data['projects'])
        return_data  = []

        for i in range(num_projects):

            # TODO: This should be handled better
            # TODO: Move this code
            # TODO: It should be able to handle other scenarios
            details = {
                'id'          : str(data['projects'][i]['id']),
                'rank'        : str(i + 1),
                'name'        : data['projects'][i]['name'],
                'creator'     : data['projects'][i]['creator']['name'],
                'goal'        : str(data['projects'][i]['goal']),
                'pledged'     : str(data['projects'][i]['pledged']),
                'state'       : data['projects'][i]['state'],
                'backers'     : str(data['projects'][i]['backers_count']),
                'launch_date' : time.strftime('%c', time.localtime(data['projects'][i]['launched_at'])),
                'deadline'    : time.strftime('%c', time.localtime(data['projects'][i]['deadline'])),
                'url'         : data['projects'][i]['urls']['web']['project'],
            }

            return_data.append(details)

        return return_data

    except Exception as e:
        print(e)

def main(category, page, proxy):

    url   = generate_url(category, page)
    data  = fetch_data(url, proxy)

    print('    URL: {}'.format(url))

    return data

def get_proxy():
    proxy = FreeProxy().get()
    print(proxy)

    if proxy.startswith('https'):
        type = 'https'
    else:
        type = 'http'
    proxy = {
        type : proxy
    }

    return proxy


if __name__ == '__main__':

    category_ids = [3, 272, 1]
    num_pages    = 12  # 12 entries per page

    for category in category_ids:

        print('Category: {}'.format(category))
        data  = []
        proxy = get_proxy()

        for page in range(1, num_pages + 1):
            print('    Page: {}'.format(page))

            data += (main(category, page, proxy))

        write_data_to_file(data, category)
