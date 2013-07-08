from django.core.urlresolvers import reverse
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

class DocuManagerTestCase(TestCase):

    def test_root(self):
        response = self.client.get('/')
        # Check that root works
        self.assertEqual(response.status_code, 200, "root not returning 200")
    
    def test_index(self):
        response = self.client.get(reverse('documanager:index'))
        self.assertEqual(response.status_code, 200, "index not returning 200")
