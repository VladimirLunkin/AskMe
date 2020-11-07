from django.shortcuts import render

def list_ask(request):
    return render(request, 'list_ask.html', {})

def add_ask(request):
    return render(request, 'add_ask.html', {})

def ask(request):
    return render(request, 'ask.html', {})

def list_ask_tag(request):
    return render(request, 'list_ask_tag.html', {})

def settings(request):
    return render(request, 'settings.html', {})

def log_in(request):
    return render(request, 'log_in.html', {})

def register(request):
    return render(request, 'register.html', {})
