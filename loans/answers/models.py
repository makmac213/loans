from django.conf import settings
from django.db import models

# django_mongodb_engine
from django_mongodb_engine.contrib import MongoDBManager


class Answer(models.Model):
    uid = models.CharField(max_length=50, null=True, blank=True)
    #session_id = models.CharField(max_length=50, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    infos = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    #facebook_me = models.TextField(null=True, blank=True)
    #facebook_likes = models.TextField(null=True, blank=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'answers_answers'
        ordering = ['-created']

    def save(self, *args, **kwargs):
        super(Answer, self).save(using=settings.DB_NONREL)
