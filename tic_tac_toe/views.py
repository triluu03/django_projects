from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.

def gameView(request):
    return render(request, 'tic_tac_toe/game.html', {'size': range(1, 51, 1)})