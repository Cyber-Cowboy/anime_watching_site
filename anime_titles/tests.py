from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

import datetime

from .models import Title

def create_title(title_name, created=None):
	if not created: created = timezone.now()
	return Title.objects.create(title_name=title_name,
		created=created,poster="image.com/image.jpg")

class LatestTitlesTests(TestCase):
	def test_no_titles(self):
		"""
		If no titles available, something is displayed
		""" 
		response = self.client.get(reverse('anime_titles:latest'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No anime yet")
		self.assertQuerysetEqual(response.context["anime_titles"],[])

	def test_only_part_of_all_anime_displayes(self):
		"""
		Tests that only five of six created titles are displayed
		"""
		N = 5 #titles on front page
		a1 = [create_title(str(i)) for i in range(0,N+1)]
		response = self.client.get(reverse('anime_titles:latest'))
		a2 = [i for i in response.context["anime_titles"]]
		self.assertEqual(a2, a1[:N])

	def test_right_order(self):
		"""
		Tests that the order is from newest to the oldest
		"""
		N = 5 #titles on front page
		a1 = [create_title(str(i), created=(timezone.now()+datetime.timedelta(seconds=1))) for i in range(0,N)]
		response = self.client.get(reverse('anime_titles:latest'))
		a2 = [i for i in response.context["anime_titles"]]
		self.assertEqual(a2, a1)



class IndexTitlesPageTests(TestCase):
	def test_index_redirects_control_to_latest(self):
		"""
		latest and index returns the same output
		"""
		indexResponse = self.client.get(reverse('anime_titles:index'))
		latestResponse = self.client.get(reverse('anime_titles:latest'))
		self.assertEqual(indexResponse.content, latestResponse.content)