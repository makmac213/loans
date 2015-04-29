# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Engagement.description'
        db.add_column('odesk_engagements', 'description',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Engagement.dev_recno_ciphertext'
        db.add_column('odesk_engagements', 'dev_recno_ciphertext',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Engagement.engagement_end_date'
        db.add_column('odesk_engagements', 'engagement_end_date',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Engagement.engagement_job_type'
        db.add_column('odesk_engagements', 'engagement_job_type',
                      self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Engagement.engagement_start_date'
        db.add_column('odesk_engagements', 'engagement_start_date',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Engagement.engagement_title'
        db.add_column('odesk_engagements', 'engagement_title',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Engagement.hourly_charge_rate'
        db.add_column('odesk_engagements', 'hourly_charge_rate',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True),
                      keep_default=False)

        # Adding field 'Engagement.hourly_pay_rate'
        db.add_column('odesk_engagements', 'hourly_pay_rate',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True),
                      keep_default=False)

        # Adding field 'Engagement.is_paused'
        db.add_column('odesk_engagements', 'is_paused',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Engagement.is_trial_assignment'
        db.add_column('odesk_engagements', 'is_trial_assignment',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Engagement.job_title'
        db.add_column('odesk_engagements', 'job_title',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Engagement.job_ref_ciphertext'
        db.add_column('odesk_engagements', 'job_ref_ciphertext',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Engagement.offer__reference'
        db.add_column('odesk_engagements', 'offer__reference',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Engagement.portrait_url'
        db.add_column('odesk_engagements', 'portrait_url',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Engagement.provider_id'
        db.add_column('odesk_engagements', 'provider_id',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Engagement.provider_reference'
        db.add_column('odesk_engagements', 'provider_reference',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Engagement.provider_team_id'
        db.add_column('odesk_engagements', 'provider_team_id',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Engagement.provider_team_reference'
        db.add_column('odesk_engagements', 'provider_team_reference',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Engagement.reference'
        db.add_column('odesk_engagements', 'reference',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Engagement.status'
        db.add_column('odesk_engagements', 'status',
                      self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Engagement.weekly_hours_limit'
        db.add_column('odesk_engagements', 'weekly_hours_limit',
                      self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Engagement.weekly_salary_charge_amount'
        db.add_column('odesk_engagements', 'weekly_salary_charge_amount',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True),
                      keep_default=False)

        # Adding field 'Engagement.weekly_salary_pay_amount'
        db.add_column('odesk_engagements', 'weekly_salary_pay_amount',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Engagement.description'
        db.delete_column('odesk_engagements', 'description')

        # Deleting field 'Engagement.dev_recno_ciphertext'
        db.delete_column('odesk_engagements', 'dev_recno_ciphertext')

        # Deleting field 'Engagement.engagement_end_date'
        db.delete_column('odesk_engagements', 'engagement_end_date')

        # Deleting field 'Engagement.engagement_job_type'
        db.delete_column('odesk_engagements', 'engagement_job_type')

        # Deleting field 'Engagement.engagement_start_date'
        db.delete_column('odesk_engagements', 'engagement_start_date')

        # Deleting field 'Engagement.engagement_title'
        db.delete_column('odesk_engagements', 'engagement_title')

        # Deleting field 'Engagement.hourly_charge_rate'
        db.delete_column('odesk_engagements', 'hourly_charge_rate')

        # Deleting field 'Engagement.hourly_pay_rate'
        db.delete_column('odesk_engagements', 'hourly_pay_rate')

        # Deleting field 'Engagement.is_paused'
        db.delete_column('odesk_engagements', 'is_paused')

        # Deleting field 'Engagement.is_trial_assignment'
        db.delete_column('odesk_engagements', 'is_trial_assignment')

        # Deleting field 'Engagement.job_title'
        db.delete_column('odesk_engagements', 'job_title')

        # Deleting field 'Engagement.job_ref_ciphertext'
        db.delete_column('odesk_engagements', 'job_ref_ciphertext')

        # Deleting field 'Engagement.offer__reference'
        db.delete_column('odesk_engagements', 'offer__reference')

        # Deleting field 'Engagement.portrait_url'
        db.delete_column('odesk_engagements', 'portrait_url')

        # Deleting field 'Engagement.provider_id'
        db.delete_column('odesk_engagements', 'provider_id')

        # Deleting field 'Engagement.provider_reference'
        db.delete_column('odesk_engagements', 'provider_reference')

        # Deleting field 'Engagement.provider_team_id'
        db.delete_column('odesk_engagements', 'provider_team_id')

        # Deleting field 'Engagement.provider_team_reference'
        db.delete_column('odesk_engagements', 'provider_team_reference')

        # Deleting field 'Engagement.reference'
        db.delete_column('odesk_engagements', 'reference')

        # Deleting field 'Engagement.status'
        db.delete_column('odesk_engagements', 'status')

        # Deleting field 'Engagement.weekly_hours_limit'
        db.delete_column('odesk_engagements', 'weekly_hours_limit')

        # Deleting field 'Engagement.weekly_salary_charge_amount'
        db.delete_column('odesk_engagements', 'weekly_salary_charge_amount')

        # Deleting field 'Engagement.weekly_salary_pay_amount'
        db.delete_column('odesk_engagements', 'weekly_salary_pay_amount')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'codename',)", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'odesk_scraper.engagement': {
            'Meta': {'object_name': 'Engagement', 'db_table': "'odesk_engagements'"},
            'buyer_team_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'buyer_team_reference': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created_time': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dev_recno_ciphertext': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'engagement_end_date': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'engagement_job_type': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'engagement_start_date': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'engagement_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'hourly_charge_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'hourly_pay_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_paused': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_trial_assignment': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'job_ref_ciphertext': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'job_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'offer__reference': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'portrait_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'engagements'", 'to': u"orm['odesk_scraper.OdeskProfile']"}),
            'provider_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'provider_reference': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'provider_team_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'provider_team_reference': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'weekly_hours_limit': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'weekly_salary_charge_amount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'weekly_salary_pay_amount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'})
        },
        u'odesk_scraper.odeskprofile': {
            'Meta': {'object_name': 'OdeskProfile', 'db_table': "'odesk_profiles'"},
            'capacity_affiliate_manager': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'capacity_buyer': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'capacity_provider': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'company_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'has_agency': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_provider': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'odesk_id': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'portrait_100_img': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'portrait_32_img': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'portrait_50_img': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'profile_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'ref': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'timezone_offset': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'odesk_profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['odesk_scraper']