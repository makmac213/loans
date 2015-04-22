from django.contrib.auth.models import User
from django.db import models


class Graph(models.Model):
    obj_id = models.CharField(max_length=50)
    src_uid = models.CharField(max_length=50)
    dest_uid = models.CharField(max_length=50)
    obj_type = models.CharField(max_length=30)
    api_type = models.CharField(max_length=30)
    created_time = models.DateTimeField(null=True, 
                                        blank=True)

    class Meta:
        db_table = 'graphs_graphs'


class GraphUser(models.Model):
    fb_id = models.CharField(max_length=50)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    link = models.URLField()
    name = models.CharField(max_length=255)
    created_time = models.DateTimeField(null=True, 
                                        blank=True)

    class Meta:
        db_table = 'graphs_graph_users'


class GraphTask(models.Model):
    user = models.ForeignKey(User, related_name='graph_tasks')
    session_id = models.CharField(max_length=255)
    task_likes = models.BooleanField(default=False)
    task_photos = models.BooleanField(default=False)
    task_videos = models.BooleanField(default=False)
    task_feeds = models.BooleanField(default=False)
    task_posts = models.BooleanField(default=False)
    task_inbox = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def is_completed(self):
        return self.task_likes and self.task_photos and self.task_videos \
                and self.task_feeds and self.task_posts and self.task_inbox

