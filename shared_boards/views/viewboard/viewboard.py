from django.shortcuts import render
from common.models import Board 


def viewboard(request,slug):
    boards = Board.objects.filter(slug=slug)
    request.session['board_slug'] = slug
    return render(request, './boards/viewboard.html' , {'boards':boards})