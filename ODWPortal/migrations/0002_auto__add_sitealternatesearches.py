# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SiteAlternateSearches'
        db.create_table('ODWPortal_sitealternatesearches', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ODWPortal.Site'])),
            ('alt_site_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('site_order', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('site_relationship', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('alt_site_url', self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=200)),
            ('alt_site_label', self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=200)),
            ('alt_site_syntax', self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=10)),
        ))
        db.send_create_signal('ODWPortal', ['SiteAlternateSearches'])


    def backwards(self, orm):
        # Deleting model 'SiteAlternateSearches'
        db.delete_table('ODWPortal_sitealternatesearches')


    models = {
        'ODWPortal.language': {
            'Meta': {'object_name': 'Language'},
            'afield': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'avalue': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site_language': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'ODWPortal.site': {
            'Meta': {'object_name': 'Site'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'site_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'site_url': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'ODWPortal.sitealternatesearches': {
            'Meta': {'object_name': 'SiteAlternateSearches'},
            'alt_site_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'alt_site_label': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '200'}),
            'alt_site_syntax': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '10'}),
            'alt_site_url': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ODWPortal.Site']"}),
            'site_order': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'site_relationship': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'ODWPortal.sitesetup': {
            'Meta': {'object_name': 'SiteSetup'},
            'afield': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'avalue': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ODWPortal.Site']"})
        }
    }

    complete_apps = ['ODWPortal']