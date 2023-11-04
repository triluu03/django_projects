from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_board/', views.createBoardView, name='create_board'),
    path('delete_board/<int:board_id>/', views.deleteBoardView, name='delete_board'),
]
