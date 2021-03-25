import os
import json
import uuid


def bulk_json_data(index, json_list):

    for doc in json_list:
        yield {
            '_index'  : index,
            '_id'     : uuid.uuid4(),
            '_source' : doc
        }


def load_data_from_json_file(filename):
    '''
    Returns data (list of dictionaries) from json file dump.
    Expects data in the following format: Each line has a valid json string which contains project details
    @filename : input filename
    '''
    with open(filename, 'r') as f:
        lines = f.readlines()

    json_data = []
    for line in lines:
        temp_json = json.loads(line)['data']

        # TODO: The mappings should be retrieved from the mappings PR.
        json_data.append({
            'title'           : temp_json['title'],
            'description'     : temp_json['description'],
            'status'          : temp_json['status'],
            'innovation_type' : temp_json['innovation_type'],
            'country'         : temp_json['country'],
            'city'            : temp_json['city'],
            'contact_person'  : temp_json['contact_person'],
            'link'            : temp_json['link']
        })
    
    return json_data
