from django import forms

class MarkdownForm(forms.Form):
    markdown_input = forms.CharField(widget = forms.Textarea)
    letterhead = forms.ChoiceField()
