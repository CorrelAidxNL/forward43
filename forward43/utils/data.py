import os
import json


def get_doc_id(document, source):
    '''
    For a given document from source dataset, generate a document id
    @document : Doument object. There should be a project id associated with each document
    @source   : Source dataset
    '''
    return source + '_' + document['id']

def bulk_json_data(index, data, source):
    '''
    Creates bulk actions from a list of json data
    @index  : index name
    @data   : list of json data
    @source : source of the dataset (e.g., kickstarter, ulule, etc.)
    '''
    for doc in data:

        _id = get_doc_id(doc, source)

        yield {
            '_index'  : index,
            '_id'     : _id,
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
