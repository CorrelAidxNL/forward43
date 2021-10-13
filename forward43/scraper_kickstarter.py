import random

from forward43.scraper import ForwardScraper
from hparams import keywords

class KickstarterScraper(ForwardScraper):

    def __init__(self, keywords, num_pages):
        ForwardScraper.__init__(self, 'kickstarter')

        self.base_url           = 'https://www.kickstarter.com/discover/advanced.json?'
        self.default_url_params = ['sort=newest', 'woe_id=1']

        self.keywords           = keywords
        self.num_pages          = num_pages

    def get_search_term_url(self, keyword, page):
        '''
        Generates an URL to scrape from based on a keyword and a page number.
        It's necessary that page parameter is not None
        @page     : page number
        '''
        search_term = 'term=' + keyword.replace(' ', '+')
        random_seed = 'seed=' + str(random.randint(1, 65536))
        get_params = self.default_url_params + [random_seed, search_term, f"page={page}"]
        return self.base_url + '&'.join(get_params)

    def process_response(self, response):

        data         = response.json()
        num_projects = len(data['projects'])
        project_list = []

        for i in range(num_projects):
            project_list.append({
                'id'              : self.which_scraper + '_' + str(data['projects'][i].get('id', 'n.a.')),
                'title'           : data['projects'][i].get('name', 'n.a.'),
                'description'     : data['projects'][i].get('blurb', 'n.a.'),
                'status'          : data['projects'][i].get('state', 'n.a.'),
                'innovation_type' : data['projects'][i].get('category', {}).get('name', 'n.a.'),
                'country'         : data['projects'][i].get('country', 'n.a'),
                'city'            : data['projects'][i].get('location', {}).get('state', 'n.a.'),
                'contact'         : data['projects'][i].get('creator', {}).get('name', 'n.a.'),
                'link'            : data['projects'][i].get('urls', {}).get('web', {}).get('project', 'n.a.')
            })

        return project_list

    def scrape(self):
        ''' Main Scraper function '''
        for keyword in keywords:
            projects = []

            for page in range(1, self.num_pages + 1):
                self.logger.info(f'Processing search: {keyword} and page: {page}')

                try:
                    url       = self.get_search_term_url(keyword, page)
                    response  = self.get_response(url)
                    projects  = self.process_response(response)

                except Exception as e:
                    self.logger.exception('Failed to get projects from current page')

            self.write_to_file(projects, str(keyword))


if __name__ == '__main__':

    scraper = KickstarterScraper(keywords=keywords, num_pages=5)
    scraper.scrape()
