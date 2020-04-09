from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

import datetime

from .models import Title, Episode, Translation

def create_title(title_name="JoJo", created=None, poster="image.com/image.jpg"):
	if not created: created = timezone.now()
	return Title.objects.create(title_name=title_name,
		created=created,poster=poster)

def create_episode(title=None, number=1):
		if title==None:
			title=create_title()
		return Episode.objects.create(title=title, number=number)

def create_translation(episode=None, author="KalaBanga", url="#"):
		if episode==None:
			episode=create_episode()
		return Translation.objects.create(episode=episode, author=author, url=url)

class LatestTitlesTests(TestCase):
	def test_no_titles(self):
		"""
		If no titles available, something is displayed
		""" 
		response = self.client.get(reverse('anime_titles:latest'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No anime yet")
		self.assertQuerysetEqual(response.context["anime_titles"],[])

	def test_only_part_of_all_anime_displays(self):
		"""
		Tests that only five of six created titles are displayed
		"""
		N = 5 #titles on front page
		a1 = [create_title(str(i)) for i in range(0,N+1)]
		response = self.client.get(reverse('anime_titles:latest'))
		a2 = [i for i in response.context["anime_titles"]]
		self.assertEqual(len(a1[:N]), len(a2))

	def test_right_order(self):
		"""
		Tests that the order is from newest to the oldest
		"""
		N = 5 #titles on front page
		a1 = [create_title(str(i), created=(timezone.now()-datetime.timedelta(days=i))) for i in range(0,N)]
		response = self.client.get(reverse('anime_titles:latest'))
		a2 = [i for i in response.context["anime_titles"]]
		self.assertEqual(a1, a2)

class DetailTitleTests(TestCase):
	def test_can_create_title_and_open_it_later(self):
		name = "JoJo"
		response = self.client.get(reverse('anime_titles:detail', args=(create_title(name).id,)))
		self.assertContains(response, "<title>"+name+"</title>")

	def test_can_create_title_with_multiple_episodes(self):
		title = create_title()
		episode1 = create_episode(title=title, number=1)
		episode2 = create_episode(title=title, number=2)
		response = self.client.get(reverse('anime_titles:detail', args=(title.id,)))
		self.assertContains(response, episode1.number)
		self.assertContains(response, episode2.number)

	def test_can_create_episode_with_multiple_translations(self):
		episode = create_episode()
		trans1 = create_translation(episode=episode, author="KalaBanga")
		trans2 = create_translation(episode=episode, author="BangaKala")
		response = self.client.get(reverse('anime_titles:detail', args=(episode.title.id,)))
		self.assertContains(response, trans1.author)
		self.assertContains(response, trans2.author)

class IndexTitlesPageTests(TestCase):
	def test_index_redirects_control_to_latest(self):
		"""
		latest and index returns the same output
		"""
		indexResponse = self.client.get(reverse('anime_titles:index'))
		latestResponse = self.client.get(reverse('anime_titles:latest'))
		self.assertEqual(indexResponse.content, latestResponse.content)