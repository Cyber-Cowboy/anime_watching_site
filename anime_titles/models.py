from django.db import models
from taggit.managers import TaggableManager
from django.conf import settings
from django.urls import reverse

class Title(models.Model):
	title_name = models.CharField(max_length=200)
	created = models.DateTimeField("First episode")
	poster = models.CharField(max_length=500)
	rating = models.IntegerField(default=0)
	tags = TaggableManager()
	
	def count_rating(self):
		rates = TitleInList.objects.filter(title=self,rated=True)
		self.rating = sum([title.rating for title in rates])/rates.count()
		self.save()
		return self.rating
	def get_absolute_url(self):
		return reverse("anime_titles:detail",
			args=[self.id])
	def __str__(self):
		return self.title_name

class Episode(models.Model):
	title = models.ForeignKey(Title, on_delete=models.CASCADE)
	number = models.IntegerField()

	def __str__(self):
		return self.title.title_name + " " + str(self.number)

class Translation(models.Model):
	episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
	author = models.CharField(max_length=200, blank=True)
	url = models.CharField(max_length=500, blank=True) 

	def __str__(self):
		return self.author + " " + self.episode.__str__()

class AnimeList(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL,
								on_delete=models.CASCADE,
								related_name="animelist")
	def __str__(self):
		return f'AnimeList of user: {self.user.username}'

class TitleInList(models.Model):
	anime_list = models.ForeignKey(AnimeList, on_delete=models.CASCADE)
	title = models.ForeignKey(Title, on_delete=models.CASCADE)
	episode_count = models.IntegerField(default=0)
	status_choices=[
	("WG","смотрю"),
	("WD","просмотренно"),
	("PL","запланировано"),
	("DP","брошено")]
	status = models.CharField(max_length=2, choices=status_choices, default="PL")
	rated = models.BooleanField(default=False)
	rating = models.IntegerField(default=0)