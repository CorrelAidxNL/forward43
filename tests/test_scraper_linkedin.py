# -*- coding: utf-8 -*-
"""
Tests for LinkedIn getter. 

Created on Sun May 30 20:30:20 2021
@author: Marijke Thijssen
"""
# %%   Import packages and settings
import unittest
unittest.TestLoader.sortTestMethodsUsing = None
from selenium import webdriver

from forward43 import forward43
from forward43 import scraper_linkedin
  

# %%   Functions
class TestLinkedInScraper(unittest.TestCase):
  
    def setUp(self):
        self.scraper = scraper_linkedin.LinkedInScraper()
    
    def test_GoToLinkedin(self):
        self.browser = webdriver.Chrome(executable_path='data\\chromedriver_win32\\chromedriver.exe')
        self.browser.get('https://www.linkedin.com/uas/login')
        self.assertIn('LinkedIn', self.browser.title)
    
    
    def test_FindLoginFields(self):
        self.browser = webdriver.Chrome(executable_path='data\\chromedriver_win32\\chromedriver.exe')
        self.browser.get('https://www.linkedin.com/uas/login')
        try:
            self.browser.find_element_by_id('username')
            self.browser.find_element_by_id('password')
            elements_exist = True
        except:
            elements_exist = False
        self.assertTrue(elements_exist)
        
  
    def tearDown(self):
        self.browser.close()
  
    
# %%   If-Main
if __name__ == '__main__':
    unittest.main()