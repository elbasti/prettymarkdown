# Tests for Documanager's views
from django.test import TestCase
from django.core.urlresolvers import reverse
from documanager.forms import MarkdownForm
from documanager.models import Stationary

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

    def test_should_declare_no_stationaries(self):
        self.assertTrue(self.response.context['no_stationary'])

class IndexStationaryTestCase(TestCase):
    def setUp(self):
        test_stationary = Stationary(name="test stationary", styling="bar")
        test_stationary.save()
        self.response = self.client.get(reverse('documanager:index'))
    def test_should_not_declare_no_stationaries(self):
        self.assertRaises(KeyError, lambda: self.response.context['no_stationary'])
