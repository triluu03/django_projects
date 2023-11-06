from django.shortcuts import render, redirect

from .models import Board

import numpy as np
from .helper.check_end_conditions import checkEndGame

# Create your views here.

def home(request):
    """
    Render the home page with all the boards
    params:
        request: http request object
    return:
        HttpResponse object with HTML templates
    """
    boards = Board.objects.all()
    return render(request, 'tic_tac_toe/home.html', {'boards': boards})

def gameView(request, board_id):
    """
    Render the game page with the board
    params:
        request: http request object
        board_id: id of the board
    return:
        HttpResponse object with HTML templates
    """
    board = Board.objects.get(pk=board_id)
    size = board.size
    details = np.array(board.details.split(',')).reshape(size, size).tolist()
    return render(request, 'tic_tac_toe/game.html', {'size': range(size), 'details': details, 'board_id': board_id})

def createBoardView(request):
    """
    Handle the creation of the board
    params:
        request: http request object
    return:
        redirect to the home page
    """
    if request.method == 'POST':
        size = request.POST.get('size')
        if size == '':
            board = Board()
        else:
            details = ','.join([""]*(int(size)**2))
            board = Board(size=size, details=details)
        board.save()
    return redirect('home')

def deleteBoardView(request, board_id):
    """
    Handle the deletion of the board
    params:
        request: http request object
        board_id: id of the board
    return:
        redirect to the home page
    """
    board = Board.objects.get(pk=board_id)
    board.delete()
    return redirect('home')

def updateBoardView(request, board_id, row, col):
    """
    Handle players' moves of the game
    params:
        request: http request object
        board_id: id of the board
        row: row of the move
        col: column of the move
    return:
        redirect to the game page
    """
    if request.method == 'POST':
        board = Board.objects.get(pk=board_id)
        size = board.size
        details = np.array(board.details.split(',')).reshape(size, size)
        details[row, col] = "X"
        if checkEndGame(details, row, col):
            # Handle the ending of the game
            pass
        board.details = ",".join(details.flatten().tolist())
        board.save()
    return redirect('game', board_id=board_id)

def endGameView(request):
    pass
