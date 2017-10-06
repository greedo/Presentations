import celery
from copy import deepcopy
from django.db import models


class Profile (models.Model):
    """ Profile information
    """

    email = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        celery.current_app.send_task('search_indexer.add_doc',
            (self.id,))

    def delete(self, *args, **kwargs):
        current_pk = deepcopy(self.pk)
        super(Profile, self).delete(*args, **kwargs)
        celery.current_app.send_task('search_indexer.delete_doc',
                (current_pk,))
