from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from .models import Movie
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.
@require_GET
def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)


@require_GET
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    context = {
        'movie': movie,
    }
    return render(request, 'movies/detail.html', context)

@login_required
@require_GET
def recommended(request):
    today_month = datetime.today().month
    movies = Movie.objects.filter(release_date__month=today_month)
    from_now = dict()
    for movie in movies:
        from_now[movie.pk] = datetime.today().year-movie.release_date.year
    context = {
        'today_month': today_month,
        'movies': movies,
        'from_now': from_now,
    }
    return render(request, 'movies/recommended.html', context)
    