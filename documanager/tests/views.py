# Tests for Documanager's views
import warnings

from django.test import TestCase
from django.core.urlresolvers import reverse
from documanager.forms import MarkdownForm
from documanager.models import Stationary
import json

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
    #def test_returns_pdf_MIME(self):
    #    self.assertEqual(self.response['Content-Type'], 'application/pdf')

class EmailPDFTestCase(TestCase):

    def setUp(self):
        self.url = reverse('documanager:email_pdf')
        self.valid_json = {"From":"myUser@theirDomain.com","FromFull":{"Email":"myUser@theirDomain.com","Name":"John Doe"},"To":"451d9b70cf9364d23ff6f9d51d870251569e+ahoy@inbound.postmarkapp.com","ToFull":[{"Email":"451d9b70cf9364d23ff6f9d51d870251569e+ahoy@inbound.postmarkapp.com","Name":""}],"Cc":"\"Full name\" <sample.cc@emailDomain.com>, \"Another Cc\" <another.cc@emailDomain.com>","CcFull":[{"Email":"sample.cc@emailDomain.com","Name":"Full name"},{"Email":"another.cc@emailDomain.com","Name":"Another Cc"}],"ReplyTo":"myUsersReplyAddress@theirDomain.com","Subject":"This is an inbound message","MessageID":"22c74902-a0c1-4511-804f2-341342852c90","Date":"Thu, 5 Apr 2012 16:59:01 +0200","MailboxHash":"ahoy","TextBody":"[ASCII]","HtmlBody":"[HTML(encoded)]","Tag":"","Headers":[{"Name":"X-Spam-Checker-Version","Value":"SpamAssassin 3.3.1 (2010-03-16) onrs-ord-pm-inbound1.wildbit.com"},{"Name":"X-Spam-Status","Value":"No"},{"Name":"X-Spam-Score","Value":"-0.1"},{"Name":"X-Spam-Tests","Value":"DKIM_SIGNED,DKIM_VALID,DKIM_VALID_AU,SPF_PASS"},{"Name":"Received-SPF","Value":"Pass (sender SPF authorized) identity=mailfrom; client-ip=209.85.160.180; helo=mail-gy0-f180.google.com; envelope-from=myUser@theirDomain.com; receiver=451d9b70cf9364d23ff6f9d51d870251569e+ahoy@inbound.postmarkapp.com"},{"Name":"DKIM-Signature","Value":"v=1; a=rsa-sha256; c=relaxed\/relaxed;        d=wildbit.com; s=google;        h=mime-version:reply-to:date:message-id:subject:from:to:cc         :content-type;        bh=cYr\/+oQiklaYbBJOQU3CdAnyhCTuvemrU36WT7cPNt0=;        b=QsegXXbTbC4CMirl7A3VjDHyXbEsbCUTPL5vEHa7hNkkUTxXOK+dQA0JwgBHq5C+1u         iuAJMz+SNBoTqEDqte2ckDvG2SeFR+Edip10p80TFGLp5RucaYvkwJTyuwsA7xd78NKT         Q9ou6L1hgy\/MbKChnp2kxHOtYNOrrszY3JfQM="},{"Name":"MIME-Version","Value":"1.0"},{"Name":"Message-ID","Value":"<CAGXpo2WKfxHWZ5UFYCR3H_J9SNMG+5AXUovfEFL6DjWBJSyZaA@mail.gmail.com>"}]}

    def test_valid_postmark_returns200(self):
        response = self.client.post(self.url, content_type='application/json', 
                                    data = json.dumps(self.valid_json))
        self.assertEqual(response.status_code, 200)

    def test_no__postmark_returns400(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 400)

    def test_invalid_postmark_returns400(self):
        response = self.client.post(self.url, content_type='application/json',
                                    data = json.dumps({"foo":"bar"}))
        self.assertEqual(response.status_code, 400)

    def test_GET_returns_405(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        
class SentViewTestCase(TestCase):
    def test_works(self):
        response = self.client.post(reverse('documanager:sent'))
        self.assertEqual(response.status_code, 200)

