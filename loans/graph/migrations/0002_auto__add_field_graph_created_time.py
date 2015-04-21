# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Graph.created_time'
        db.add_column('graphs_graphs', 'created_time',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Graph.created_time'
        db.delete_column('graphs_graphs', 'created_time')


    models = {
        u'graph.graph': {
            'Meta': {'object_name': 'Graph', 'db_table': "'graphs_graphs'"},
            'api_type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'dest_uid': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'obj_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'obj_type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'src_uid': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['graph']