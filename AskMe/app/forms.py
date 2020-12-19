from django import forms
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from app.models import Question, Answer, Tag, Profile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)


class AskForm(forms.ModelForm):
    tags = forms.CharField(required=False)

    class Meta:
        model = Question
        fields = ['title', 'text']

    def __init__(self, profile_id, **kwargs):
        self._profile_id = profile_id
        super(AskForm, self).__init__(**kwargs)

    def clean_tags(self):
        self.tags = self.cleaned_data['tags'].split()
        if len(self.tags) > 3:
            self.add_error(None, 'use no more than 3 tags!')
            raise forms.ValidationError('use no more than 3 tags!')
        return self.tags

    def save(self, **kwargs):
        question = Question()
        question.profile_id = self._profile_id
        question.title = self.cleaned_data['title']
        question.text = self.cleaned_data['text']
        question.save()

        for tag in self.tags:
            if not Tag.objects.filter(tag=tag).exists():
                Tag.objects.create(tag=tag)
        question.tags.set(Tag.objects.filter(tag__in=self.tags))
        return question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

    def __init__(self, profile_id, question_id, **kwargs):
        self._profile_id = profile_id
        self._question_id = question_id
        super(AnswerForm, self).__init__(**kwargs)

    def save(self, **kwargs):
        self.cleaned_data['profile_id'] = self._profile_id
        self.cleaned_data['question_id'] = self._question_id
        return Answer.objects.create(**self.cleaned_data)


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
