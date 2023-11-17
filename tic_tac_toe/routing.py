from django.urls import path
from .consumers import GameConsumer

websocket_urlpatterns = [
    path("ws/tic_tac_toe/game/<int:board_id>/", GameConsumer.as_asgi()),
]