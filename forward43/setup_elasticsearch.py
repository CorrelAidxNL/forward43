import json
import os
import pandas as pd

import utils_elasticsearch as utils


def create_index_with_mapping(es):

    # FIXME: The mappings should be retrieved from the mappings PR
    mappings = {
        "properties": {
            "name": {
                "type": "keyword"
            },
            "creator": {
                "type": "text"
            },
            "pledged": {
                "type": "float"
            },
            "state": {
                "type": "text"
            }
        }
    }

    is_created = utils.create_index(
        es_object  = es, 
        index_name = 'forward43', 
        mappings   = mappings,
        n_shards   = 1,
        n_replicas = 0
    )


def read_json_data(es):

    # FIXME: This assumes that data is stored in ../data folder. Only kickstarter_scraper does this.
    #        1. Do the same for the other scrapers
    #        2. Add a path argument
    data_path_common = '../data/'

    for _file in os.listdir(data_path_common):

        if _file.endswith('.json'):
            with open(data_path_common + _file) as f:
                d = json.load(f)
    
            for doc in d:
                d_smaller = {
                    'name'    : doc['name'],
                    'creator' : doc['creator'],
                    'pledged' : doc['pledged'],
                    'state'   : doc['state']
                }
                utils.index_document(es, 'forward43', '_doc', d_smaller)


def read_csv_file(es):

    # FIXME: This assumes that data is stored in ../data folder. Only kickstarter_scraper does this.
    #        1. Do the same for the other scrapers
    #        2. Add a path argument
    data_path_common = '../data/'

    for _file in os.listdir(data_path_common):
        if _file.endswith('.csv'):

            df = pd.read_csv(data_path_common + _file)

            for i in range(len(df)):
                try:
                    d_smaller = {
                        'name'    : df.loc[i, 'name'],
                        'creator' : json.loads(df.loc[i, 'creator']).get('name', 'n.a.'),
                        'pledged' : df.loc[i, 'pledged'],
                        'state'   : df.loc[i, 'state']
                    }

                    utils.index_document(es, 'forward43', '_doc', d_smaller)
                except:
                    pass


if __name__ == '__main__':

    # Get ES instance
    es = utils.connect_elasticsearch()
    # Create a mapping if necessary
    create_index_with_mapping(es)
    # # Read data from json file
    # read_json_data(es)
    # # Read data from csv file
    # read_csv_file(es)
