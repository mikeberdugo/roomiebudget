from django.shortcuts import render

# Create your views here.


def boards(request):
    return render(request, './boards/board.html')