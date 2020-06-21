from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Title, TitleInList 
from .forms import RatingForm

class LatestView(generic.ListView):
	template_name = "anime_titles/latest_anime.html"
	context_object_name = "anime_titles"
	queryset = Title.objects.order_by('-created')
	paginate_by = 5

class TitleView(generic.DetailView):
	template_name = "anime_titles/detail.html"
	model = Title
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['rating_form'] = RatingForm()
		return context

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
		messages.success(request,"сохранено")
	else:
		TitleInList(anime_list=anime_list, title=title, status=status, episode_count=episode_count).save()
		messages.success(request,"добавлено")
	return HttpResponseRedirect(reverse("anime_titles:detail",kwargs={"pk":title.id}))

@login_required
@require_http_methods(["POST"])
def rate_title(request):
	title = Title.objects.get(pk=request.POST["title"])
	title_in_list = TitleInList.objects.filter(anime_list=request.user.animelist, title=title)
	form = RatingForm(request.POST)
	if form.is_valid():
		if title_in_list:
			title_in_list = title_in_list.first()
			title_in_list.rated = True
			title_in_list.rating = form.cleaned_data["rating"]
			title_in_list.save()
			title.count_rating()
			messages.success(request,"оценено")
		else:
			messages.error(request,"Добавьте аниме в список, перед тем как его оценить")
	return HttpResponseRedirect(reverse("anime_titles:detail",kwargs={"pk":title.id}))