from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from core.views.mixins import LoggedInTestMixin
from core.forms import LoginForm


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
                messages.add_message(request, messages.ERROR,
                                     'Invalid login details')
                return redirect('login')
        # invalid form
        messages.add_message(request, messages.ERROR, 'Invalid login details')
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
        messages.add_message(request, messages.SUCCESS,
                             'Successfully logged out')
        return redirect('login')
