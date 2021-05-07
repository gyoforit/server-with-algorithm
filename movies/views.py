from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from .models import Movie
from datetime import datetime


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


@require_GET
def recommended(request):
    # 출시월이 현재 검색하는 달과 같은 영화를 추천해주려 한다.
    today = datetime.today()
    movies = Movie.objects.filter(release_date__month=today)
    
    context = {
        'today': today,
        'movies': movies,
    }

    return render(request, 'movies/recommended.html', context)
    