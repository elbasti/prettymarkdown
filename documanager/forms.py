from django import forms
from documanager.models import Stationary

class MarkdownForm(forms.Form):
    markdown_input = forms.CharField(widget = forms.Textarea)
    stationary = forms.ModelChoiceField(queryset = Stationary.objects.all(), 
                 empty_label = None)
