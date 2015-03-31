from django.conf import settings
from django.db import models

# django_mongodb_engine
from django_mongodb_engine.contrib import MongoDBManager


class Answer(models.Model):
    uid = models.CharField(max_length=50)
    session_id = models.CharField(max_length=50)
    content = models.TextField(null=True, blank=True)       # json???
    created = models.DateTimeField(null=True, blank=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'answers_answers'
        ordering = ['-created']

    def save(self, *args, **kwargs):
        super(Answer, self).save(using=settings.DB_NONREL)
