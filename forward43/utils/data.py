import os
import json


def create_bulk_actions(index, data, source):
    '''
    Creates bulk actions from a list of json data
    @index  : index name
    @data   : list of json data
    @source : source of the dataset (e.g., kickstarter, ulule, etc.)
    '''
    for doc in data:

        yield {
            '_index'  : index,
            '_id'     : doc['id'],
            '_source' : doc
        }


def read_webrobots_kickstarter_data(filename):
    '''
    Returns Kickstarter data from json file dump obtained from https://webrobots.io
    Expects data in the following format: Each line has a valid json string which contains project details
    @filename : input filename
    '''
    with open(filename, 'r') as f:
        lines = f.readlines()

    projects_list = []
    for line in lines:
        project = json.loads(line)['data']

        # NOTE: The mappings should be retrieved from the mappings PR.
        projects_list.append({
            'id'              : project.get('id',       'n.a.'),
            'title'           : project.get('name',     'n.a.'),
            'description'     : project.get('blurb',    'n.a.'),
            'status'          : project.get('state',    'n.a.'),
            'country'         : project.get('country',  'n.a.'),
            'innovation_type' : project.get('category', {}).get('name',  'n.a.'),
            'city'            : project.get('location', {}).get('state', 'n.a.'),
            'contact_person'  : project.get('creator',  {}).get('name',  'n.a.'),
            'link'            : project.get('urls',     {}).get('web',   {}).get('project', 'n.a.')
        })
    
    return projects_list
