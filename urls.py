from django.conf.urls import url
from django.contrib import admin

from web.views import SearchView, MovieView, ContributorView, GenreView

urlpatterns = [
	url(r'^$', SearchView.as_view(), name='search'),
	url(r'^movie/(?P<name>.+)$', MovieView.as_view(), name='movie-detail'),
	url(r'^contributor/(?P<name>.+)$', ContributorView.as_view(), name='contributor-detail'),
	url(r'^genre/(?P<name>.+)$', GenreView.as_view(), name='genre-detail'),
]
