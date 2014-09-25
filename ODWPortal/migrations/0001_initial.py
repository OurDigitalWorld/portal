# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Language'
        db.create_table('ODWPortal_language', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site_language', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('afield', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('avalue', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('ODWPortal', ['Language'])

        # Adding model 'Site'
        db.create_table('ODWPortal_site', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('site_url', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('ODWPortal', ['Site'])

        # Adding model 'SiteSetup'
        db.create_table('ODWPortal_sitesetup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ODWPortal.Site'])),
            ('afield', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('avalue', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('ODWPortal', ['SiteSetup'])


    def backwards(self, orm):
        # Deleting model 'Language'
        db.delete_table('ODWPortal_language')

        # Deleting model 'Site'
        db.delete_table('ODWPortal_site')

        # Deleting model 'SiteSetup'
        db.delete_table('ODWPortal_sitesetup')


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
            'date_added': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'site_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'site_url': ('django.db.models.fields.CharField', [], {'max_length': '256'})
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