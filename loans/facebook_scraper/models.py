from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# django_mongodb_engine
from django_mongodb_engine.contrib import MongoDBManager


class Like(models.Model):
    user = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    created_time = models.DateTimeField(null=True, blank=True)
    object_name = models.CharField(max_length=255, null=True, blank=True)
    object_id = models.CharField(max_length=255, null=True, blank=True)
    raw = models.TextField(null=True, blank=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'facebook_likes'

    def save(self, *args, **kwargs):
        super(Like, self).save(using=settings.DB_NONREL)


class Photo(models.Model):
    user = models.IntegerField(null=True, blank=True)
    object_id = models.CharField(max_length=255, null=True, blank=True)
    album = models.CharField(max_length=40, null=True, blank=True)
    #backdated_time = models.DateTimeField(null=True, blank=True)
    #backdated_time_granularity = models.DateTimeField(null=True, blank=True)
    created_time = models.DateTimeField(null=True, blank=True)
    event = models.CharField(max_length=40, null=True, blank=True)
    object_from = models.TextField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    icon = models.TextField(null=True, blank=True)
    images = models.TextField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    name = models.TextField(null=True, blank=True)
    picture = models.URLField(null=True, blank=True)
    place = models.TextField(null=True, blank=True)
    source = models.URLField(null=True, blank=True)
    updated_time = models.DateTimeField(null=True, blank=True)
    width = models.TextField(null=True, blank=True)
    # tags has paging need to scrape all
    tags = models.TextField(null=True, blank=True)
    # likes has paging need to scrape all
    likes = models.TextField(null=True, blank=True)
    # comments has paging need to scrape all
    comments = models.TextField(null=True, blank=True)

    raw = models.TextField(null=True, blank=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'facebook_photos'

    def save(self, *args, **kwargs):
        super(Photo, self).save(using=settings.DB_NONREL)


class Video(models.Model):
    user = models.IntegerField(null=True, blank=True)
    object_id = models.CharField(max_length=255, null=True, blank=True)
    created_time = models.DateTimeField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    embed_html = models.TextField(null=True, blank=True)
    format = models.TextField(null=True, blank=True)
    object_from = models.TextField(null=True, blank=True)
    icon = models.TextField(null=True, blank=True)
    length = models.FloatField(null=True, blank=True)
    name = models.TextField(null=True, blank=True)
    picture = models.URLField(null=True, blank=True)
    source = models.URLField(null=True, blank=True)
    tags = models.TextField(null=True, blank=True)
    updated_time = models.DateTimeField(null=True, blank=True)

    raw = models.TextField(null=True, blank=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'facebook_videos'

    def save(self, *args, **kwargs):
        super(Video, self).save(using=settings.DB_NONREL)


class Feed(models.Model):
    user = models.IntegerField(null=True, blank=True)
    feed_id = models.CharField(max_length=255, null=True, blank=True)
    object_from = models.TextField(null=True, blank=True)
    object_to = models.TextField(null=True, blank=True)
    with_tags = models.TextField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    story = models.TextField(null=True, blank=True)
    story_tags = models.TextField(null=True, blank=True)
    picture = models.URLField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    icon = models.TextField(null=True, blank=True)
    privacy = models.TextField(null=True, blank=True)
    object_type = models.CharField(max_length=100, null=True, blank=True)
    object_id = models.CharField(max_length=255, null=True, blank=True)
    created_time = models.DateTimeField(null=True, blank=True)
    updated_time = models.DateTimeField(null=True, blank=True)
    is_hidden = models.CharField(max_length=20, null=True, blank=True)
    subscribed = models.CharField(max_length=20, null=True, blank=True)
    likes = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)

    raw = models.TextField(null=True, blank=True)

    objects = MongoDBManager()

    class Meta:
        db_table = 'facebook_feeds'

    def save(self, *args, **kwargs):
        super(Feed, self).save(using=settings.DB_NONREL)


class Post(models.Model):
    user = models.IntegerField(null=True, blank=True)
    post_id = models.CharField(max_length=255, null=True, blank=True)
    object_from = models.TextField(null=True, blank=True)
    object_to = models.TextField(null=True, blank=True)
    with_tags = models.TextField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    story = models.TextField(null=True, blank=True)
    story_tags = models.TextField(null=True, blank=True)
    picture = models.URLField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    icon = models.TextField(null=True, blank=True)
    privacy = models.TextField(null=True, blank=True)
    object_type = models.CharField(max_length=100, null=True, blank=True)
    object_id = models.CharField(max_length=255, null=True, blank=True)
    created_time = models.DateTimeField(null=True, blank=True)
    updated_time = models.DateTimeField(null=True, blank=True)
    is_hidden = models.CharField(max_length=20, null=True, blank=True)
    subscribed = models.CharField(max_length=20, null=True, blank=True)
    likes = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    status_type = models.CharField(max_length=50, null=True, blank=True)
    name = models.TextField(null=True, blank=True)
    caption = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    objects = MongoDBManager()
    
    class Meta:
        db_table = 'facebook_posts'

    def save(self, *args, **kwargs):
        super(Post, self).save(using=settings.DB_NONREL)