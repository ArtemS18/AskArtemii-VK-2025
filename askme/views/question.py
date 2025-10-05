from django.http import HttpResponse
from django.shortcuts import render


def main_view(request):
    return render(request, "index.html")

def ask_view(request):
    return render(request, "ask.html")

def question_view(request):
    return render(request, "question.html")

def singup_view(request):
    return render(request, "signup.html")

def login_view(request):
    return render(request, "login.html")

def user_view(request):
    return render(request, "user.html")