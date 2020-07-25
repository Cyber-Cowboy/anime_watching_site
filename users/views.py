from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.db.utils import IntegrityError
from django.views import generic
from .forms import LoginForm, UserRegistrationForm
from .models import Profile
from anime_titles.models import TitleInList, AnimeList

def register_view(request):
	template = "users/register.html"
	user_form = UserRegistrationForm()
	if request.user.is_authenticated:
		messages.error(request,"Вы уже зашли под именем "+request.user.username)

	if request.method == "POST":
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			new_user = user_form.save(commit=False)
			new_user.set_password(
				user_form.cleaned_data['password'])
			new_user.save()
			Profile(user=new_user).save()
			AnimeList(user=new_user).save()
			return HttpResponseRedirect(reverse("users:login"))
	return render(request, template,
				{"form":user_form})

def login_view(request):
	template = "users/login.html"
	form = LoginForm()
	if request.user.is_authenticated:
		messages.error(request,"Вы уже зашли под именем "+request.user.username)
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(request, 
								username=cd['username'], 
								password=cd['password'])
			if user is not None:
				login(request, user)
				return HttpResponseRedirect(reverse("anime_titles:index"))
			else:
				messages.error(request,"Неверное имя или пароль")
				return render(request, template, {"form":form})
	else:
		form = LoginForm()
	return render(request, template, {"form":form})

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse("anime_titles:index"))

class ProfileView(generic.DetailView):
	template_name = "users/profile.html"
	model = Profile
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		profile = Profile.objects.get(pk=self.kwargs['pk'])
		context['titles'] = TitleInList.objects.filter(anime_list=profile.user.animelist)
		return context