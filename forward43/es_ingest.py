import json
import os

from forward43.data.data_path import DATA_DIRECTORY
from forward43.logger         import logger

import forward43.utils.elasticsearch as es_utils


def injest_data_to_es(es_host, es_port, es_user, es_secret):
    '''
    Load json data and Injest into elastic
    @host : elasticsearch host
    @port : elasticsearch port
    '''
    if es_host == 'localhost':
        es_object = es_utils.connect_elasticsearch_localhost(host=es_host, port=es_port)
    else:
        es_object = es_utils.connect_elastic_remote(host=es_host, port=es_port, user=es_user, secret=es_secret)

    # injest scraped data
    for filepath in os.listdir(DATA_DIRECTORY):
        if filepath.endswith('.json'):
            load_to_es(os.path.join(DATA_DIRECTORY, filepath), es_object)

        try:
            with open(filepath) as f:
                data = json.load(f)

            for document in data:
                es_utils.index_document(es_object, 'forward43', '_doc', document, document['id'])

        except Exception as e:
            logger.exception(f'Error while reading {filepath}. Message: {e}')


if __name__ == '__main__':

    injest_data_to_es(es_host='localhost', es_port=9200)
