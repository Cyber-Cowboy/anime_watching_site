from django.shortcuts import render

from .models import Title 
def index(request):
	return latestAnime(request)

def latestAnime(request):
	latest_anime_titles = Title.objects.order_by("-created")[:5]
	return render(request, 'anime_titles/latest_anime.html',{"anime_titles":latest_anime_titles})