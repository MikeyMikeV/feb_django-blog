from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=256, required=True, help_text='Required', label="Адрес электронной почты")
    class Meta:
        model=User
        fields = ('email', 'username', 'password1', 'password2')