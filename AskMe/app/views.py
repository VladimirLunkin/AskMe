from django.shortcuts import render
from django.core.paginator import Paginator
from app.models import Question, Answer
from random import randint


def paginate(objects_list, request, per_page=2):
    paginator = Paginator(objects_list, per_page)
    page_num = request.GET.get('page')

    return paginator.get_page(page_num)


def new_questions(request):
    questions_page = paginate(Question.objects.all(), request)
    return render(request, 'new_questions.html', {
        'content': questions_page,
    })


def create_ask(request):
    return render(request, 'create_ask.html', {})


def question_page(request, pk):
    question = Question.objects.get(id=pk)
    answers_page = paginate(Answer.objects.by_question(pk), request, 1)
    return render(request, 'question.html', {
        'question': question,
        'content': answers_page,
    })


def hot_questions(request):
    questions_page = paginate(Question.objects.all(), request)
    return render(request, 'hot_questions.html', {
        'content': questions_page,
    })


def questions_by_tag(request, tag):
    questions_page = paginate(Question.objects.by_tag(tag), request)
    return render(request, 'questions_by_tag.html', {
        'content': questions_page,
        'tag': tag,
    })


def settings(request):
    return render(request, 'settings.html', {})


def login(request):
    return render(request, 'login.html', {})


def signup(request):
    return render(request, 'signup.html', {})
