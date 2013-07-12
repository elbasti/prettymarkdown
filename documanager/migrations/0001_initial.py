# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Stationary'
        db.create_table(u'documanager_stationary', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('styling', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'documanager', ['Stationary'])


    def backwards(self, orm):
        # Deleting model 'Stationary'
        db.delete_table(u'documanager_stationary')


    models = {
        u'documanager.stationary': {
            'Meta': {'object_name': 'Stationary'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'styling': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['documanager']