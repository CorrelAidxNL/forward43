import os

import json
import random
import time
import requests
from pathlib import Path

from datetime       import datetime
from urllib.request import urlopen


MAX_VALUE                  = 65536
KICKSTARTER_URL            = 'https://www.kickstarter.com/discover/advanced.json?'
KICKSTARTER_DEFAULT_PARAMS = ['sort=newest', 'woe_id=1']
ATTRIBUTES                 = ['name', 'creator', 'goal', 'pledged', 'state', 'backers', 'launch_date', 'deadline', 'url']


def write_data_to_file(data, category):
    '''
    Write json data to file
    @data     : dictionary
    @category : category id
    '''
    filepath = '../data/{}.json'.format(category)

    with open(filepath, 'w+') as f:
        json.dump(data, f)


def generate_url(category, page):
    '''
    Generates a URL to scrape from. It's necessary that category and page parameters are not None
    Args:
        @category : category id
        @page     : page number
    '''
    random_seed = 'seed=' + str(random.randint(1, MAX_VALUE))
    get_params  = KICKSTARTER_DEFAULT_PARAMS + [f"category_id={category}", f"page={page}", random_seed]
    return KICKSTARTER_URL + '&'.join(get_params)

def fetch_data(url):
    '''
    Scrape kickstarter based on the url. Returns a list of dicts, where each dict is a project
    '''
    try:
        r = requests.get(url)

        if r.status_code != 200:
            print(f'Http error,: {str(r.status_code)}')
            return ''

        data         = r.json()
        num_projects = len(data['projects'])
        return_data  = []

        for i in range(num_projects):

            details = { 'rank' : str(i + 1) }

            for att in ATTRIBUTES:
                details[att] = data['projects'][i].get(att, 'n.a.')

            if details['creator'] != 'n.a.':
                details['creator'] = details['creator'].get('name', 'n.a.')

            try:
                details['urls'] = details['urls']['web']['project']
            except:
                details['urls'] = 'n.a.'

            return_data.append(details)

        return return_data

    except Exception as e:
        print(e)


def main(category, page):
    '''
    Fetch kickstarter projects for a given category and page
    Args:
        @category : category id
        @page     : page number
    Return:
        data (list of dicts)
    '''
    url  = generate_url(str(category), str(page))
    data = fetch_data(url)
    print('    URL: {}'.format(url))
    return data


if __name__ == '__main__':

    category_ids = [3, 272, 1]
    num_pages    = 5  # 12 entries per page

    for category in category_ids:

        print('Category: {}'.format(category))
        data = []

        for page in range(1, num_pages + 1):
            print('    Page: {}'.format(page))

            data += (main(category, page))

        write_data_to_file(data, category)
