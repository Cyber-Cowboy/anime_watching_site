from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from .models import Title, TitleInList 
from .forms import RatingForm
import json

class LatestView(generic.ListView):
	template_name = "anime_titles/latest_anime.html"
	context_object_name = "anime_titles"
	queryset = Title.objects.order_by('-created')
	paginate_by = 10

def popular_titles_page(request):
	return render(request,"anime_titles/popular.html", {})

def popular_titles_load(request):
	title_per_page = 20
	current_page = int(request.GET["current_page"])
	queryset = Title.objects.order_by('rating')[current_page*title_per_page:(current_page+1)*title_per_page]
	titles = [{
	"name":title.title_name,
	"url":title.get_absolute_url(),
	"poster":title.poster} for title in queryset]
	return HttpResponse(json.dumps(titles))
"""
class TitleView(generic.DetailView):
	template_name = "anime_titles/detail.html"
	model = Title
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['rating_form'] = RatingForm()
		return context
"""

def title_detail(request, pk):
	template = "anime_titles/detail.html"
	title = get_object_or_404(Title, pk=pk)
	personal_rating = None
	if request.user.is_authenticated:
		rated = TitleInList.objects.get(anime_list=request.user.animelist, title=title)
		if rated.rated:
			personal_rating = rated.rating
	context = {"title":title, "personal_rating":personal_rating,}
	return render(request,template,context)
	
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