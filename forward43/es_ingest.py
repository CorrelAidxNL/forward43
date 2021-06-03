import json
import os

from data.data_path import DATA_DIRECTORY

import utils.elasticsearch as es_utils


def load_to_es(filepath, es_object): 
    '''
    Load json data into elastic
    @filepath  : json filepath which contains project details
    @es_object : es instance
    '''
    try:
        with open(filepath) as f:
            data = json.load(f)

        for document in data:
            es_utils.index_document(es_object, 'forward43', '_doc', document, document['id'])

    except Exception as e:
        print(f'Error while reading {filepath}. Message: {e}')


if __name__ == '__main__':

    # Get ES instance
    es_object = es_utils.connect_elasticsearch()

    # Populate ES with data
    for filepath in os.listdir(DATA_DIRECTORY):
        if not filepath.endswith('.json'):
            continue

        print(f'file: {filepath}')
        load_to_es(os.path.join(DATA_DIRECTORY, filepath), es_object)
