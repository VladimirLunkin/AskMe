from django import forms
from django.forms import ModelForm, TextInput, PasswordInput, DateTimeInput, Textarea, FileInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from app.models import *


class LoginForm(forms.Form):
    username = forms.CharField(required=True,
                               widget=TextInput(attrs={
                                   'class': 'form-control',
                               }),
                               label='Login')
    password = forms.CharField(required=True,
                               widget=PasswordInput(attrs={
                                   'class': 'form-control',
                               }),
                               label='Password')


class AskForm(forms.ModelForm):
    tags = forms.CharField(required=False,
                           widget=forms.TextInput(attrs={
                               'class': 'form-control',
                           }),
                           label='Tags')

    class Meta:
        model = Question
        fields = ['title', 'text']

        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
            }),
            'text': Textarea(attrs={
                'class': 'form-control',
                'rows': '7',
            }),
        }

        labels = {
            'title': 'Title',
            'text': 'Text',
        }

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

        widgets = {
            'text': Textarea(attrs={
                'class': 'form-control',
                'rows': '2',
                'placeholder': 'Enter your answer here...'
            }),
        }

        labels = {
            'text': 'Text',
        }

    def __init__(self, profile_id=None, question_id=None, **kwargs):
        self._profile_id = profile_id
        self._question_id = question_id
        super(AnswerForm, self).__init__(**kwargs)

    def save(self, **kwargs):
        self.cleaned_data['profile_id'] = self._profile_id
        self.cleaned_data['question_id'] = self._question_id
        return Answer.objects.create(**self.cleaned_data)


class SignupForm(forms.ModelForm):
    password2 = forms.CharField(required=True,
                               widget=PasswordInput(attrs={
                                   'class': 'form-control',
                               }),
                               label='Password check')
    # avatar = forms.ImageField(required=False,
    #                            widget=FileInput(attrs={
    #                                'class': 'custom-file',
    #                            }),
    #                            label='Avatar')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
            }),
            'email': TextInput(attrs={
                'class': 'form-control',
            }),
            'password': PasswordInput(attrs={
                'class': 'form-control',
            }),
        }

        labels = {
            'username': 'Login',
        }

    def clean(self):
        if not 'password' in self.cleaned_data or not 'password2' in self.cleaned_data:
            raise forms.ValidationError('Password is too short (minimum 1 characters)')
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            self.add_error('password', 'Passwords do not match!')
            self.add_error('password2', 'Passwords do not match!')
            raise forms.ValidationError('Passwords do not match!')

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            self.add_error(None, 'This username is already in use')
            raise forms.ValidationError('This username is already in use')
        return self.cleaned_data['username']

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            self.add_error(None, 'This email is already in use')
            raise forms.ValidationError('This email is already in use')
        return self.cleaned_data['email']

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


class SettingsForm(forms.ModelForm):
    password2 = forms.CharField(required=True,
                                widget=PasswordInput(attrs={
                                    'class': 'form-control',
                                }),
                                label='Password check')
    # avatar = forms.ImageField(required=False,
    #                           widget=FileInput(attrs={
    #                               'class': 'custom-file',
    #                           }),
    #                           label='Avatar')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
            }),
            'email': TextInput(attrs={
                'class': 'form-control',
            }),
            'password': PasswordInput(attrs={
                'class': 'form-control',
            }),
        }

        labels = {
            'username': 'Login',
        }

    def __init__(self, user=None, **kwargs):
        self.user = user
        super(SettingsForm, self).__init__(**kwargs)

    def clean(self):
        if not 'password' in self.cleaned_data or not 'password2' in self.cleaned_data:
            raise forms.ValidationError('Password is too short (minimum 1 characters)')
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            self.add_error('password', 'Passwords do not match!')
            self.add_error('password2', 'Passwords do not match!')
            raise forms.ValidationError('Passwords do not match!')

    def clean_username(self):
        if self.user.username != self.cleaned_data['username']:
            if User.objects.filter(username=self.cleaned_data['username']).exists():
                self.add_error(None, 'This username is already in use')
                raise forms.ValidationError('This username is already in use')
        return self.cleaned_data['username']

    def clean_email(self):
        if self.user.email != self.cleaned_data['email']:
            if User.objects.filter(email=self.cleaned_data['email']).exists():
                self.add_error(None, 'This email is already in use')
                raise forms.ValidationError('This email is already in use')
        return self.cleaned_data['email']

    def save(self, **kwargs):
        self.user.username = self.cleaned_data['username']
        self.user.email = self.cleaned_data['email']

        self.user.set_password(self.cleaned_data['password'])

        # if self.cleaned_data['avatar'] is not None:
        #     self.user.profile.avatar = self.cleaned_data['avatar']

        self.user.save()

        return self.user


class ImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        required = None

class LikeQuestionForm:
    def __init__(self, user, question, is_like):
        self.user = user
        self.question = Question.objects.get(id=question)
        self.is_like = is_like

    def save(self):
        if not LikeQuestion.objects.filter(question_id=self.question, profile_id=self.user).exists():
            like = LikeQuestion(question_id=self.question,
                                profile_id=self.user,
                                is_like=self.is_like)
            rating = like.save()
        else:
            like = LikeQuestion.objects.get(question_id=self.question, profile_id=self.user)
            if self.is_like == like.is_like:
                rating = like.delete()
            else:
                rating = like.change_mind()

        return rating


class LikeAnswerForm:
    def __init__(self, user, answer, is_like):
        self.user = user
        self.answer = Answer.objects.get(id=answer)
        self.is_like = is_like

    def save(self):
        if not LikeAnswer.objects.filter(answer_id=self.answer, profile_id=self.user).exists():
            like = LikeAnswer(answer_id=self.answer,
                              profile_id=self.user,
                              is_like=self.is_like)
            rating = like.save()
        else:
            like = LikeAnswer.objects.get(answer_id=self.answer, profile_id=self.user)
            if self.is_like == like.is_like:
                rating = like.delete()
            else:
                rating = like.change_mind()

        return rating
