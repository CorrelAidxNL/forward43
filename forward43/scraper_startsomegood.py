from bs4     import BeautifulSoup

from scraper import ForwardScraper


class StartSomeGoodScraper(ForwardScraper):

    def __init__(self, num_pages):
        ForwardScraper.__init__(self)

        self.which_scraper = 'start_some_good'
        self.base_url      = 'https://startsomegood.com'

        self.num_pages     = num_pages

    def get_url(self, page_num):
        '''
        Generates a URL based on the page number
        '''
        return self.base_url + '/projects?page=' + str(page_num)

    def process_response(self, response):

        soup_overview = BeautifulSoup(response.content, "html.parser")
        projects      = soup_overview.find_all('a', class_="col-sm-6 col-md-4 project-tile project-tile-link")
        project_list  = []

        for project in projects:

            link           = self.base_url + project.get('href')
            project_resp   = self.get_response(link)
            project_parsed = BeautifulSoup(project_resp.content, 'html.parser')

            story          = project_parsed.find('p',  class_='story')
            category       = project_parsed.find('ul', class_="nav nav-pills categories")
            subtitle       = project_parsed.find("p",  class_="sub-title")

            if subtitle.contents is not None and len(subtitle.contents) > 2:
                city    = subtitle.contents[2].split(',')[0].strip()
                country = subtitle.contents[2].split(',')[-1].strip()
                contact = subtitle.contents[-1].strip()
            else: 
                city = country = contact = subtitle.text.strip()  # Fallback scenario

            project_list.append({
                'id'              : project.get('href')[1:],
                'title'           : project.find('h4').text,
                'description'     : story.text if story is not None else 'n.a.',
                'status'          : project.find('span', class_='pull-right closing-date').text,
                'innovation_type' : category.text if category is not None else 'n.a.',
                'country'         : country,
                'city'            : city,
                'contact'         : contact,
                'link'            : link
            })

        return project_list

    def scrape(self):
        ''' Main Scraper function '''
        for i in range(1, self.num_pages):

            try:
                url      = self.get_url(i)
                response = self.get_response(url)
                projects = self.process_response(response)

                self.write_to_file(projects, str(i), self.which_scraper)
            except Exception as e:
                print(e)


if __name__ == '__main__':

    scraper = StartSomeGoodScraper(num_pages=15)
    scraper.scrape()
