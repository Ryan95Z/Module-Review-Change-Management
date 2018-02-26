from django import forms
from django.forms.widgets import Textarea
from timeline.models import Discussion


class DiscussionForm(forms.Form):
    css_attr = {
        'class': 'form-control',
        'placeholder': 'Add your comments here. Markdown is active.',
        'rows': 4,
    }
    comment = forms.CharField(required=True, widget=Textarea(attrs=css_attr))
