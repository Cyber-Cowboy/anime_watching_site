from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Title, TitleInList 

class LatestView(generic.ListView):
	template_name = "anime_titles/latest_anime.html"
	context_object_name = "anime_titles"

	def get_queryset(self):
		return Title.objects.order_by('-created')[:5]

class TitleView(generic.DetailView):
	template_name = "anime_titles/detail.html"
	model = Title

@login_required
@require_http_methods(["POST"])
def add_title_to_list(request):
	anime_list = request.user.animelist
	title = Title.objects.get(pk=request.POST["title"])
	status = request.POST["status"]
	episode_count = request.POST["episode_count"]
	old_title = TitleInList.objects.filter(anime_list=anime_list, title=title)
	if old_title:
		old_title = old_title[0]
		old_title.status = status
		old_title.episode_count = episode_count
		old_title.save()
	else:
		TitleInList(anime_list=anime_list, title=title, status=status, episode_count=episode_count).save()
	return HttpResponseRedirect(reverse("anime_titles:detail",kwargs={"pk":title.id}))
