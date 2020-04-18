from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.utils import IntegrityError


def register_view(request):
	template = "users/register.html"
	if request.user.is_authenticated:
		return render(request, template, {"error_message":"You are already logged in as "+request.user.username})
	if request.method == "POST":
		try:
			user = User.objects.create_user(username = request.POST["nickname"],
			password = request.POST["password"])
			user.save()
		except IntegrityError as e:
			return render(request, template, {"error_message":e})

		login(request, user)
		return HttpResponseRedirect(reverse("anime_titles:index"))
	else:
		return render(request, template,{})

def login_view(request):
	template = "users/login.html"
	if request.user.is_authenticated:
		return render(request, template, {"error_message":"You are already logged in as "+request.user.username})
	if request.method == "POST":
		username = request.POST['nickname']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse("anime_titles:index"))
		else:
			return render(request, template, {"error_message":"invalid login"})
	else:
		return render(request, template)

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse("anime_titles:index"))