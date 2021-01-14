import json
import requests
from bs4 import BeautifulSoup
import pandas as pd

# create url's for ... overview pages
browse_url_base        = 'https://startsomegood.com/projects?page='
browse_pages = []

for page in range(3):
    browse_pages.append(browse_url_base + str(page))

# create dataframe to store data
column_names            = ["Title", "Description", "Status", "innovation_type", "Country", "City", "Contact person/details", "Link"]
good_data               = []

# loop over the overview pages to find the project tiles
project_url_base        = 'https://startsomegood.com'

for URL in browse_pages:
    RESPONSE_OVERVIEW = requests.get(URL, timeout = 5)
    SOUP_OVERVIEW     = BeautifulSoup(RESPONSE_OVERVIEW.content, "html.parser")

    PROJECTS = SOUP_OVERVIEW.find_all('a', class_="col-sm-6 col-md-4 project-tile project-tile-link")
    
    # loop over the tiles to find the data needed
    for project in PROJECTS:
        # Get available data from project tile on overview page
        title               = project.find('h4').text
        status              = project.find('span', class_='pull-right closing-date').text
        link                = project_url_base + project.get('href')
        
        # Scrape soup from project page
        project_response    = requests.get(link, timeout = 5)
        project_soup        = BeautifulSoup(project_response.content, "html.parser")
        
        # Get remaining data from project-page soup
        description         = project_soup.find("div", class_="story").text
                                        # AttributeError: 'NoneType' object has no attribute 'text'
        location            = project_soup.find("p", class_="sub-title").text.strip()
        city                = location.split(',')[0]
        country             = location  #.split(',')[1]
                                        # Note that Country and Contact, if working, are identical and messy
        contact             = location  #.split(',')[1]
        innovation_type     = project_soup.find('ul', class_="nav nav-pills categories").text
        
        good_observation    = {"Title":[title], "Description":[description], "Status":[status], "innovation_type":[innovation_type], "Country":[country], "City":[city], "Contact person/details":[contact], "Link":[link]}
        good_data.append(good_observation)

good_data_df = pd.DataFrame.from_records(good_data)

# export df to JSON
# good_data_df.to_json(r'...\good_stuff.json')
