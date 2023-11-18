from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from .models import Board
from django.contrib.auth.models import User

import numpy as np

# Create your views here.

@login_required(login_url='/tic_tac_toe/login/')
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

@login_required(login_url='/tic_tac_toe/login/')
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

csrf_protect
@login_required(login_url='/tic_tac_toe/login/')
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

@login_required(login_url='/tic_tac_toe/login/')
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

@login_required(login_url='/tic_tac_toe/login/')
def endGameView(request, board_id):
    return render(request, 'tic_tac_toe/end_game.html', {'board_id': board_id, 'winner': 'X'})

csrf_protect
def loginView(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'tic_tac_toe/login.html', {'message': 'Username or Password is incorrect!'})
    return render(request, 'tic_tac_toe/login.html')

def logoutView(request):
    logout(request)
    return redirect('login')

csrf_protect
def createUserView(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            return render(request, 'tic_tac_toe/create_user.html', {'message': 'Username already exists'})
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return redirect('login')
    return render(request, 'tic_tac_toe/create_user.html')
