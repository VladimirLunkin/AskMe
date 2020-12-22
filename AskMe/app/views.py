from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.http import JsonResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from app.models import *
from django.contrib.auth.models import User
from app.forms import LoginForm, AskForm, AnswerForm, SignupForm, SettingsForm


def paginate(objects_list, request, limit=2):
    paginator = Paginator(objects_list, limit)
    page_num = request.GET.get('page')

    return paginator.get_page(page_num)


def new_questions(request):
    questions_page = paginate(Question.objects.all(), request)
    return render(request, 'new_questions.html', {
        'content': questions_page,
    })


@login_required
def create_ask(request):
    if request.method == 'GET':
        form = AskForm()
    else:
        form = AskForm(request.user.profile, data=request.POST)
        if form.is_valid():
            question = form.save()
            return redirect(reverse('question', kwargs={'pk': question.pk}))
    return render(request, 'create_ask.html',{
        'form': form,
    })


def question_page(request, pk):
    question = Question.objects.get(id=pk)
    answers_page = paginate(Answer.objects.by_question(pk), request, limit=1)

    if request.method == 'GET':
        form = AnswerForm()
    else:
        if not request.user.is_authenticated:
            return redirect(f"/login/?next={request.get_full_path()}")

        form = AnswerForm(profile_id=request.user.profile, question_id=question, data=request.POST)
        if form.is_valid():
            form.save()
            answers_page = paginate(Answer.objects.by_question(pk), request, limit=1)
            return redirect(reverse('question', kwargs={'pk': pk}) + f"?page={answers_page.paginator.num_pages}")

    return render(request, 'question.html', {
        'question': question,
        'content': answers_page,
        'form': form,
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
    form_updated = False
    if request.method == 'GET':
        form = SettingsForm()
    else:
        form = SettingsForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            form_updated = True
            login(request, user)
    return render(request, 'settings.html', {
        'form': form,
        'form_updated': form_updated,
    })


def login_view(request):
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            profile = authenticate(request, **form.cleaned_data)
            if profile is not None:
                login(request, profile)
                return redirect(request.POST.get('next', '/'))
    return render(request, 'login.html', {
        'form': form,
    })


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
            user = form.save()
            login(request, user)
            return redirect(request.POST.get('next', '/'))
    return render(request, 'signup.html', {
        'form': form,
    })


@require_POST
@login_required
def votes(request):
    data=request.POST
    # form = LikeForm(user=request.user.profile, data=data)
    # rating = form.save()

    like = LikeQuestion(question_id=Question.objects.get(id=data['id']), profile_id=request.user.profile, is_like=(data['action'] == 'like'))
    like.save()

    rating = Question.objects.get(id=data['id']).like
    return JsonResponse({'rating': rating})