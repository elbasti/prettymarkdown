# Test for Documanager's forms
from django.test import TestCase
from django import forms
from documanager.forms import MarkdownForm

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

