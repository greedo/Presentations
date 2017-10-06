from celery import task, group
from elasticsearch import Elasticsearch


@task
def index_all_docs():
    """ Master task for indexing all profiles into
    Elasticsearch.
    """
    from profile_model import Profile

    es_instance = Elasticsearch('https://my_elasticsearchserver')
    es_instance.es.indices.create('my-new-index')
    profiles = list(Profile.objects.all().values_list('id', flat=True))
    group(process_doc.si(i) for i in profiles)()

@task
def process_doc(a_profile_id):
    """ Grabs the database objects and field names necessary to
    flatten a single document.
    """
    from profile_model import Profile

    candidate_profile = Profile.objects.get(pk=a_profile_id)
    field_names = [f for f in candidate_profile._meta.get_all_field_names(Profile)]
    flattened_doc = index_single_doc(field_names, profile)
    add_doc(flattened_doc, a_profile_id)

def add_doc(self, data, doc_id):
    """ Adds a new document to Elasticsearch.
    """
    es_instance = Elasticsearch('https://my_elasticsearchserver')
    es_instance.index(index='my-index', doc_type='db-text', id=doc_id,
                      body=data, refresh=True)

def update_doc(self, doc_id, data):
    """ Updates to an existing document in Elasticsearch.
    """
    es_instance = Elasticsearch('https://my_elasticsearchserver')
    es_instance.update(index='my-new-index', doc_type='db-text', id=doc_id,
                       body={'doc': json.loads(data)}, refresh=True)

def index_single_doc(field_names, profile):
    """ Handles the flattening logic of a single document for
    Elasticsearch.
    """
    index = {}
    for field_name in field_names:
        field_value = getattr(profile, field_name)
        index[field_name] = field_value
    return index
