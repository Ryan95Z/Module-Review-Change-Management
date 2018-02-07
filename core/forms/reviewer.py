from django import forms
from core.models import Reviewer, Module, User

class ReviewerCreationForm(forms.ModelForm):
    """
    Form to create a new reviewer
    """

    class Meta:
        model = Reviewer
        fields = ['user', 'modules']

    attrs = {'class': 'form-control'}
    user = forms.ModelChoiceField(
        queryset = User.objects.all()
    )
    modules = forms.ModelMultipleChoiceField(
        queryset = Module.objects.all()
    )
