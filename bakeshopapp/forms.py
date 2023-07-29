from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class ChangeUserDataForm(forms.Form):
	first_name = forms.CharField(
		label="Ваше имя",
		required=True,
		max_length=100,
	)
	last_name = forms.CharField(
		label="Ваша фамилия",
		required=True,
		max_length=100,
	)
	phone_number = forms.CharField(
		label="Ваш телефон",
		required=True,
		max_length=12,
	)
	address = forms.CharField(
		label="Ваш адрес",
		required=False,
		max_length=250,
	)
