from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_board/', views.createBoardView, name='create_board'),
    path('delete_board/<int:board_id>/', views.deleteBoardView, name='delete_board'),
    path('game/<int:board_id>/', views.gameView, name='game'),
    path('update_board/<int:board_id>/<int:row>/<int:col>/', views.updateBoardView, name='update_board')
]
