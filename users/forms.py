from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
	username = forms.CharField(label="Никнейм")
	password = forms.CharField(label="Пароль",
								widget=forms.PasswordInput)
	password2 = forms.CharField(label="Повторите пароль",
								widget=forms.PasswordInput)
	class Meta:
		model = User
		fields =('username',)

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password'] != cd['password2']:
			raise forms.ValidationError("Пароли не совпадают")
		return cd['password2']

	def clean_username(self):
		cd = self.cleaned_data
		if str(User.objects.filter(username=cd["username"]))!="<QuerySet []>":
			raise forms.ValidationError("Такой никнейм уже занят")
		return cd['username']

class LoginForm(forms.Form):
	username = forms.CharField(label="Никнейм")
	password = forms.CharField(label="Пароль",
								widget=forms.PasswordInput)