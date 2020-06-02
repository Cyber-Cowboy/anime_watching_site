from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.utils import IntegrityError
from .forms import LoginForm, UserRegistrationForm

def register_view(request):
	template = "users/register.html"
	errors = []
	user_form = UserRegistrationForm()
	if request.user.is_authenticated:
		errors.append("Вы уже зашли поди именем "+request.user.username)
		return render(request, template, {"form":user_form,"error_messages":errors})

	if request.method == "POST":
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			new_user = user_form.save(commit=False)
			new_user.set_password(
				user_form.cleaned_data['password'])
			new_user.save()
			return HttpResponseRedirect(reverse("users:login"))
	return render(request, template,
				{"form":user_form,"errors":errors})

def login_view(request):
	template = "users/login.html"
	errors = []
	form = LoginForm()
	if request.user.is_authenticated:
		errors.append("Вы уже зашли поди именем "+request.user.username)
		return render(request, template, {"form":form,"error_messages":errors})
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
				errors.append("invalid login")
				return render(request, template, {"form":form,"error_messages":errors})
	else:
		form = LoginForm()
	return render(request, template, {"form":form, "error_messages":errors})

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse("anime_titles:index"))