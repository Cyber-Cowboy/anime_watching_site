from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile

def register_user(username="JoJo", password="password"):
	user = User.objects.create_user(username=username,
									password=password)
	user.save()
	Profile(user=user).save()
	return user

class UserAuthTest(TestCase):

	def test_registration(self):
		nickname = "Jhon"
		response = self.client.post(reverse("users:register"), {"username":nickname, "password":"password", "password2":"password"})
		user = User.objects.get(username=nickname)
		self.assertEqual(nickname, user.username)

	def test_return_errormessage_if_username_taken(self):
		nickname = "Jhon"
		response1 = self.client.post(reverse("users:register"), {"username":nickname, "password":"password", "password2":"password"})
		response2 = self.client.post(reverse("users:register"), {"username":nickname, "password":"password", "password2":"password"})
		self.assertEqual(response2.status_code, 200) #It's not a redirect or error page
		self.assertTrue("errorlist" in str(response2.content)) 
		
	def test_user_cannot_login_with_wrong_password(self):
		username = "Jhon"
		user = register_user(username=username, password="123")
		response = self.client.post(reverse("users:login"), {"username":username,
											"password":"321"})
		self.assertTrue("error" in str(response.content))

	def test_user_cant_rate_anime_without_auth(self):
		response2 = self.client.post(reverse("anime_titles:rate_title"), {})
		self.assertEqual(response2.status_code,302)