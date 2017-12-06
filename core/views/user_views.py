from django.views import View
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.contrib.auth import (authenticate, login, logout)

from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy

from core.forms import LoginForm, UserForm
from core.models import User
from .mixins import (AdminTestMixin, LoggedInTestMixin)


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
        return redirect('login')


class UserListView(AdminTestMixin, ListView):
    """
    Generic view that will list all users. Inherits
    AdminTestMixin to check that only admins can access this view.
    """
    model = User

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        return context


class UserUpdateView(UpdateView):
    model = User
    template_name_suffix = '_update_form'
    form_class = UserForm

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy('all_users')


# class UserDetailView(View):
#     def get(self, request, user_id):
#         user = get_object_or_404(User, pk=user_id)
#         context = {'user': user}
#         return render(request, 'core/user_details.html', context)
