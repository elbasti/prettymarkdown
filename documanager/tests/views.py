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

class IndexNoStationaryTestCase(TestCase):
    def test_should_declare_no_stationaries(self):
        self.response = self.client.get(reverse('documanager:index'))
        self.assertTrue(self.response.context['no_stationary'])

class IndexStationaryTestCase(TestCase):
    fixtures = ['stationary.json']

    def setUp(self):
        self.url = reverse('documanager:index')
        self.response = self.client.get(self.url)

    def test_should_not_declare_no_stationaries(self):
        self.assertRaises(KeyError, lambda: self.response.context['no_stationary'])

    def test_should_not_return_html_if_not_valid(self):
        invalid_response = self.client.post(self.url)
        self.assertRaises(KeyError, lambda: invalid_response.context['html'])

    def test_should_return_html_if_valid(self):
        response = self.client.post(self.url, 
                {'stationary':'1', 'markdown_input': "Hello"})
        self.assertEqual(response.context['html'].rstrip('\n'),
                u'<p>Hello</p>')

    def test_should_not_rendertemplate_if_preview(self):
        self.assertNotIn('documanager/browser_render.html',
                [template.name for template in (self.response.templates)],
                "rendering browser render template when not supposed to")
    
    def test_should_render_template_in_browser(self):
        response = self.client.post(self.url,
                {'stationary':'1', 'markdown_input': "hello", 'generate':'generate'}
                )

        self.assertIn('documanager/browser_render.html',
                [template.name for template in (response.templates)])



class PrintTestCase(TestCase):
    fixtures = ['stationary.json']

    def setUp(self):
        self.url = reverse('documanager:index')
        self.response = self.client.post(self.url,
                {'stationary':'1', 'markdown_input':"Hello", 'print':'print'}
                )
        print self.response
    def test_returns_pdf_MIME(self):
        self.assertEqual(self.response['Content-Type'], 'application/pdf')


class print_to_browserTestCase(TestCase):
    def setUp(self):
        self.view_url = reverse('documanager:print_to_browser')
        self.index_url = reverse('documanager:index')

    def test_redirects_if_not_post(self):
        response = self.client.get(self.view_url)
        self.assertRedirects(response, self.index_url)

    def test_returns_ok_if_post(self):
        response = self.client.post(self.view_url)

class print_to_pdfviewTestCase(TestCase):
    def setUp(self):
        self.view_url = reverse('documanager:print_to_pdf')
        self.response = self.client.get(self.view_url)

    def test_returns_ok(self):
        self.assertEquals(self.response.status_code, 200)
