import random

from scraper import ForwardScraper
from hparams import keywords



class KickstarterScraper(ForwardScraper):

    def __init__(self, category_ids, num_pages):
        ForwardScraper.__init__(self, 'kickstarter')

        self.base_url           = 'https://www.kickstarter.com/discover/advanced.json?'
        self.default_url_params = ['sort=newest', 'woe_id=1']

        self.category_ids       = category_ids
        self.num_pages          = num_pages


    def get_url(self, category, page):
        '''
        Generates a URL to scrape from. It's necessary that category and page parameters are not None
        @category : category id
        @page     : page number
        '''
        
        ## I inserted a for loop over the keywords to create a list of urls to scrape below that include the search terms we want to use
        url_term_list = []
        
        for term in keywords:
            search_term = 'term=' + term.replace(' ', '+')
            random_seed = 'seed=' + str(random.randint(1, 65536))
            get_params  = self.default_url_params + [f"category_id={category}", f"page={page}", random_seed, search_term]   # added a keyword parameter to the url
            url         = self.base_url + '&'.join(get_params)
            url_term_list.append(url)
            
        return url_term_list

    def process_response(self, response):

        data         = response.json()
        num_projects = len(data['projects'])
        project_list = []

        for i in range(num_projects):
            project_list.append({
                'id'              : data['projects'][i].get('id', 'n.a.'),
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
        for category in self.category_ids:
            projects = []

            for page in range(1, self.num_pages + 1):
                self.logger.info(f'Processing category: {category} and page: {page}')

                # Now, instead of trying a single url, it tries to loop over the list created above
                try:
                    url_term_list       = self.get_url(category, page)
                    
                    print(url_term_list)
                    
                    for url in url_term_list:
                        response  = self.get_response(url)
                        projects  = self.process_response(response)
                    return projects
                    
                except Exception as e:
                    self.logger.exception('Failed to get projects from current page')

            self.write_to_file(projects, str(category))
            

if __name__ == '__main__':

    scraper = KickstarterScraper(category_ids=[3, 272, 1], num_pages=5)
    scraper.scrape()
