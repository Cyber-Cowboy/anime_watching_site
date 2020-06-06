from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

def register_user(username="JoJo", password="password"):
	user = User.objects.create_user(username=username,
									password=password)
	user.save()
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
	
	def test_return_error_if_logged_user_try_to_login(self):
		"""Login user using django then check if login page show error message"""
		username = "Jhon"
		password = "password"
		user = register_user(username=username, password=password)
		self.client.login(username=username, password=password)
		response = self.client.get(reverse("users:login"))
		self.assertTrue("error" in str(response.content))
	
	def test_login(self):
		"""Login user using view then check if login page show error message"""
		username = "Jhon"
		password = "password"
		user = register_user(username=username, password=password)
		response = self.client.post(reverse("users:login"), {"username":username,
												"password":password})
		response2 = self.client.get(reverse("users:login"))
		self.assertTrue("error" in str(response2.content))

	def test_user_cannot_login_with_wrong_password(self):
		username = "Jhon"
		user = register_user(username=username, password="123")
		response = self.client.post(reverse("users:login"), {"username":username,
											"password":"321"})
		self.assertTrue("error" in str(response.content))