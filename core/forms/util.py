from django import forms
from django.forms.widgets import TextInput


class SearchForm(forms.Form):
    search = forms.CharField(
        max_length=40,
        widget=TextInput(attrs={
            'class': "form-control mr-sm-2",
            'type': 'search',
            'placeholder': 'Search'
            }))
