from django.views import View
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.contrib.auth import (authenticate, login, logout)

from core.forms import LoginForm
from core.models import User
from .mixins import (AdminTestMixin, LoggedInTestMixin)

class LoginView(LoggedInTestMixin, View):
	def get(self, request):
		next_url = request.GET.get('next', None)
		context = {'form' :  LoginForm(), 'next' : next_url}
		return render(request, 'core/login.html', context)

	def post(self, request, *args, **kwargs):
		form = LoginForm(request.POST)
		next_url = request.GET.get('next', None)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			auth = authenticate(username=username, password=password)
			if auth is not None:
				login(request, auth)
				if next_url:
					return HttpResponseRedirect(next_url)
				return redirect('dashboard')
			else:
				return redirect('login')
		return redirect('login')


class LogoutView(View):
	def get(self, request):
		logout(request)
		return redirect('login')


class UserListView(AdminTestMixin, ListView):
	model = User

	def get_context_data(self, **kwargs):
		context = super(UserListView, self).get_context_data(**kwargs)
		return context