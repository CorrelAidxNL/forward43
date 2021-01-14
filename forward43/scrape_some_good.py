import json
import requests
from bs4 import BeautifulSoup
import pandas as pd

# create url's for ... overview pages
browse_url_base        = 'https://startsomegood.com/projects?page='
browse_pages = []

for page in range(15):
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
        if project_soup.find("div", class_="story") is None:
            description     = 'Description not available'
        else:   
            description     = project_soup.find("div", class_="story").text
        
        if project_soup.find("p", class_="sub-title") is None:
            city            = 'City not available'
            country         = 'Country not available'
            contact         = 'Contact not available'
        else:
            location        = project_soup.find("p", class_="sub-title").text.strip()
            city            = location.split(',')[0]
            country         = location  #.split(',')[1]
                                        # Note that country and contact are identical and messy
            contact         = location  #.split(',')[1]
        
        if project_soup.find('ul', class_="nav nav-pills categories") is None:
            innovation_type = 'Innovation type not available'
        else:
            innovation_type = project_soup.find('ul', class_="nav nav-pills categories").text
        
        good_observation    = {"Title":[title], "Description":[description], "Status":[status], "innovation_type":[innovation_type], "Country":[country], "City":[city], "Contact person/details":[contact], "Link":[link]}
        good_data.append(good_observation)

good_data_df = pd.DataFrame.from_records(good_data)

# export df to JSON
# good_data_df.to_json(r'...\good_stuff.json')
