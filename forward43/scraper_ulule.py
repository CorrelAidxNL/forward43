import math
import requests

from scraper import ForwardScraper


class UluleScraper(ForwardScraper):

    def __init__(self):
        ForwardScraper.__init__(self)

        self.which_scraper = 'ulule'
        self.base_url      = 'https://api.ulule.com/v1/'
        self.projects_ref  = 'search/projects/'
        self.query         = ['status:currently']

    def _get_page(self, url, query, limit, page=1):
        ''' Retrieve a paginated response. '''
        response = requests.get(url, params={'q': '+'.join(query), 'offset': page * limit})

        if response.status_code != 200:
            raise Exception(f'Unsuccessful GET on {url}: {response.status_code}')

        return response
    
    def get_url(self, project_id):
        return self.base_url + f'projects/{project_id}'

    def process_response(self, response):
        response    = response.json()

        # Get title and description
        title       = response.get('name_en',        '')
        description = response.get('description_en', '')
        for k, v in response.items():
            if k.startswith('description') and description != '':
                if response[k] != '':
                    description = response[k]
            if k.startswith('name') and title != '':
                if response[k] != '':
                    title       = response[k]

        details     = {
            'id'              : response.get('id',             'n.a.'),
            'title'           : title,
            'description'     : description,
            'status'          : response.get('status',         'n.a.'),
            'innovation_type' : response.get('type',           'n.a.'),
            'country'         : response.get('country',        'n.a.'),
            'city'            : response.get('owner', {}).get('location', 'n.a.'),
            'contact'         : response.get('owner', {}).get('name',     'n.a.'),
            'link'            : response.get('absolute_url',   'n.a.'),
        }

        return details

    def scrape(self):
        
        # Get initial response to assess number of projects
        page_response = self._get_page(self.base_url + self.projects_ref, query=self.query, limit=0)
        
        data          = page_response.json()
        meta          = data['meta']
        n_projects    = meta['total_count']
        limit         = meta['limit']
        n_pages       = math.ceil(n_projects / limit)

        # Get list of IDs
        id_list       = []
        for n in range(n_pages):
            page      = self._get_page(self.base_url + self.projects_ref, query=self.query, limit=limit, page=n).json()
            projects  = page['projects']
            for p in projects:
                id_list.append(p['id'])
    
        # Get projects with criteria
        project_list  = []
        for project_id in id_list:

            try:
                url       = self.get_url(project_id)
                response  = self.get_response(url)
                project   = self.process_response(response)

                project_list.append(project)
            except Exception as e:
                print(e)

        self.write_to_file(projects, 'projects', self.which_scraper)


if __name__ == '__main__':

    scraper = UluleScraper()
    scraper.scrape()
