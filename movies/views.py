from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from .models import Movie
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from random import random, sample

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


@login_required
@require_GET
def recommended2(request):
    return render(request, 'movies/recommended2.html')


@login_required
@require_GET
def mvti(request):
    answer = request.GET.get('answer')
    movies = ''
    if answer == '1':
        movies = Movie.objects.filter(release_date__year__lte=1999).order_by('?')[:10]
    elif answer == '2':
        movies = Movie.objects.order_by('-vote_average')[:10]
    elif answer == '3':
        movies = Movie.objects.order_by('popularity')[:10]
    else:
        movies = Movie.objects.order_by('?')[:10]

    movies_list = []
    for movie in movies:
        movies_list.append({
            'title': movie.title,
            'release_date': movie.release_date,
            'vote_average': movie.vote_average,
            'poster_path': movie.poster_path,
            })
    response = {
        'moviesList': movies_list,
    }
    return JsonResponse(response)
    