from typing_extensions import Literal
from elasticsearch import Elasticsearch, helpers
import json

from forward43.configurations.configuration_path import CONFIG_DIRECTORY


def connect_elasticsearch(host='localhost', port=9200):
    """ Connect to Elasticsearch host. """
    es = Elasticsearch([{'host': host, 'port': port}])
    if not es.ping():
        raise ConnectionError(f'Failed to connect to {es}!')
    else:
        print(f'Connected to {es}')

    return es


def create_index(es_object, index_name, mappings=None, n_shards=1, n_replicas=0):
    """ Create an index if it does not exists yet. """
    is_created = False

    settings = {
        'settings': {
            'number_of_shards': n_shards,
            'number_of_replicas': n_replicas
        },
        'mappings': mappings
    }

    try:
        if not es_object.indices.exists(index_name):
            es_object.indices.create(index=index_name, ignore=400, body=settings)  # Ignore 400 "Index Already Exist" error
            print(f'Created Index: {index_name}')
        is_created = True
    except Exception as e:
        print(f'Failed to create index: {e}')
    finally:
        return is_created


def index_document(elastic_object, index, doc_type, document, id):
    """ Index a document. """
    try:
        result = elastic_object.index(index=index, doc_type=doc_type, body=document, id=id)
    except Exception as e:
        print(f'Failed to index document: {e}')

    return result


def search(es_object, index, search_params):
    """ Search the Elasticsearch index. """
    json_search = json.dumps(search_params)
    result = es_object.search(index=index, body=json_search)

    return result


def get_document(es_object, index, doc_type, es_id):
    """ Get a document. """
    result = es_object.get(index=index, doc_type=doc_type, id=es_id)

    return result


def bulk_ingest(es_object, actions, **kwargs):
    """ Bulk ingest """
    try:
        response = helpers.bulk(es_object, actions, **kwargs)
    except Exception as e:
        print(f'Failed to complete a bulk action: {e}')

    return response


def get_mappings(index_type: Literal["project_scrapes", "linkedin", "masterpeace_meal"]) -> dict:
    """Get ES mapping properties based on index type

    Args:
        index_type: Literal["project_scrapes", "linkedin", "masterpeace_meal"]
            project_scrapes: scrapes of innovations found online
            linkedin: linkedin descriptions of companies
            masterpeace_meal: evaluations from masterpeace clubs' projects
    Returns:
        dict: mappings to instantiate an elasticsearch index
    """
    if index_type == "masterpeace_meal":
        raise NotImplementedError

    if index_type == "linkedin":
        file_name = CONFIG_DIRECTORY+"/linkedin_mapping.json"
    elif index_type == "project_scrapes":
        file_name = CONFIG_DIRECTORY+"/project_scrapes_mapping.json"
    else:
        raise NotImplementedError


    with open(file_name, "r") as f:
        mapping = json.load(f)

    return mapping
