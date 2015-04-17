# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Graph'
        db.create_table('graphs_graphs', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('obj_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('src_uid', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('dest_uid', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('obj_type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('api_type', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'graph', ['Graph'])


    def backwards(self, orm):
        # Deleting model 'Graph'
        db.delete_table('graphs_graphs')


    models = {
        u'graph.graph': {
            'Meta': {'object_name': 'Graph', 'db_table': "'graphs_graphs'"},
            'api_type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'dest_uid': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'obj_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'obj_type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'src_uid': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['graph']