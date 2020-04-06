from django.db import models

class Title(models.Model):
	title_name = models.CharField(max_length=200)
	created = models.DateTimeField("First episode")
	poster = models.CharField(max_length=500)
	
	def __str__(self):
		return self.title_name