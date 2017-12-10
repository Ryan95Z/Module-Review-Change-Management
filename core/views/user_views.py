from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout)
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy

from .mixins import (UserOnlyMixin, LoggedInTestMixin)
from core.forms import LoginForm, UserDetailsForm, UserPasswordForm
from core.models import User


class LoginView(LoggedInTestMixin, View):
    """
    Class that allows users to access the login page.
    Inherits LoggedInTestMixin to determine where to
    route the user if they are already logged in.
    """

    def get(self, request):
        """
        Get method for view that will provide login form.
        """
        next_url = request.GET.get('next', None)
        context = {'form':  LoginForm(), 'next': next_url}
        return render(request, 'core/login.html', context)

    def post(self, request, *args, **kwargs):
        """
        Post method that will enable users to login
        if the details provided are correct. Will then
        redirect to correct view.
        """
        form = LoginForm(request.POST)
        next_url = request.GET.get('next', None)
        # check that the form is valid
        if form.is_valid():
            # clean the user's information
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            auth = authenticate(username=username, password=password)
            if auth is not None:
                # login user and route
                login(request, auth)
                request.session['username'] = username
                request.session['user_pk'] = auth.id
                if next_url:
                    return HttpResponseRedirect(next_url)
                return redirect('dashboard')
            else:
                # details incorrect
                return redirect('login')
        # invalid form
        return redirect('login')


class LogoutView(View):
    """
    View to allow users to log out of system
    """
    def get(self, request):
        """
        Get method that will logout a user
        and redirect to login page.
        """
        logout(request)
        try:
            del request.session['username']
            del request.session['user_pk']
        except KeyError:
            pass
        return redirect('login')


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
            changed = form.update_password(request.user.id)
            if not changed:
                # if password was not updated
                # create a message to the UI.
                messages.add_message(request, messages.ERROR,
                                     'Invalid passwords provided')
                return redirect('user_password', slug)
            else:
                # password was succesfully updated
                messages.add_message(request, messages.SUCCESS,
                                     'Password changed successfully')
                return redirect('user_settings', slug)
        else:
            # form was not valid
            # push mesage ot UI.
            messages.add_message(request, messages.ERROR,
                                 'Invalid passwords provided')
            return redirect('user_password', slug)
