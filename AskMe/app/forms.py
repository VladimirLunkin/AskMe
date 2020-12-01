from django import forms
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from app.models import Question, Answer, Tag, Profile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)


class AskForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text']


class TagForm(forms.Form):
    tags = forms.CharField(required=False)


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']


class SignupForm(forms.ModelForm):
    password_check = forms.CharField(required=True)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class SettingsForm(forms.Form):
    username = forms.CharField(required=False)
    email = forms.CharField(required=False)
    password = forms.CharField(required=False)
    password_check = forms.CharField(required=False)
    avatar = forms.ImageField(required=False)
