from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_board/', views.createBoardView, name='create_board'),
    path('delete_board/<int:board_id>/', views.deleteBoardView, name='delete_board'),
    path('game/<int:board_id>/', views.gameView, name='game'),
    path('game/<int:board_id>/end/', views.endGameView, name='end_game'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('create_user/', views.createUserView, name='create_user'),
]
