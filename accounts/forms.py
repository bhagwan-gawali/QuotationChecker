from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.fields['acc_type'].widget.attrs.update({'class': 'form-select'})
		self.fields['username'].widget.attrs.update({'class': 'form-control'})
		self.fields['email'].widget.attrs.update({'class': 'form-control'})
		self.fields['password1'].widget.attrs.update({'class': 'form-control'})
		self.fields['password2'].widget.attrs.update({'class': 'form-control'})

		for field_name in ['username', 'password1', 'password2']:
			self.fields[field_name].help_text = None


	class Meta:
		model = CustomUser
		fields = ['email', 'username', 'acc_type', ]

class CustomUserChangeForm(UserChangeForm):

	class Meta:
		model = CustomUser
		fields = ['email', 'username', ]


class CustomLoginForm(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.fields['username'].widget.attrs.update({'class': 'form-control'})
		self.fields['password'].widget.attrs.update({'class': 'form-control'})
