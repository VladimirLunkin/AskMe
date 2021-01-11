from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.http import JsonResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from app.models import *
from django.contrib.auth.models import User
from app.forms import *


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
        ava = ImageForm(data=request.POST)
    else:
        form = SettingsForm(user=request.user, data=request.POST)
        ava = ImageForm(data=request.POST, files=request.FILES, instance=request.user.profile)
        if form.is_valid():
            user = form.save()
            ava.save()
            form_updated = True
            login(request, user)
    return render(request, 'settings.html', {
        'form': form,
        'form_updated': form_updated,
        'ava': ava,
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
        ava = ImageForm()
    else:
        form = SignupForm(data=request.POST)
        ava = ImageForm()
        if form.is_valid(): # and ava.is_valid():
            user = form.save()
            login(request, user)

            # ava = ImageForm(data=request.POST, files=request.FILES, instance=request.user.profile)
            # ava.save()
            return redirect(request.POST.get('next', '/'))
    return render(request, 'signup.html', {
        'form': form,
        # 'ava': ava,
    })


@require_POST
@login_required
def votes(request):
    data=request.POST
    rating = 0
    if data['type'] == 'question':
        form = LikeQuestionForm(user=request.user.profile, question=data['id'], is_like=(data['action'] == 'like'))
        rating = form.save()
    elif data['type'] == 'answer':
        form = LikeAnswerForm(user=request.user.profile, answer=data['id'], is_like=(data['action'] == 'like'))
        rating = form.save()

    return JsonResponse({'rating': rating})


@require_POST
@login_required
def is_correct(request):
    data=request.POST
    answer = Answer.objects.get(pk=data['id'])
    if Answer.objects.filter(question_id=answer.question_id, is_correct=True).count() < 3 or answer.is_correct:
        answer.change_mind_correct()
    return JsonResponse({'action': answer.is_correct})
