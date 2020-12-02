from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from app.models import Question, Answer, Tag, Profile
from django.contrib.auth.models import User
from app.forms import LoginForm, AskForm, TagForm, AnswerForm, SignupForm, SettingsForm


def paginate(objects_list, request, per_page=2):
    paginator = Paginator(objects_list, per_page)
    page_num = request.GET.get('page')

    return paginator.get_page(page_num)


def new_questions(request):
    questions_page = paginate(Question.objects.all(), request)
    return render(request, 'new_questions.html', {
        'content': questions_page,
    })


@login_required
def create_ask(request):
    if request.method == 'POST':
        ask_form = AskForm(data=request.POST)
        tag_form = TagForm(data=request.POST)
        if ask_form.is_valid() and tag_form.is_valid():
            question = ask_form.save(commit=False)
            question.profile_id = request.user.profile
            question.save()

            tags = tag_form.cleaned_data.get('tags').split()
            if len(tags) > 3 or len(tags) == 0:
                ask_form.add_error(None, 'Max 3 tags!')
            else:
                for _tag in tags:
                    if not Tag.objects.filter(tag=_tag).exists():
                        Tag.objects.create(tag=_tag)
                question.tags.set(Tag.objects.filter(tag__in=tags))

            return redirect(reverse('question', kwargs={'pk': question.pk}))
    return render(request, 'create_ask.html', {})


def question_page(request, pk):
    question = Question.objects.get(id=pk)
    answers_page = paginate(Answer.objects.by_question(pk), request, 1)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f"/login/?next={request.get_full_path()}")

        form = AnswerForm(data=request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.profile_id = request.user.profile
            answer.question_id = question
            answer.save()
            answers_page = paginate(Answer.objects.by_question(pk), request, 1)
            return redirect(reverse('question', kwargs={'pk': pk}) + f"?page={answers_page.paginator.num_pages}")

    return render(request, 'question.html', {
        'question': question,
        'content': answers_page,
    })


def hot_questions(request):
    questions_page = paginate(Question.objects.hot(), request)
    return render(request, 'hot_questions.html', {
        'content': questions_page,
    })


def questions_by_tag(request, tag):
    questions_page = paginate(Question.objects.by_tag(tag), request)
    return render(request, 'questions_by_tag.html', {
        'content': questions_page,
        'tag': tag,
    })


@login_required
def settings(request):
    if request.method == 'POST':
        form = SettingsForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            password_check = form.cleaned_data.get('password_check')
            avatar = form.cleaned_data.get('avatar')

            current_user = request.user
            if username is not None and current_user.username != username:
                if not User.objects.filter(username=username).exists():
                    current_user.username = username
                else:
                    form.add_error("This username is already in use")

            if email is not None and current_user.email != email:
                if not User.objects.filter(email=email).exists():
                    current_user.email = email
                else:
                    form.add_error("This email is already in use")

            if password is not None and password_check is not None:
                if password == password_check:
                    current_user.set_password(password)
                    login(request, current_user)
                else:
                    form.add_error("Passwords do not match")

            if avatar is not None:
                current_user.profile.avatar = avatar

            current_user.save()

    return render(request, 'settings.html', {})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            profile = authenticate(request, **form.cleaned_data)
            if profile is not None:
                login(request, profile)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect("/")
    return render(request, 'login.html', {})


@login_required
def logout_view(request):
    logout(request)
    previous_page = request.META.get('HTTP_REFERER')
    if previous_page is not None:
        return redirect(previous_page)
    return redirect("/")


def signup(request):
    if request.method == 'GET':
        form = SignupForm()
    else:
        form = SignupForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            password_check = form.cleaned_data.get('password_check')
            avatar = form.cleaned_data.get('avatar')
            if avatar is None:
                avatar = "img/no_avatar.png"

            if password != password_check:
                form.add_error(None, 'Passwords do not match!')
            else:
                user = User.objects.create_user(username, email, password)
                Profile.objects.create(user_id=user, avatar=avatar)
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect('/')
    return render(request, 'signup.html', {'form': form})
