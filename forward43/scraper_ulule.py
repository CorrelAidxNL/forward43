# -*- coding: utf-8 -*-
"""
This module uses the API for the platform Ulule to extract data on projects.

Created on Wed Dec 16 22:06:55 2020
@author: Marijke Thijssen
"""
# %%   Import packages
import json
import math
# import pandas as pd
import requests

from support import timer

# %%   Set variables
URL = 'https://api.ulule.com/v1/'
ENDPOINT_PROJECTS = 'search/projects/'
QUERY = ['status:currently']  
CRITERIA = ['id', 'name_en', 'description_en', 'status', 'type', 'country', 'location', 'absolute_url']

# - id
# Title - name
# Description - description
# Status - status
# Innovation type - type
# Country - country
# City - location
# Link - absolute_url

# The description and name are only available if you get the project on ID. 
# You also have to know the language you want the description in because the fields
# have the country code appended to it, eg. decription_de, description_en.

# Type: 1 (presale) or 2 (project)

# Country is given as a two-letter ISO code

# %%   Functions
# @timer
def get_object(url):
    """ Retrieve a response. """
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f'Unsuccessful GET on {url}: {response.status_code}')
    
    return response


# @timer
def get_page(url, query, limit, page=1):
    """ Retrieve a paginated response. """
    response = requests.get(url, params={'q': '+'.join(query), 'offset': page * limit})
    if response.status_code != 200:
        raise Exception(f'Unsuccessful GET on {url}: {response.status_code}')
    
    return response


def write_to_file(projects, file_name):
    """ Write a list of projects to file. """
    # project_df = pd.DataFrame(projects)
    # project_df.to_csv(f'{file_name}.csv', index=False)
    
    with open(f'{file_name}.json', 'w', encoding='utf-8') as dest:
        json.dump(projects, dest, ensure_ascii=False, indent=4)
    
    print(f'Wrote data to file: {file_name}.csv')


@timer
def main():
    # Get initial response to assess number of projects
    response = get_page(URL + ENDPOINT_PROJECTS, QUERY, limit=0)

    data = response.json()
    meta = data['meta']
    n_projects = meta['total_count']
    limit = meta['limit']
    n_pages = math.ceil(n_projects / limit)
    
    #   Get list of IDs
    id_list = []
    for n in range(n_pages):
        page = get_page(URL + ENDPOINT_PROJECTS, QUERY, limit, page=n).json()
        projects = page['projects']
        for p in projects:
            id_list.append(p['id'])
    
    #   Get projects with criteria
    project_list = []
    for project_id in id_list:
        project = get_object(URL + f'projects/{project_id}').json()
        project = {k: project[k] for c in CRITERIA for k in project.keys() 
                   if k == c}
        details = {
            'id': project.get('id', 'no ID given'),
            'title': project.get('name_en', 'no English title given'),
            'description': project.get('description_en', 'no English description given'),
            'status': project.get('status', 'no status given'),
            'innovation_type': project.get('type', 'no type given'),
            'country': project.get('country', 'no country given'),
            'city': project.get('city', 'no location given'),
            'link': project.get('absolute_url', 'no link given')}
        project_list.append(details)
        
    return json.dumps(project_list)
        
    
    # #   Write to file
    # write_to_file(project_list, file_name='projects_ulule')


# %%   If-Main
if __name__ == '__main__':
    projects = main()

