import json
import requests
from bs4 import BeautifulSoup
import pandas as pd

PROJECT_URL_BASE        = 'https://startsomegood.com'
BROWSE_URL_BASE         = 'https://startsomegood.com/projects?page='


def scrape_some_good(n_pages = 15):

    # create url's for ... overview pages
    browse_pages = []

    for page in range(1, n_pages):
        browse_pages.append(BROWSE_URL_BASE + str(page))

    # create dataframe to store data
    good_data               = []

    # loop over the overview pages to find the project tiles
    for url in browse_pages:
        try:
            response_overview   = requests.get(url, timeout = 5)
            soup_overview       = BeautifulSoup(response_overview.content, "html.parser")

            projects            = soup_overview.find_all('a', class_="col-sm-6 col-md-4 project-tile project-tile-link")
        
            # loop over the tiles to find the data needed
            for project in projects:
                # Get available data from project tile on overview page
                title                   = project.find('h4').text
                status                  = project.find('span', class_='pull-right closing-date').text
                link                    = PROJECT_URL_BASE + project.get('href')
            
                # Scrape soup from project page
                project_response        = requests.get(link, timeout = 5)
                project_soup            = BeautifulSoup(project_response.content, "html.parser")
            
                # Get remaining data from project-page soup
                row = defaultdict(lambda: 'n.a.') # if row[x] value is non existent, it returns n.a.
            
                story = project_soup.find('p', class_='story')
                if story is not None:
                    row['description']  = story.text
                        
                subtitle = project_soup.find("p", class_="sub-title")
                if subtitle is not None:
                    row['location']     = subtitle.text.strip()
                    row['city']         = row['location'].split(',')[0]
                    row['country']      = row['location']#.split(',')[1]
                    row['contact']      = row['location']#.split(',')[1]
                                                 # Note that country and contact are identical and messy
            
                category = project_soup.find('ul', class_="nav nav-pills categories")
                if category is not None:
                    row['innovation_type'] = category.text
            
                good_observation        = {"Title":[title], "Description":[description], "Status":[status], "innovation_type":[innovation_type], "Country":[country], "City":[city], "Contact person/details":[contact], "Link":[link]}
                good_data.append(good_observation)
        except:
            pass

    good_data_df = pd.DataFrame.from_records(good_data)
    return good_data_df


# export df to JSON
# good_data_df.to_json(r'...\good_stuff.json')
