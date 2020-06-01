from django.db import models
from taggit.managers import TaggableManager

class Title(models.Model):
	title_name = models.CharField(max_length=200)
	created = models.DateTimeField("First episode")
	poster = models.CharField(max_length=500)
	tags = TaggableManager()
	
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