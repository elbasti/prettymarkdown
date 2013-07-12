# Tests for documanager utils
from django.test import TestCase
from documanager.utils import make_html

class MarkdownProcessTestCase(TestCase):
    
    def test_should_accept_one_arg(self):
        self.assertRaises(TypeError, make_html,"foo", "bar")

    def test_should_not_accept_nothing(self):
        self.assertRaises(ValueError, make_html,None)

    def test_should_make_html(self):
        html = make_html("Hello world!")
        self.assertEqual(html.rstrip('\n'), u"<p>Hello world!</p>") 

    def test_should_make_wiki_tables(self):
        table = "|| col1 || col2 || col3 ||"
        html = make_html(table)
        self.assertNotEqual(html.find('<table>'), -1)
