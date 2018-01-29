from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from core.views.mixins import UserOnlyMixin
from core.forms import UserDetailsForm, UserPasswordForm
from core.models import User


class UserSettingsView(UserOnlyMixin, TemplateView):
    """
    Generic view to render user settings template
    """
    template_name = 'core/user_settings.html'


class UserUpdateDetailsView(UserOnlyMixin, UpdateView):
    """
    View that enables users to update thier persoanl
    information by rendering a form.
    """
    model = User
    form_class = UserDetailsForm
    slug_field = 'username'
    template_name = "core/user_details.html"

    def get_context_data(self, **kwargs):
        context = super(UserUpdateDetailsView, self).get_context_data(**kwargs)
        return context

    def get_success_url(self, **kwargs):
        return reverse('user_settings', kwargs={'slug': self.object.username})


class UserUpdatePasswordView(UserOnlyMixin, View):
    """
    View to enable users to update thier passwords
    by rendering a form.
    """
    def __init__(self):
        super(UserUpdatePasswordView, self).__init__()
        self.form = UserPasswordForm

    def get(self, request, slug):
        """
        GET request that will display the form
        """
        context = {'form': self.form}
        return render(request, "core/user_password.html", context)

    def post(self, request, *args, **kwargs):
        """
        POST request that will process and upate the user's
        password if valid.
        """
        form = self.form(request.POST)
        slug = kwargs['slug']
        if form.is_valid():
            # update the password
            user = form.update_password(request.user.id)
            if user is None:
                # if password was not updated
                # create a message to the UI.
                messages.add_message(request, messages.ERROR,
                                     'Invalid passwords provided')
                return redirect('user_password', slug)
            else:
                # password was succesfully updated
                messages.add_message(request, messages.SUCCESS,
                                     'Password changed successfully')
                # update the auth hash to validate the current session
                update_session_auth_hash(request, user)
                return redirect('user_settings', slug)
        else:
            # form was not valid
            # push mesage ot UI.
            messages.add_message(request, messages.ERROR,
                                 'Invalid passwords provided')
            return redirect('user_password', slug)
