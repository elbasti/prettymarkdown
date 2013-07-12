# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Stationary.name'
        db.add_column(u'documanager_stationary', 'name',
                      self.gf('django.db.models.fields.CharField')(default='My name', max_length=20),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Stationary.name'
        db.delete_column(u'documanager_stationary', 'name')


    models = {
        u'documanager.stationary': {
            'Meta': {'object_name': 'Stationary'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'styling': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['documanager']