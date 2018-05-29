from django.http import HttpResponseRedirect
from django.urls import reverse

from django.views.generic import FormView, TemplateView

from web.forms import SearchForm
from web.models import Movie, Contributor, Genre

class SearchView(FormView):
	template_name = 'search.html'
	form_class = SearchForm

	def form_valid(self, form):
		if len(form.data['movie_name']) > 0:
			movie, created = Movie.objects.get_or_create(name=form.data['movie_name'])
			return HttpResponseRedirect(reverse('movie-detail', kwargs={ 'name': movie.name }))
		elif len(form.data['genre_name']) > 0:
			genre, created = Genre.objects.get_or_create(name=form.data['genre_name'])
			return HttpResponseRedirect(reverse('genre-detail', kwargs={ 'name': genre.name }))
		elif len(form.data['contributor_name']) > 0:
			contributor, created = Contributor.objects.get_or_create(name=form.data['contributor_name'])
			return HttpResponseRedirect(reverse('contributor-detail', kwargs={ 'name': contributor.name }))

class MovieView(TemplateView):
	template_name = 'movie.html'

	def get_context_data(self, **kwargs):
		movie = Movie.objects.get(name=kwargs['name'])
		movie.load()
		kwargs.update({ 'object': movie })
		return super().get_context_data(**kwargs)

class ContributorView(TemplateView):
	template_name = 'contributor.html'

	def get_context_data(self, **kwargs):
		contributor = Contributor.objects.get(name=kwargs["name"])
		contributor.load()
		kwargs.update({ 'object': contributor })
		return super().get_context_data(**kwargs)

class GenreView(TemplateView):
	template_name = 'genre.html'

	def get_context_data(self, **kwargs):
		genre = Genre.objects.get(name=kwargs['name'])
		genre.load()
		kwargs.update({ 'object': genre })
		return super().get_context_data(**kwargs)
