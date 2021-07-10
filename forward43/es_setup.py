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

    # Create index projects
    is_created = es_utils.create_index(
        es_object  = es_object,
        index_name = 'forward43',
        mappings   = es_utils.get_mappings("project_scrapes"),
        n_shards   = 1,
        n_replicas = 0
    )

    # Create index linkedin
    is_created = es_utils.create_index(
        es_object  = es_object,
        index_name = 'forward43_companies',
        mappings   = es_utils.get_mappings("linkedin"),
        n_shards   = 1,
        n_replicas = 0
    )
