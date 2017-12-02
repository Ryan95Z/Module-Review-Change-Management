from django.conf.urls import url
from core.views import (LoginView, LogoutView, UserListView)

urlpatterns = [
	url(r'^login/', LoginView.as_view(), name='login'),
	url(r'^logout/', LogoutView.as_view(), name='logout'),
	url(r'^all/', UserListView.as_view(), name='all_users'),
]