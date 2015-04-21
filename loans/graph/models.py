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


