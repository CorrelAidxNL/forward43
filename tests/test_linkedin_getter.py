# -*- coding: utf-8 -*-
"""
Tests for LinkedIn getter. 

Created on Sun May 30 20:30:20 2021
@author: Marijke Thijssen
"""
# %%   Import packages and settings
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
  

# %%   Functions
class LinkedInSearch(unittest.TestCase):
  
    def setUp(self):
        self.browser = webdriver.Chrome(executable_path='..\\Data\\chromedriver_win32\\chromedriver.exe')


    def test_load_linkedin(self):
        """ Test if connection with LinkedIn can be made. """
        browser = self.browser
        browser.get('https://www.linkedin.com/uas/login')
          
        # Assertion to confirm if title has keyword LinkedIn in it
        self.assertIn('LinkedIn', browser.title)
        
  
    def tearDown(self):
        self.browser.close()
  
    
# %%   If-Main
if __name__ == '__main__':
    unittest.main()