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

    def __init__(self, profile_id=None, **kwargs):
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

    def __init__(self, profile_id=None, question_id=None, **kwargs):
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

    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['password_check']:
            self.add_error(None, 'Passwords do not match!')
            raise forms.ValidationError('Passwords do not match!')

    def save(self, **kwargs):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = User.objects.create_user(username, email, password)

        Profile.objects.create(user_id=user)
        avatar = self.cleaned_data['avatar']
        if avatar is not None:
            Profile.avatar.set(avatar)

        return user


class SettingsForm(forms.Form):
    username = forms.CharField(required=False)
    email = forms.CharField(required=False)
    password = forms.CharField(required=False)
    password_check = forms.CharField(required=False)
    avatar = forms.ImageField(required=False)

    def __init__(self, user=None, **kwargs):
        self.user = user
        super(SettingsForm, self).__init__(**kwargs)

    def clean(self):
        if self.cleaned_data['username'] is not None and self.user.username != self.cleaned_data['username']:
            if not User.objects.filter(username=self.cleaned_data['username']).exists():
                self.add_error('This username is already in use')
                raise forms.ValidationError('This username is already in use')

        if self.cleaned_data['email'] is not None and self.user.email != self.cleaned_data['email']:
            if not User.objects.filter(email=self.cleaned_data['email']).exists():
                self.add_error('This email is already in use')
                raise forms.ValidationError('This email is already in use')

        if self.cleaned_data['password'] != self.cleaned_data['password_check']:
            self.add_error(None, 'Passwords do not match!')
            raise forms.ValidationError('Passwords do not match!')

    def save(self, **kwargs):
        self.user.username = self.cleaned_data['username']
        self.user.email = self.cleaned_data['email']

        self.user.set_password(self.cleaned_data['password'])

        if self.cleaned_data['avatar'] is not None:
            self.user.profile.avatar = self.cleaned_data['avatar']

        self.user.save()

        return self.user
