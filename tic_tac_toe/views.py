from django.shortcuts import render, redirect
from django.http.response import HttpResponse

from .models import Board

# Create your views here.

def home(request):
    boards = Board.objects.all()
    return render(request, 'tic_tac_toe/home.html', {'boards': boards})

def gameView(request, board_id):
    board = Board.objects.get(pk=board_id)
    size = board.size
    return render(request, 'tic_tac_toe/game.html', {'size': range(1, size + 1, 1)})

def createBoardView(request):
    if request.method == 'POST':
        size = request.POST.get('size')
        if size == '':
            board = Board()
        else: 
            board = Board(size=size)
        board.save()
    return redirect('home')

def deleteBoardView(request, board_id):
    board = Board.objects.get(pk=board_id)
    board.delete()
    return redirect('home')