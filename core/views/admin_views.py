from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView

from .mixins import AdminTestMixin
from core.forms import UserPermissionsForm
from core.models import User


class UserListView(AdminTestMixin, ListView):
    """
    Generic view that will list all users. Inherits
    AdminTestMixin to check that only admins can access this view.
    """
    model = User

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        return context


class AdminUpdateUserPermissions(UpdateView):
    """
    Update view for allowing users to be updated
    """
    model = User
    template_name_suffix = '_update_form'
    form_class = UserPermissionsForm

    def get_context_data(self, **kwargs):
        context = super(
            AdminUpdateUserPermissions, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy('all_users')
