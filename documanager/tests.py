from django.core.urlresolvers import reverse
from documanager.models import *

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django import forms
from documanager.forms import MarkdownForm
class ViewsTestCase(TestCase):

    def test_should_respond_to_root(self):
        response = self.client.get('/')
        # Check that root works
        self.assertEqual(response.status_code, 200, "root not returning 200")

class IndexTestCase(TestCase):

    def setUp(self):
        self.response = self.client.get(reverse('documanager:index')) 

    def test_index_should_return(self):
        self.assertEqual(self.response.status_code, 200, "index not returning 200")

    def test_index_returns_form(self):
        self.assertEqual(type(self.response.context['form']), MarkdownForm, 
                        "Index not returning a Markdown Form")

    def test_index_should_render_home(self):
        self.assertIn('documanager/home.html', 
                        [template.name for template in (self.response.templates)],
                        "Index not rendering home template"
                     )

class MarkdownFormTestCase(TestCase):

    def setUp(self):
        self.form = MarkdownForm()

    def test_should_exist(self):
        self.assertEqual(type(MarkdownForm()),MarkdownForm)

    def test_should_accept_text(self):
        self.assertEqual(type(self.form.fields['markdown_input']),
                forms.CharField)
    
    def test_widget_should_be_textarea(self):
        self.assertEqual(type(self.form.fields['markdown_input'].widget),
                forms.widgets.Textarea, "widget is not a textarea")

    def test_should_accept_letterheads(self):
        self.assertEqual(type(self.form.fields['letterhead']),
                forms.ChoiceField, "is not a choice field")

