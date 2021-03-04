import json
import os
import pandas as pd

import utils_elasticsearch as utils


def create_index_with_mapping(es):

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
                    print(i)

                    utils.index_document(es, 'forward43', '_doc', d_smaller)
                except:
                    pass


if __name__ == '__main__':

    es = utils.connect_elasticsearch()

    # create_index_with_mapping(es)

    # read_json_data(es)

    read_csv_file(es)












