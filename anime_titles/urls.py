from django.urls import path

from . import views

app_name="anime_titles"
urlpatterns = [
	path('', views.index, name="index"),
	path('latest/', views.index, name="latest"),
]