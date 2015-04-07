from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# django_mongodb_engine
from django_mongodb_engine.contrib import MongoDBManager


class Like(models.Model):
    user = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    created_time = models.CharField(max_length=255, null=True, blank=True)
    object_name = models.CharField(max_length=255, null=True, blank=True)
    object_id = models.CharField(max_length=255, null=True, blank=True)
    raw = models.TextField(null=True, blank=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'facebook_likes'

    def save(self, *args, **kwargs):
        super(Like, self).save(using=settings.DB_NONREL)