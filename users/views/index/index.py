from django.shortcuts import render

# Create your views here.


def login_index(request):
    return render(request, './base/base_index.html')