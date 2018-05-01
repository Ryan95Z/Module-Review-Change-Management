from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from forms.views import *
from recommenderSystem.views import *


urlpatterns = [
    # software recommender urls
    url(r'^software-search/$', login_required(
        searchBar.as_view()), name='software_search'),
]
