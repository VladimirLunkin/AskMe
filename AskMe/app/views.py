from django.shortcuts import render
from django.core.paginator import Paginator
from app.models import Question, Answer
from random import randint


questions = [
    {
        'id': idx,
        'img': f'img/ava{idx % 6 + 1}.png',
        'like': (randint(0, 120) % 100),
        'title': f'Media with stretched link? {idx}',
        'text': 'Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque ante sollicitudin. Cras purus odio, vestibulum in vulputate at, tempus viverra turpis. Fusce condimentum nunc ac nisi vulputate fringilla. Donec lacinia congue felis in faucibus.',
    } for idx in range(1, 11)
]

answers = [
    {
        'id': idx,
        'img': f'img/ava{(idx+1)%6}.png',
        'like': (randint(0, 120) % 100),
        'text': 'Quickly design and customize responsive mobile-first sites with Bootstrap, the world’s most popular front-end open source toolkit, featuring Sass variables and mixins, responsive grid system, extensive prebuilt components, and powerful JavaScript plugins.',
        'correct': True,
    } for idx in range(1, 5)
]


def paginate(objects_list, request, per_page=2):
    paginator = Paginator(objects_list, per_page)
    page_num = request.GET.get('page')

    return paginator.get_page(page_num)


def new_questions(request):
    questions_page = paginate(Question.objects1.all(), request)
    return render(request, 'new_questions.html', {
        'content': questions_page,
    })


def create_ask(request):
    return render(request, 'create_ask.html', {})


def question_page(request, pk):
    question = Question.objects1.get(id=pk)
    answers_page = paginate(answers, request, 1)
    return render(request, 'question.html', {
        'question': question,
        'content': answers_page,
    })


def hot_questions(request):
    questions_page = paginate(Question.objects1.all(), request)
    return render(request, 'hot_questions.html', {
        'content': questions_page,
    })


def questions_by_tag(request, tag):
    questions_page = paginate(Question.objects1.by_tag(tag), request)
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
