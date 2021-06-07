import forward43.utils.elasticsearch as es_utils


if __name__ == '__main__':

    # Get ES instance
    es_object = es_utils.connect_elasticsearch()

    # Fetch mappings
    # NOTE: The mappings should be retrieved from the mappings PR
    mappings = {
        "properties": {
            "title"           : { "type" : "text" },
            "description"     : { "type" : "text" },
            "status"          : { "type" : "text" },
            "innovation_type" : { "type" : "text" },
            "country"         : { "type" : "text" },
            "contact"         : { "type" : "text" },
            "link"            : { "type" : "text" },
        }
    }

    # Create index 
    is_created = es_utils.create_index(
        es_object  = es_object, 
        index_name = 'forward43', 
        mappings   = mappings,
        n_shards   = 1,
        n_replicas = 0
    )
