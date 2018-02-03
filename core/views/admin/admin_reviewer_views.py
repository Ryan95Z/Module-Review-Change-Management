from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render

from core.views.mixins import AdminTestMixin
from core.forms import ReviewerCreationForm
from core.models import User, Reviewer


class AdminReviewerListView(AdminTestMixin, ListView):
    """
    Generic view that lists all of the current reviewers
    in the system.
    """
    model = Reviewer


class AdminReviewerCreateView(AdminTestMixin, CreateView):
    """
    View to create reviewer
    """
    model = Reviewer
    form_class = ReviewerCreationForm

    #fields = ['user', 'modules']

    def get_success_url(self):
        return reverse('all_reviewers')


class AdminReviewerUpdateView(AdminTestMixin, UpdateView):
    """
    View to update existing reviewer
    """
    model = Reviewer
    fields = ['modules', 'user']

    def get_form(self, *args, **kwargs):
        form = super(AdminReviewerUpdateView, self).get_form(*args, **kwargs)
        # limit drop down to only contain those with reviewer permission
        form.fields['user'].queryset = User.objects.filter(
            is_module_reviewer=True)
        return form

    def get_context_data(self, **kwargs):
        kwargs = {'pk': self.object.id}
        context = super(
            AdminReviewerUpdateView, self).get_context_data(**kwargs)
        # url for form action
        context['form_url'] = reverse('update_reviewer', kwargs=kwargs)
        # button text
        context['form_type'] = 'Update'
        return context

    def get_success_url(self):
        return reverse('all_reviewers')

class AdminReviewerDeleteView(AdminTestMixin, DeleteView):
    """
    View to delete and existing reviewer
    """
    model = Reviewer

    def get_success_url(self):
        return reverse("all_reviewers")

