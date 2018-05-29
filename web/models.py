from django.db import models

from web.sparql_query import get_contributors_for_movie, get_movies_for_contributor, get_genres_for_contributor, get_movies_for_genre

class Movie(models.Model):
	name = models.CharField(max_length=128, unique=True)
	loaded = models.BooleanField(default=False)

	contributors = models.ManyToManyField(to='Contributor', related_name='movies')

	def __str__(self):
		return self.name

	def load(self):
		if self.loaded:
			return

		for obj in get_contributors_for_movie(self.name):
			genre, created = Genre.objects.get_or_create(name=obj["genre"])
			contributor, created = Contributor.objects.get_or_create( name=obj["contributor"])
			self.contributors.add(contributor)
			genre.contributors.add(contributor)

		self.loaded = True
		self.save()

class Genre(models.Model):
	name = models.CharField(max_length=128, unique=True)
	loaded = models.BooleanField(default=False)

	@property
	def movies(self):
		return Movie.objects.filter(contributors__in=self.contributors.all()).distinct()

	def __str__(self):
		return self.name

	def load(self):
		if self.loaded:
			return

		for obj in get_movies_for_genre(self.name):
			movie, created = Movie.objects.get_or_create(name=obj['movie'])
			contributor, created = Contributor.objects.get_or_create(name=obj['contributor'])
			contributor.movies.add(movie)
			self.contributors.add(contributor)

		self.loaded = True
		self.save()

class Contributor(models.Model):
	name = models.CharField(max_length=128, unique=True)
	loaded = models.BooleanField(default=False)

	genres = models.ManyToManyField(to=Genre, related_name='contributors')

	def __str__(self):
		return self.name

	def load(self):
		if self.loaded:
			return

		for obj in get_movies_for_contributor(self.name):
			movie, created = Movie.objects.get_or_create(name=obj['movie'])
			self.movies.add(movie)

		for obj in get_genres_for_contributor(self.name):
			genre, created = Genre.objects.get_or_create(name=obj['genre'])
			self.genres.add(genre)

		self.loaded = True
		self.save()
