from django.shortcuts import render

def index(request):
    return render(request, 'index.html', {})

def add_ask(request):
    return render(request, 'add_ask.html', {})

def settings(request):
    return render(request, 'settings.html', {})

def register(request):
    return render(request, 'register.html', {})

def log_in(request):
    return render(request, 'log_in.html', {})
