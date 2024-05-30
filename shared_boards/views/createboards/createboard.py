from django.shortcuts import render

# Create your views here.


def createboard(request):
    return render(request, './users/board.html')