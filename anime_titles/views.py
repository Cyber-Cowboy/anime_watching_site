from django.shortcuts import render
from django.views import generic

from .models import Title 

class LatestView(generic.ListView):
	template_name = "anime_titles/latest_anime.html"
	context_object_name = "anime_titles"

	def get_queryset(self):
		return Title.objects.order_by('-created')[:5]

class TitleView(generic.DetailView):
	template_name = "anime_titles/detail.html"
	model = Title