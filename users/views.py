from django.shortcuts import render

def index(request):
    return render(request, './user/index.html')


def login_view(request):
    return render(request, './user/login.html')