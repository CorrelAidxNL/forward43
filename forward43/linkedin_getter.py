# -*- coding: utf-8 -*-
"""
This module retrieves data from the LinkedIn about section.

Created on Wed Apr 21 21:35:48 2021
@author: Marijke Thijssen
"""
# %%   Import packages and settings
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

pd.set_option('display.max_columns', None)

SCROLL_PAUSE_TIME = 5


# %%   Functions
def login(browser, username, password):
    """ Login to LinkedIn. """
    browser.find_element_by_id('username').send_keys(username)
    browser.find_element_by_id('password').send_keys(password)
    browser.find_element_by_id('password').send_keys(Keys.RETURN)


def scroll_full_page(browser, pause_time):
    """ Scroll to the bottom of the page. This loads every element. """
    last_height = browser.execute_script('return document.body.scrollHeight')
    
    for i in range(5):
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(pause_time)
        new_height = browser.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height


def scrape_about(browser, main_page):
    """ Scrape the about page for a long description. """
    link = 'http://' + main_page + '/about'
    browser.get(link)
    
    scroll_full_page(browser, pause_time=SCROLL_PAUSE_TIME)
    src = browser.page_source
    soup = BeautifulSoup(src, 'lxml')
    
    try:
        about_element = soup.find('div', {'class': 'mb6'})
        about = about_element.find('p').get_text().strip()
    except:
        # Sites can be automatically created by LinkedIn. These do not always
        # have a long description. 
        print(f'The page {link} was automatically created and has no about information.')
        about = ''
        
    return about


# %%   Read in company data
interesting_industries = ['civic & social organization', 'e-learning', 
                          'education management', 'environmental services',
                          'non-profit organization management', 
                          'professional training & coaching',
                          'think tanks', 'renewables & environment']

path_company = '..\\Data\\free_company_dataset_pipe.csv'
chunksize = 10 ** 6
company_df = []
for i, chunk in enumerate(pd.read_csv(path_company, engine='python', sep='|', 
                                          quoting=3, chunksize=chunksize,
                                          usecols=['country', 'founded', 'id', 'industry',
                                                  'linkedin_url', 'locality', 'name',
                                                  'region', 'size', 'website'],
                                          header=0, index_col=False)):
    temp_df = chunk[chunk['industry'].isin(interesting_industries)]
    company_df.append(temp_df)
    
company_df = pd.concat(company_df, ignore_index=True)
company_df = company_df.replace('""', np.nan)
print(f'Set contains {len(company_df)} companies, ' \
      ' of which {len(company_df[~company_df["linkedin_url"].isna()])} companies have a LinkedIn URL.')


# %%   Start browser and login to LinkedIn
path_driver = '..\\Data\\chromedriver_win32\\chromedriver.exe' # from: https://sites.google.com/chromium.org/driver/
browser = webdriver.Chrome(executable_path=path_driver)
browser.get('https://www.linkedin.com/uas/login')
user = open('..\\user.txt').readlines()
login(browser, user[0], user[1])

    # %%   Scrape about information
company_df['about'] = company_df.apply(lambda x: scrape_about(browser, x['linkedin_url']), axis=1)
browser.close()

# %%   Create ES document 
    # %%   Push to Elasticsearch