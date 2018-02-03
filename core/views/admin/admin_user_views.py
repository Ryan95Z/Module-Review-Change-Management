from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q

from core.views.mixins import AdminTestMixin
from core.forms import UserPermissionsForm, UserCreationForm, SearchForm
from core.models import User


class AdminUserListView(AdminTestMixin, ListView):
    """
    Generic view that will list all users. Inherits
    AdminTestMixin to check that only admins can access this view.
    """
    model = User
    paginate_by = 10

    def get_queryset(self):
        """
        Returns query set for view. If search made then returns
        a filtered list. Otherwise it returns all objects.
        """
        search = self.request.GET.get('search', "")
        if len(search) > 0:
            # search for users by looking at thier
            # username, email, first and last name
            object_list = self.model.objects.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
            return object_list
        return super(AdminUserListView, self).get_queryset()

    def get_context_data(self, *args, **kwargs):
        context = super(AdminUserListView, self).get_context_data()
        context['search_form'] = SearchForm
        return context


class AdminNewUserView(AdminTestMixin, CreateView):
    """
    View for creating a new user
    """
    model = User
    template_name_suffix = '_new_form'
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse('all_users')


class AdminUpdateUserPermissions(AdminTestMixin, UpdateView):
    """
    Update view for allowing users to be updated
    """
    model = User
    template_name_suffix = '_update_form'
    form_class = UserPermissionsForm

    def get_success_url(self):
        return reverse('all_users')
