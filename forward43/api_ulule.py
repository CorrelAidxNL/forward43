# -*- coding: utf-8 -*-
"""
This module uses the API for the platform Ulule to extract data on projects.

Created on Wed Dec 16 22:06:55 2020
@author: Marijke Thijssen
"""
# %%   Import packages
import requests

# %%   Set variables
criteria = ['id', 'name', 'description', 'status', 'type', 'country', 'location', 'absolute_url']

# - id
# Title - name
# Description - description
# Status - status
# Innovation type - type
# Country - country (as two-letter ISO code)
# City - location
# Link - absolute_url


# %%   Functions



def main():
    pass


# %%   If-Main
if __name__ == '__main__':
    # main()
    url = 'https://api.ulule.com/v1/'
    projects = 'search/projects/'
    query = 'status=all'

    response = requests.get(url + projects, params={'q': query})
    if response.status_code != 200:
        raise Exception('GET {}'.format(response.status_code))
    # PAY ATTENTION: The response is paginated

    data = response.json()

    # TODO: keep only criteria fields
    # TODO: save to file

