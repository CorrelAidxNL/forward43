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


def get_data_from_json_file(filename):
    '''
    Get (kicstarter projects) data from json file dump.
    Expects data in the following format: Each line has a valid json string which contains project details
    @filename : input filename
    '''
    with open(filename, 'r') as f:
        lines = f.readlines()
        
    json_data = []
    for line in lines:
        temp_json = json.loads(line)['data']

        # FIXME: The mappings should be retrieved from the mappings PR.  
        json_data.append({
            'name'    : temp_json['name'],
            'state'   : temp_json['state'],
            'pledged' : temp_json['pledged'],
            'creator' : temp_json['creator']['name']
        })
    
    return json_data
