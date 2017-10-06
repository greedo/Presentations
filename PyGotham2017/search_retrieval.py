from profile_model import Profile
from elasticsearch import Elasticsearch


class Search(object):
    """ Everything search
    """

    __query_fields = ['first_name',
                      'last_name']

    __available_query_flags = ['phrase']

    __function_scripts = [{'field_value_factor': {'field': 'profile_completeness', 'factor': 1.0, 'modifier': 'ln', 'missing': 1.0}}]

    def __init__(self, index):
        self.es_instance = Elasticsearch('https://my_elasticsearchserver')
        self.index = index

    def basic_search(self, query_string, limit, offset):
        """ Basic search functionality
        """
        query_json = {'query': {'simple_query_string': {'query': query_string, 'fields': self.__query_fields}}}
        search_json.update({'query': {'function_score': {'query': {'filtered': query_json}, 'functions': self.__function_scripts}}})
        es_results = self.es_instance.search(index=self.index,
                                             body=search_json,
                                             size=limit,
                                             from_=offset)

        hits_data = es_results['hits']
        raw_ids = list(set([hit['_source']['id'] for hit in hits_data['hits']]))

        search_results = []
        for _id in raw_ids:
            try:
                search_results.append(Profile.objects.get(pk=_id))
            except:
                pass

        return search_results
