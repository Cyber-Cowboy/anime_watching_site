from django.urls import path

from . import views

app_name="anime_titles"
urlpatterns = [
	path('', views.LatestView.as_view(), name="index"),
	path('latest/', views.LatestView.as_view(), name="latest"),
	path('popular/', views.popular_titles_page, name="popular"),
	path('get_popular/', views.popular_titles_load, name="get_popular"),
	path('<int:pk>/detail/', views.TitleView.as_view(), name="detail"),
	path('add_title/', views.add_title_to_list, name="add_title_to_list"),
	path('rate_title/', views.rate_title, name="rate_title")
]