"""
    starwars URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin

from starwars.views import Movies, MovieCreate, MovieUpdate, MovieDetail

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', Movies.as_view(), name='home'),
    url(r'^movie/create/', MovieCreate.as_view(), name='movie_create'),
    url(r'^movie/edit/(?P<pk>\d+)$', MovieUpdate.as_view(), name='movie_edit'),
    url(r'^movie/(?P<pk>\d+)$', MovieDetail.as_view(), name='movie'),
]
