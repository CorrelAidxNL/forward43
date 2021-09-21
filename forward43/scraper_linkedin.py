# -*- coding: utf-8 -*-
"""
LinkedIn scraper

Created on Sun Jul  4 15:32:13 2021
@author: Marijke Thijssen
"""
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import random
from selenium import webdriver
import time

from forward43 import forward43
from forward43.scraper import ForwardScraper


class LinkedInScraper(ForwardScraper):

    def __init__(self):
        ForwardScraper.__init__(self, 'LinkedIn')
        
        self.driver = 'data/chromedriver_linux64/chromedriver.exe' # from: https://sites.google.com/chromium.org/driver/

        self.login_page        = 'https://www.linkedin.com/uas/login'
        self.user              = open('../user.txt').readlines()  # Replace with other credentials: https://developer.linkedin.com/support/faq
        self.scroll_pause_time = 5
        
        self.company_file           = 'data/free_company_dataset_pipe.csv'
        self.interesting_industries = ['civic & social organization', 'e-learning', 
                                       'education management', 'environmental services',
                                       'non-profit organization management', 
                                       'professional training & coaching',
                                       'think tanks', 'renewables & environment']
        self.chunksize = 10 ** 6
        
    
    def set_browser(self):
        """ Activate the browser. """
        self.browser = webdriver.Chrome(executable_path=self.driver)
        self.browser.get(self.login_page)
        
        
    def get_helper_info(self):
        """ Get the content from the helper file that contains information on companies. """
        company_df = []
        for i, chunk in enumerate(pd.read_csv(self.company_file, engine='python', sep='|', 
                                                  quoting=3, chunksize=self.chunksize,
                                                  usecols=['country', 'founded', 'id', 'industry',
                                                          'linkedin_url', 'locality', 'name',
                                                          'region', 'size', 'website'],
                                                  header=0, index_col=False)):
            temp_df = chunk[chunk['industry'].isin(self.interesting_industries)]
            company_df.append(temp_df)
            
        company_df = pd.concat(company_df, ignore_index=True)
        company_df = company_df.replace('""', np.nan)
        self.logger.info(f'Set contains {len(company_df)} companies of interest, ' \
                         f' of which {len(company_df[~company_df["linkedin_url"].isna()])} ' \
                          'companies have a LinkedIn URL.')   
        return company_df
    
    
    def login(self):
        """ Login to LinkedIn. """
        self.browser.find_element_by_id('username').send_keys(self.user[0])
        self.browser.find_element_by_id('password').send_keys(self.user[1])
        

    def scroll_full_page(self):
        """ Scroll to the bottom of the page. This loads every element. """
        last_height = self.browser.execute_script('return document.body.scrollHeight')
        
        for i in range(5):
            self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(self.scroll_pause_time)
            new_height = self.browser.execute_script('return document.body.scrollHeight')
            if new_height == last_height:
                break
            last_height = new_height
    
    
    def scrape_about(self, main_page):
        """ Scrape the about page for a long description. """
        link = 'http://' + main_page + '/about'
        self.browser.get(link)
        
        self.scroll_full_page()
        src = self.browser.page_source
        soup = BeautifulSoup(src, 'lxml')
        
        try:
            about_element = soup.find('div', {'class': 'mb6'})
            about = about_element.find('p').get_text().strip()
        except:
            # Sites can be automatically created by LinkedIn. These do not always have a long description. 
            self.logger.info(f'The page {link} was automatically created and has no about information.')
            about = ''
            
        return about
    
    
    def get_url(self):
        pass
    
    
    def get_response(self, company_df):
        """ Get information. """
        company_df['about'] = company_df.apply(lambda x: self.scrape_about(x['linkedin_url']), 
                                               axis=1)
        return company_df
              
    
    def process_response(self, response):
        companies_df = response[['id', 'name', 'about', 'size', 'industry',
                                 'country', 'region', 'locality', 'website']]
        companies_df = companies_df.replace('', np.nan).fillna('n.a.')
        companies_dict = companies_df.to_dict(orient='records')

        return companies_dict
        
        
    def scrape(self):
        companies = self.get_helper_info()
        self.set_browser()
        self.login()
        response = self.get_response(companies)
        self.browser.close() 
        companies_with_info = self.process_response(response)
        self.write_to_file(companies_with_info, str(random.randint(1, 1000000)))


if __name__ == '__main__':
    scraper = LinkedInScraper()
    scraper.scrape()
